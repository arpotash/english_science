import pydantic


class StudentForListingResponse(pydantic.BaseModel):
    id: int
    fio: str
    login: str


class UnitForListingResponse(pydantic.BaseModel):
    id: int
    name: str
    gaaginx_idx: float | None = None
    diversity_idx: float | None = None



class WordForListingResponse(pydantic.BaseModel):
    id: int
    title: str
    translation: str
    topic: str | None = None

class CreateUnitWordRequest(pydantic.BaseModel):
    title: str
    topic: str

class CreateUnitRequest(pydantic.BaseModel):
    name: str

class UpdateUnitWordRequest(pydantic.BaseModel):
    title: str | None = None
    translation: str | None = None
    completed: bool | None = None

class CreateStudentRequest(pydantic.BaseModel):
    login: str
    fio: str


class UpdateStudentRequest(pydantic.BaseModel):
    login: str | None = None
    fio: str  | None = None
    is_active: bool | None = None


class UpdateTeacherRequest(pydantic.BaseModel):
    login: str
    fio: str
    is_active: bool

class UpdateUnitRequest(pydantic.BaseModel):
    name: str | None = None


class CsvFileColumns(pydantic.BaseModel):
    title: str
    topic: str