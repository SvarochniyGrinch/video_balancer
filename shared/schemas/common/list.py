from .models import CamelModel
from .pagination import PaginationParams
from .sort import SortParams
from fastapi import Depends


class ListParams(CamelModel):
    pagination: PaginationParams = Depends()
    sort: SortParams = Depends()


class ListResponse[T](CamelModel):
    items: list[T]
    total: int


__all__ = [
    "ListParams",
    "ListResponse",
]
