import typing as t

from sqlalchemy.ext.asyncio import AsyncSession

class AbstractRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, body: t.Any) -> t.NoReturn:
        raise NotImplemented

    async def get(self, idx: int) -> t.NoReturn:
        raise NotImplemented

    async def list(self, **kwargs) -> t.NoReturn:
        raise NotImplemented

    async def update(self, idx: int, body: t.Any) -> t.NoReturn:
        raise NotImplemented

    async def delete(self, idx: int) -> t.NoReturn:
        raise NotImplemented