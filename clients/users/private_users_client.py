from httpx import Response

from clients.api_client import APIClient
from typing import TypedDict


class UpdateUsersRequestDict(TypedDict):
    """
    Описание структуры запроса на обновление пользователя.
    """
    email: str | None
    lastName: str | None
    firstName: str | None
    middleName: str | None

class PrivateUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """
    def get_users_me_api(self) -> Response:
        """
        Метод получения текущего пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.client.get('/api/v1/users/me')

    def get_users_api(self, user_id: str) -> Response:
        """
        Метод для получения информации о пользователе по его user_id.
        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.client.get(f'/api/v1/users/{user_id}')

    def update_user_api(self, user_id: str, request: UpdateUsersRequestDict) -> Response:
        """
        Обновления информации о пользователе по его идентификатору.
        :param user_id: Идентификатор пользователя.
        :param request: Словарь с email, lastName, firstName, middleName.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.client.patch(f'/api/v1/users/{user_id}', json=request)

    def delete_user_api(self, user_id: str) -> Response:
        """
        Удаление пользователя по его идентификатору.
        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.client.delete(f'/api/v1/users/{user_id}')