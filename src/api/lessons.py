import fastapi
import httpx
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.auth_dependency import get_current_user
from src.external_systems.unit_of_work import AsyncSqlAlchemyUnitOfWork
from src.models import Teacher
from src.settings.db import get_async_session
from src.repository import lesson as lesson_repo
from src.schemas import lesson as lesson_schema
from src.repository import auth as auth_repo
from src.settings.settings import Config
from src.utils import UnitParams, CsvFileManager, OxfordApi

lessons_router = fastapi.APIRouter(
    prefix='/lessons',
    tags=['lessons'],
    dependencies=[fastapi.Depends(get_current_user)]
)


@lessons_router.post(
    '/students',
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=None
)
async def create_student(
    body: lesson_schema.CreateStudentRequest,
    session: AsyncSession = fastapi.Depends(get_async_session),
):
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    async with async_unit_of_work:
        repository = lesson_repo.StudentRepository(session)
        await repository.create(body)


@lessons_router.get(
    '/students',
    status_code=fastapi.status.HTTP_200_OK,
    response_model=list[lesson_schema.StudentForListingResponse]
)
async def get_students(
    session: AsyncSession = fastapi.Depends(get_async_session),
) -> list[lesson_schema.StudentForListingResponse]:
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    async with async_unit_of_work:
        repository = lesson_repo.StudentRepository(session)
        students = await repository.list()

    return [
        lesson_schema.StudentForListingResponse(
            login=student.login, id=student.id, fio=student.fio) for student in students
    ]


@lessons_router.patch(
    '/students/{student_id}',
    status_code=fastapi.status.HTTP_200_OK,
    response_model=None
)
async def update_student_profile(
    body: lesson_schema.UpdateStudentRequest,
    student_id: int = fastapi.Path(...),
    session: AsyncSession = fastapi.Depends(get_async_session),
) -> None:
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    async with async_unit_of_work:
        repository = lesson_repo.StudentRepository(session)
        await repository.update(student_id, body.model_dump())


@lessons_router.get(
    '/students/{student_id}/units',
    status_code=fastapi.status.HTTP_200_OK,
    response_model=list[lesson_schema.UnitForListingResponse]
)
async def get_units_by_student(
    student_id: int = fastapi.Path(...),
    session: AsyncSession = fastapi.Depends(get_async_session),
) -> list[lesson_schema.UnitForListingResponse]:
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    async with async_unit_of_work:
        repository = lesson_repo.UnitRepository(session)
        units = await repository.list(student_id=student_id)

    return [
        lesson_schema.UnitForListingResponse(
            id=unit.id, name=unit.name, gaaginx_idx=unit.gaaging_idx
        ) for unit in units
    ]

@lessons_router.post(
    '/students/{student_id}/units',
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=None
)
async def create_unit(
    body: lesson_schema.CreateUnitRequest,
    student_id: int = fastapi.Path(...),
    session: AsyncSession = fastapi.Depends(get_async_session),
) -> None:
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    async with async_unit_of_work:
        repository = lesson_repo.UnitRepository(session)
        await repository.create(body, student_id=student_id)

@lessons_router.patch(
    '/students/{student_id}/units/{unit_id}',
    status_code=fastapi.status.HTTP_200_OK,
    response_model=None
)
async def update_unit(
    body: lesson_schema.UpdateUnitRequest,
    student_id: int = fastapi.Path(...),
    unit_id: int = fastapi.Path(...),
    session: AsyncSession = fastapi.Depends(get_async_session),
) -> None:
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    async with async_unit_of_work:
        repository = lesson_repo.UnitRepository(session)
        await repository.update(unit_id, body.model_dump())



@lessons_router.patch(
    '/teachers/{teacher_id}',
    status_code=fastapi.status.HTTP_200_OK,
    response_model=None
)
async def update_teacher_profile(
    body: lesson_schema.UpdateTeacherRequest,
    teacher_id: int = fastapi.Path(...),
    session: AsyncSession = fastapi.Depends(get_async_session),
) -> None:
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    async with async_unit_of_work:
        repository = auth_repo.TeacherRepository(session)
        await repository.update(teacher_id, body.model_dump())


@lessons_router.get(
    '/units/{unit_id}/words',
    status_code=fastapi.status.HTTP_200_OK,
    response_model=list[lesson_schema.WordForListingResponse]
)
async def get_words_by_unit(
    unit_id: int = fastapi.Path(...),
    session: AsyncSession = fastapi.Depends(get_async_session),
) -> list[lesson_schema.WordForListingResponse]:
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    async with async_unit_of_work:
        repository = lesson_repo.WordRepository(session)
        words = await repository.list(unit_id=unit_id)

    return [
        lesson_schema.WordForListingResponse(
            id=word.id, title=word.title, translation=word.translation, topic=word.topic
        ) for word in words
    ]

@lessons_router.post(
    '/units/{unit_id}/words',
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=None
)
async def create_new_word_into_unit(
    body: lesson_schema.CreateUnitWordRequest,
    unit_id: int = fastapi.Path(...),
    session: AsyncSession = fastapi.Depends(get_async_session),
    user: Teacher = fastapi.Depends(get_current_user)
):
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    word_meta = await OxfordApi.parse_word_from_api(body.title)

    if word_meta:
        word_meaning = OxfordApi.get_meaning(word_meta)
        word_synonyms = OxfordApi.get_synonyms(word_meta)

        async with async_unit_of_work:
            repository = lesson_repo.WordRepository(session)

            word_id = await repository.create(body, word_meaning, unit_id)
            unit_words = await repository.list(unit_id)
            gaaging_idx = UnitParams.calculate_gag_index(unit_words)
            diversity_idx = UnitParams.calculate_diversity_index(unit_words)

            repository = lesson_repo.WordSynonymRepository(session)
            await repository.bulk_create(word_synonyms, word_id)

            repository = lesson_repo.UnitRepository(session)
            await repository.update(
                unit_id,
                {'gaaging_idx': gaaging_idx, 'diversity_idx': diversity_idx}
            )

@lessons_router.patch(
    '/units/{unit_id}/words/{word_id}',
    status_code=fastapi.status.HTTP_200_OK,
    response_model=None
)
async def update_unit_word(
    body: lesson_schema.UpdateUnitWordRequest,
    unit_id: int = fastapi.Path(...),
    session: AsyncSession = fastapi.Depends(get_async_session),
    word_id: int = fastapi.Path(...),
) -> None:
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    async with async_unit_of_work:
        repository = lesson_repo.WordRepository(session)
        await repository.update(word_id, body.model_dump())

    async with async_unit_of_work:
        repository = lesson_repo.WordRepository(session)
        unit_words = await repository.list(unit_id)
        gaaging_idx = UnitParams.calculate_gag_index(unit_words)
        diversity_idx = UnitParams.calculate_diversity_index(unit_words)

        repository = lesson_repo.UnitRepository(session)
        await repository.update(
            unit_id,
            {'gaaging_idx': gaaging_idx, 'diversity_idx': diversity_idx}
        )


@lessons_router.delete(
    '/units/{unit_id}/words/{word_id}',
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_unit_word(
    unit_id: int = fastapi.Path(...),
    session: AsyncSession = fastapi.Depends(get_async_session),
    word_id: int = fastapi.Path(...),
) -> None:
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    async with async_unit_of_work:
        repository = lesson_repo.WordRepository(session)
        await repository.delete(word_id)

@lessons_router.post(
    'units/{unit_id}/words/upload',
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=None
)
async def upload_unit_words(
    unit_id: int = fastapi.Path(...),
    session: AsyncSession = fastapi.Depends(get_async_session),
    file: UploadFile = fastapi.File(...)
) -> None:
    async_unit_of_work = AsyncSqlAlchemyUnitOfWork(session)

    contents = await file.read()
    contents = contents.decode("utf-8")
    list_of_words = CsvFileManager.read(contents)

    for one_word in list_of_words:
        async with async_unit_of_work:
            word_meta = await OxfordApi.parse_word_from_api(one_word.title)

            if word_meta:
                word_meaning = OxfordApi.get_meaning(word_meta)
                word_synonyms = OxfordApi.get_synonyms(word_meta)

                word_repo = lesson_repo.WordRepository(session)
                word_id = await word_repo.create(one_word, word_translation=word_meaning, unit_id=unit_id)

                word_synonyms_repo = lesson_repo.WordSynonymRepository(session)
                await word_synonyms_repo.bulk_create(word_synonyms, word_id)


    async with async_unit_of_work:

        repository = lesson_repo.WordRepository(session)
        unit_words = await repository.list(unit_id)

        gaaging_idx = UnitParams.calculate_gag_index(unit_words)
        diversity_idx = UnitParams.calculate_diversity_index(unit_words)

        repository = lesson_repo.UnitRepository(session)
        await repository.update(
            unit_id,
            {'gaaging_idx': gaaging_idx, 'diversity_idx': diversity_idx}
        )