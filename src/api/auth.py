import fastapi
import jwt
from fastapi import APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import DecodeError

from src.external_systems.unit_of_work import AsyncSqlAlchemyUnitOfWork
from src.repository import auth as auth_repo
from src.schemas import auth as auth_schemas
from src import utils
from src.settings.db import get_async_session

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=auth_schemas.UserResponseModel)
async def register(
    body: auth_schemas.RegisterUserModel,
    session: AsyncSession = fastapi.Depends(get_async_session)
):
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)
    async with async_unit_of_work:
        repository = auth_repo.TeacherRepository(session)
        created_teacher_id = await repository.create(body)
        teacher = await repository.get(created_teacher_id)

    verification_token = utils.Token.encode_verification_token(teacher.login)
    await utils.send_mail(body.email, verification_token)

    return auth_schemas.UserResponseModel(
        login=teacher.login,
        email=teacher.email,
        id=teacher.id
    )

@auth_router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=auth_schemas.AccessTokenModel
)
async def login(
    body: OAuth2PasswordRequestForm = fastapi.Depends(),
    session: AsyncSession = fastapi.Depends(get_async_session)
) -> auth_schemas.AccessTokenModel:
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    async with async_unit_of_work:
        repository = auth_repo.LoginRepository(session)
        logged_user = await repository.create(body)

    access_token = utils.Token.encode_auth_token(logged_user.login)

    return auth_schemas.AccessTokenModel(access_token=access_token)

@auth_router.get('/verify', status_code=status.HTTP_200_OK)
async def verify(
    access_token: str = fastapi.Query(...),
    session: AsyncSession = fastapi.Depends(get_async_session)
):
    if not access_token:
        raise DecodeError

    try:
        decoded_token = utils.Token.decode_auth_token(access_token)
    except (
            jwt.DecodeError,
            jwt.ExpiredSignatureError,
            jwt.InvalidSignatureError,
            jwt.InvalidTokenError,
            jwt.InvalidKeyError,
            jwt.InvalidAlgorithmError
    ) as e:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail=e)

    user_login = decoded_token.get('iss')
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    async with async_unit_of_work:
        repository = auth_repo.TeacherRepository(session)
        user = await repository.get_by_login(user_login)
        await repository.update(user.id, {'is_active': True})
