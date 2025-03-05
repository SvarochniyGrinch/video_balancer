from shared.database import get_session, SessionT
from shared.database.models import Base
from shared.schemas.common import *

from contextlib import asynccontextmanager
from sqlalchemy import exc, select, func
from fastapi import Depends
from typing import Iterable, Any, AsyncGenerator


class BaseRepo[ModelT: Base]:
    model: type[ModelT]

    def __init_subclass__(cls):
        if not hasattr(cls, "model"):
            raise AttributeError("Attribute 'model' not set")

    def __init__(self, session: SessionT = Depends(get_session)):
        self.session = session

    async def execute(self, query: Any) -> Any:
        async with self._start_session():
            return await self.session.execute(query)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def expunge(self, obj: ModelT):
        async with self._start_session():
            self.session.expunge(obj)

    async def copy(self, obj: ModelT) -> ModelT | None:
        cpy = obj.model_copy()
        cpy.id = None
        return await self.create(cpy)

    def add(self, obj: ModelT):
        self.session.add(obj)

    async def new(self, **data: Any) -> ModelT | None:
        obj = self.model(**data)
        return await self.create(obj)

    async def create(self, obj: ModelT) -> ModelT | None:
        async with self._start_session():
            self.session.add(obj)
            try:
                await self.commit()
            except exc.IntegrityError as e:
                print(e)
                await self.rollback()
                return None
        async with self._start_session():
            await self.session.refresh(obj)
        return obj

    async def get(self, id: int) -> ModelT | None:
        async with self._start_session():
            return await self.filter_one(self.model.id == id)

    async def filter(self, *where: Any, **filters: Any) -> Iterable[ModelT]:
        query = self._get_query().where(*where).filter_by(**filters)
        return (await self.execute(query)).scalars()

    async def filter_one(self, *where: Any, **filters: Any) -> ModelT | None:
        query = self._get_query().where(*where).filter_by(**filters)
        return (await self.execute(query)).scalar_one_or_none()

    async def count(self, **filters: Any) -> int:
        query = self._get_query(func.count(self.model.id)).filter_by(**filters)  # type: ignore  # noqa
        return (await self.execute(query)).scalar_one()

    async def update(self, obj: ModelT, **kwargs: Any) -> ModelT | None:
        async with self._start_session():
            for field, value in kwargs.items():
                if hasattr(obj, field):
                    setattr(obj, field, value)
            try:
                await self.commit()
            except exc.IntegrityError as e:
                print(e)
                await self.rollback()
                return None
        async with self._start_session():
            await self.session.refresh(obj)
        return obj

    async def delete(self, obj: ModelT):
        async with self._start_session():
            await self.session.delete(obj)
            await self.commit()

    async def list(self, params: ListParams,
                   **filters: Any) -> tuple[Iterable[ModelT], int]:
        query = self._get_query().filter_by(**filters)
        total = await self.count(**filters)
        query = self._apply_sort(query, params.sort)
        query = self._apply_pagination(query, params.pagination)
        items = (await self.execute(query)).scalars()
        return items, total

    def _apply_sort(self, query, params: SortParams) -> Any:
        if params.sort_by is None:
            return query
        field = getattr(self.model, params.sort_by, None)
        if field is None:
            return query
        sorting_field = field.asc() if params.sort_order == SortOrder.Asc else field.desc()
        return query.order_by(sorting_field)

    def _apply_pagination(self, query, params: PaginationParams) -> Any:
        limit = params.per_page
        offset = (params.page - 1) * limit
        return query.limit(limit).offset(offset)

    def _get_query(self, select_data: Any = None):
        if select_data is None:
            select_data = self.model
        return select(select_data)

    @asynccontextmanager
    async def _start_session(self) -> AsyncGenerator[SessionT, None]:
        if self.session.is_active:
            yield self.session
            return
        async with self.session.begin():
            yield self.session

    def check_sort(self, params: SortParams) -> bool:
        if params.sort_by is None:
            return True
        return self.contains_field(params.sort_by)

    def contains_field(self, field: str) -> bool:
        return field in self.model.model_fields
