import pydantic


class StudentForListingResponse(pydantic.BaseModel):
    id: int
    fio: str
    login: str


class UnitForListingResponse(pydantic.BaseModel):
    id: int
    name: str
    gaaginx_idx: float


class WordForListingResponse(pydantic.BaseModel):
    id: int
    title: str
    translation: str


class CreateUnitWordRequest(pydantic.BaseModel):
    title: str


class UpdateUnitWordRequest(pydantic.BaseModel):
    title: str
    translation: str
    completed: bool

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
