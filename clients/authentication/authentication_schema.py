from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class TokenSchema(BaseModel):
    """
    Описание структуры аутентификационных токенов.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    token_type: str
    access_token: str
    refresh_token: str

class LoginRequestSchema(BaseModel):
    """
    Описание структуры запроса на аутентификацию
    """
    email: str
    password: str

class LoginResponseSchema(BaseModel):
    """
    Описание структуры ответа аутентификации
    """
    token: TokenSchema

class RefreshRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление токена аутентификации
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    refresh_token: str