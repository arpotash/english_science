import sqlalchemy as sa
from fastapi.security import OAuth2PasswordRequestForm

from src.exceptions import TeacherNotFoundError, AuthError
from src.models import Teacher
from src.repository.abstract import AbstractRepository
from src.schemas import auth as auth_schemas
from src.utils import Password


class TeacherRepository(AbstractRepository):
    async def create(self, body: auth_schemas.RegisterUserModel) -> int:
        stmt = sa.insert(Teacher).values(
            login=body.login,
            email=body.email,
            password=Password.get_password_hash(body.password),
            fio=body.fio
        )
        teacher = await self.session.execute(stmt)

        return teacher.inserted_primary_key[0] if teacher.inserted_primary_key else 0

    async def get(self, idx: int) -> Teacher:
        stmt = sa.select(Teacher).where(Teacher.id == idx)
        teacher = (await self.session.execute(stmt)).scalars().one_or_none()

        if not teacher:
            raise TeacherNotFoundError(idx)

        return teacher

    async def get_by_login(self, login: str) -> Teacher:
        stmt = sa.select(Teacher).where(Teacher.login == login)
        teacher = (await self.session.execute(stmt)).scalars().one_or_none()

        if not teacher:
            raise TeacherNotFoundError(login)

        return teacher

    async def update(self, idx: int, data: dict) -> None:
        stmt = sa.update(Teacher).values(**data)
        await self.session.execute(stmt)


class LoginRepository(AbstractRepository):
    async def create(self, body: OAuth2PasswordRequestForm) -> Teacher:
        stmt = sa.select(Teacher).where(Teacher.login == body.username)
        teacher = (await self.session.execute(stmt)).scalars().one_or_none()

        if not teacher:
            raise AuthError('Пользователь с таким username не найден')

        if not Password.verify_password(body.password, teacher.password):
            raise AuthError('Неверный пароль')

        return teacher
