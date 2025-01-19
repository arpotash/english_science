from sqlalchemy import orm
import sqlalchemy as sa


class Base(orm.DeclarativeBase):
    ...

class Student(Base):
    __tablename__ = 'student'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    login: orm.Mapped[str] = orm.mapped_column(sa.String)
    fio: orm.Mapped[str] = orm.mapped_column(sa.String)
    is_active: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True)
    units = orm.relationship("Unit", back_populates="student")


class Teacher(Base):
    __tablename__ = 'teacher'
    __table_args__ = (
        sa.UniqueConstraint('email', 'login', name='unique_email_login'),
    )

    fio: orm.Mapped[str] = orm.mapped_column(sa.String)
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    login: orm.Mapped[str] = orm.mapped_column(sa.String)
    email: orm.Mapped[str] = orm.mapped_column(sa.String)
    password: orm.Mapped[str] = orm.mapped_column(sa.String)
    is_active: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)


class Unit(Base):
    __tablename__ = 'unit'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String)
    student_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey('student.id'))
    student = orm.relationship("Student", back_populates="units")
    words = orm.relationship("Word", back_populates="unit")
    gaaging_idx: orm.Mapped[float] = orm.mapped_column(sa.Float, nullable=True)
    diversity_idx: orm.Mapped[float] = orm.mapped_column(sa.Float, nullable=True)

class Word(Base):
    __tablename__ = 'word'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    title: orm.Mapped[str] = orm.mapped_column(sa.String)
    unit_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey('unit.id'))
    unit = orm.relationship("Unit", back_populates="words")
    translation: orm.Mapped[str] = orm.mapped_column(sa.String)
    completed: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    word_synonyms = orm.relationship("WordSynonyms", back_populates="word")

class WordSynonyms(Base):
    __tablename__ = 'word_synonyms'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    title: orm.Mapped[str] = orm.mapped_column(sa.String)
    word_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey('word.id'))
    word = orm.relationship("Word", back_populates="word_synonyms")
