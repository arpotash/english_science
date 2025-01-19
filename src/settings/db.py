import sqlalchemy.ext.asyncio as sa_io

from src.settings.base import normalize_url
from src.settings.settings import Config

AsyncPostgreSQLEngine = sa_io.create_async_engine(
    normalize_url(Config.DB_URI),
    echo=False,
    isolation_level=Config.SQLALCHEMY_ISOLATION_LEVEL
)

AsyncPostgreSQLSession = sa_io.async_sessionmaker(
    AsyncPostgreSQLEngine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=sa_io.AsyncSession
)

def get_async_session():
    return AsyncPostgreSQLSession()