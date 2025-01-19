import abc

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractUnitOfWork(abc.ABC):

    @abc.abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @property
    def outer_session(self) -> AsyncSession:
        raise NotImplementedError


class AsyncSqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self):
        if not self._session.in_transaction():
            await self._session.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                await self._session.commit()
            else:
                await self._session.rollback()
        finally:
            await self._session.close()

    @property
    def outer_session(self) -> AsyncSession:
        return self._session
