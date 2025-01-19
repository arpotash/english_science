import pydantic

class RegisterUserModel(pydantic.BaseModel):
    email: str = pydantic.Field(default='test_mail@gmail.com')
    login: str = pydantic.Field(default='тестовый логин')
    fio: str = pydantic.Field(default='Тестовый тест тестович')
    password: str = pydantic.Field()
    confirm_password: str = pydantic.Field()

    def validate_password(self, password: str, confirm_password):
        if len(password) < 8:
            raise pydantic.ValidationError('Длина пароля должна быть не менее 8 символов')
        if password != confirm_password:
            raise pydantic.ValidationError('Пароли должны совпадать')


class LoginUserModel(pydantic.BaseModel):
    username: str = pydantic.Field(default='test_mail@gmail.com')
    password: str = pydantic.Field()


class UserResponseModel(pydantic.BaseModel):
    id: int = pydantic.Field(default=1)
    email: str = pydantic.Field(default='test_mail@gmail.com')
    login: str = pydantic.Field(default='тестовый логин')


class AccessTokenModel(pydantic.BaseModel):
    access_token: str = pydantic.Field()