from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class ShortUserSchema(BaseModel):
    """
    Краткое представление сущности User.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str

class UserSchema(ShortUserSchema):
    """
    Полное представление сущности User.
    """
    id: str

class GetUserResponseSchema(BaseModel):
    """
    Описание структуры ответа получения пользователя.
    """
    user: UserSchema

class CreateUserRequestSchema(ShortUserSchema):
    """
    Структура запроса для создания пользователя.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    password: str

class CreateUserResponseSchema(BaseModel):
    """
    Струтура ответа создания пользователя.
    """
    user: UserSchema

class UpdateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление пользователя.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    email: EmailStr | None
    last_name: str | None
    first_name: str | None
    middle_name: str | None

class UpdateUserResponseSchema(GetUserResponseSchema):
    """
    Описание структуры ответа обновления пользователя.
    """
    pass

