from httpx import Response

from clients.api_client import APIClient
from typing import TypedDict


class CreateUsersRequestDict(TypedDict):
    """
    Описание структуры запроса для создания пользователя
    """
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str

class PublicUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """
    def create_users_api(self, request: CreateUsersRequestDict) -> Response:
        """
        Метод выполняет регистрацию пользователя
        :param request: Словарь с ключами email, password, lastName, firstName, middleName
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.client.post('/api/v1/users', json=request)