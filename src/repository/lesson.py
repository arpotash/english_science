import typing as t

import sqlalchemy as sa

from src import models
from src.repository.abstract import AbstractRepository
from src.schemas import lesson as lesson_schemas


class StudentRepository(AbstractRepository):

    async def list(self, **kwargs):
        stmt = sa.select(models.Student)
        return (await self.session.execute(stmt)).scalars().all()

    async def update(self, idx: int, body: dict) -> None:
        body = {key: value for key, value in body.items() if value is not None}
        stmt = sa.update(models.Student).where(models.Student.id == idx).values(**body)
        await self.session.execute(stmt)

    async def create(self, body: lesson_schemas.CreateStudentRequest) -> None:
        stmt = sa.insert(models.Student).values(
            fio=body.fio,
            login=body.login,
            is_active=True
        )
        await self.session.execute(stmt)

class UnitRepository(AbstractRepository):

    async def list(self, student_id: int | None = None):
        stmt = sa.select(models.Unit)
        filters = []

        if student_id:
            filters.append(models.Unit.student_id == student_id)

        stmt = stmt.filter(*filters)
        units = (await self.session.execute(stmt)).scalars().all()

        return units

    async def update(self, idx: int, body: t.Any) -> t.NoReturn:
        stmt = sa.update(models.Unit).where(models.Unit.id == idx).values(**body)
        await self.session.execute(stmt)

    async def create(
        self,
        body: lesson_schemas.CreateUnitRequest,
        student_id: int | None = None
    ) -> None:
        stmt = sa.insert(models.Unit).values(
            name=body.name,
            student_id=student_id
        )
        await self.session.execute(stmt)

class WordRepository(AbstractRepository):

    async def list(self, unit_id: int | None = None):
        stmt = sa.select(models.Word)
        filters = []

        if unit_id:
            filters.append(models.Word.unit_id == unit_id)

        stmt = stmt.filter(*filters)
        words = (await self.session.execute(stmt)).scalars().all()

        return words

    async def create(
        self,
        body: lesson_schemas.CreateUnitWordRequest | lesson_schemas.CsvFileColumns,
        word_translation: str | None = None,
        unit_id: int | None = None
    ) -> int:
        stmt = sa.insert(models.Word).values(
            title=body.title,
            unit_id=unit_id,
            topic=body.topic,
            translation=word_translation
        )
        result = await self.session.execute(stmt)
        return result.inserted_primary_key[0] if result.inserted_primary_key else 0

    async def update(self, idx: int, body: dict) -> None:
        stmt = sa.update(models.Word).where(models.Word.id == idx).values(**body)
        await self.session.execute(stmt)


    async def delete(self, idx: int) -> None:
        stmt = sa.delete(models.Word).where(models.Word.id == idx)
        await self.session.execute(stmt)

class WordSynonymRepository(AbstractRepository):

    async def bulk_create(self, titles: list, word_id: int) -> None:
        for title in titles:
            stmt = sa.insert(models.WordSynonyms).values(
                title=title,
                word_id=word_id,
            )
            await self.session.execute(stmt)
