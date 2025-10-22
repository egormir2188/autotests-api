from httpx import Response

from clients.api_client import APIClient
from typing import TypedDict

from clients.private_http_builder import get_private_http_client, AuthenticationUserDict


class UpdateUsersRequestDict(TypedDict):
    """
    Описание структуры запроса на обновление пользователя.
    """
    email: str | None
    lastName: str | None
    firstName: str | None
    middleName: str | None

class User(TypedDict):
    """
    Описание структуры пользователя.
    """
    id: str
    email: str
    lastName: str
    firstName: str
    middleName: str

class GetUserResponseDict:
    """
    Описание структуры ответа получения пользователя.
    """
    user: User

class PrivateUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """
    def get_users_me_api(self) -> Response:
        """
        Метод получения текущего пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get('/api/v1/users/me')

    def get_users_api(self, user_id: str) -> Response:
        """
        Метод для получения информации о пользователе по его user_id.
        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(f'/api/v1/users/{user_id}')

    def update_user_api(self, user_id: str, request: UpdateUsersRequestDict) -> Response:
        """
        Обновления информации о пользователе по его идентификатору.
        :param user_id: Идентификатор пользователя.
        :param request: Словарь с email, lastName, firstName, middleName.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.patch(f'/api/v1/users/{user_id}', json=request)

    def delete_user_api(self, user_id: str) -> Response:
        """
        Удаление пользователя по его идентификатору.
        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.delete(f'/api/v1/users/{user_id}')

    def get_user(self, user_id: str) -> GetUserResponseDict:
        response = self.get_users_api(user_id)
        return response.json()

def get_private_users_client(user: AuthenticationUserDict) -> PrivateUsersClient:
    """
    Функция создаёт экземпляр PrivateUsersClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию PrivateUsersClient.
    """
    return PrivateUsersClient(client=get_private_http_client(user))