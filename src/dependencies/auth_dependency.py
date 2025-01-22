import fastapi
import typing as t
import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.external_systems.unit_of_work import AsyncSqlAlchemyUnitOfWork
from src.models import Teacher
from src.repository import auth as auth_repo
from src.settings.db import get_async_session
from src.settings.settings import Config


class TokenData(BaseModel):
    username: str | None = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    request: fastapi.Request,
    token: t.Annotated[str, fastapi.Depends(oauth2_scheme)],
    session: AsyncSession = fastapi.Depends(get_async_session)
) -> Teacher:
    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.AUTH_SECRET_KEY, algorithms=[Config.AUTH_ALGORITHM])
        username: str = payload.get("iss")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)
    async with async_unit_of_work:
        repository = auth_repo.TeacherRepository(session)
        user = await repository.get_by_login(token_data.username)

    if user is None:
        raise credentials_exception

    return user
