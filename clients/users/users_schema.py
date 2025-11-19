from pydantic import BaseModel, ConfigDict, Field,EmailStr
from pydantic.alias_generators import to_camel
from tools.fakers import fake


class ShortUserSchema(BaseModel):
    """
    Краткое представление сущности User.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    email: EmailStr = Field(default_factory=fake.email)
    last_name: str = Field(default_factory=fake.last_name)
    first_name: str = Field(default_factory=fake.first_name)
    middle_name: str = Field(default_factory=fake.middle_name)

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

    password: str = Field(default_factory=fake.password)

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

    email: EmailStr | None = Field(default=fake.email())
    last_name: str | None = Field(default=fake.last_name())
    first_name: str | None = Field(default=fake.first_name())
    middle_name: str | None = Field(default=fake.middle_name())

class UpdateUserResponseSchema(GetUserResponseSchema):
    """
    Описание структуры ответа обновления пользователя.
    """
    pass

class CreateUserInvalidRequestSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    email: str = Field(default_factory=fake.email)
    last_name: str = Field(default_factory=fake.last_name)
    first_name: str = Field(default_factory=fake.first_name)
    middle_name: str = Field(default_factory=fake.middle_name)
    password: str = Field(default_factory=fake.password)