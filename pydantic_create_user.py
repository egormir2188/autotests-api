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

class CreateUserRequestSchema(ShortUserSchema):
    """
    Структура запроса для создания пользователя.
    """
    password: str

class CreateUserResponseSchema(BaseModel):
    """
    Струтура ответа создания пользователя.
    """
    user: UserSchema