from typing import AsyncIterator
from abc import ABC

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from grocery.config import PostgreSqlConfig


class DatabaseConnector:
    def __init__(self) -> None:
        self.engine = create_async_engine(
            url=PostgreSqlConfig().DSN,
            pool_size=PostgreSqlConfig().POOL_SIZE,
        )
        self.sessionmaker = async_sessionmaker(self.engine, expire_on_commit=False)
    
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.sessionmaker() as session:
            yield session
            await session.commit()

    async def get_session_read_only(self) -> AsyncIterator[AsyncSession]:
        async with self.sessionmaker() as session:
            await session.execute(text("SET TRANSACTION READ ONLY"))
            yield session


class Session(ABC):
    ...


class SessionReadOnly(ABC):
    ...
