from httpx import Response

from clients.api_client import APIClient
from typing import TypedDict

from clients.public_http_builder import get_public_http_client


class CreateUsersRequestDict(TypedDict):
    """
    Описание структуры запроса для создания пользователя.
    """
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str

class User(TypedDict):
    """
    Описание структуры пользователя.
    """
    id: str
    email: str
    lastName: str
    firstName: str
    middleName: str

class CreateUserResponseDict(TypedDict):
    """
    Описание структуры запроса на создание пользователя.
    """
    user: User

class PublicUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """
    def create_users_api(self, request: CreateUsersRequestDict) -> Response:
        """
        Метод выполняет регистрацию пользователя.
        :param request: Словарь с ключами email, password, lastName, firstName, middleName.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post('/api/v1/users', json=request)

    def create_user(self, request: CreateUsersRequestDict) -> CreateUserResponseDict:
        response = self.create_users_api(request)
        return response.json()

def get_public_users_client() ->PublicUsersClient:
    """
    Функция создаёт экземпляр PublicUsersClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PublicUsersClient.
    """
    return PublicUsersClient(client=get_public_http_client())