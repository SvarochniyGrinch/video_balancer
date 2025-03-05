from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncIterator, TypeAlias
import asyncio
import os


DATABASE_URL = os.environ["DATABASE_URL"]

DATABASE_ENGINE = create_async_engine(
    DATABASE_URL,
    future=True,
    pool_size=100,
    max_overflow=0,
    pool_timeout=30,
    pool_recycle=900,
)

SessionT: TypeAlias = AsyncSession

SESSIONMAKER = async_sessionmaker(
    bind=DATABASE_ENGINE,
    expire_on_commit=False,
)


async def get_session() -> AsyncIterator[SessionT]:
    async with SESSIONMAKER() as session:
        yield session


@asynccontextmanager
async def get_session_ctx() -> AsyncIterator[SessionT]:
    async with SESSIONMAKER() as session:
        yield session


@asynccontextmanager
async def get_scoped_session():
    scoped_factory = async_scoped_session(
        SESSIONMAKER,
        scopefunc=asyncio.current_task,
    )
    try:
        async with scoped_factory() as session:
            yield session
    finally:
        await scoped_factory.remove()


__all__ = [
    "DATABASE_URL",
    "DATABASE_ENGINE",
    "SessionT",
    "SESSIONMAKER",
    "get_session",
    "get_session_ctx",
    "get_scoped_session",
]
