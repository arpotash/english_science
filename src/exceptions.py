import typing as t

class ApiError(Exception):
    ...

class TeacherError(ApiError):
    ...


class TeacherNotFoundError(TeacherError):
    def __init__(self, field: str | int):
        self.status_code = 404
        self.message = f'Учитель не найден по указанным параметрам {field}'

class AuthError(ApiError):
    def __init__(self, message: str):
        self.status_code = 401
        self.message = message
