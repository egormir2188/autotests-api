from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client


class CreateFileRequestDict(TypedDict):
    """
    Описание структуры запросы для создания файла.
    """
    filename: str
    directory: str
    upload_file: str

class File(TypedDict):
    """
    Описание структуры файла.
    """
    id: str
    fileName: str
    directory: str
    url: str

class CreateFileResponseDict(TypedDict):
    """
    Описание структуры запроса на создание файла.
    """
    file: File

class FileClient(APIClient):
    """
    Клиент для работы с /api/v1/files.
    """
    def create_file_api(self, request: CreateFileRequestDict) -> Response:
        """
        Метода создания файла.
        :param request: Параметры запроса: filename, directory, upload_files.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(
            '/api/v1/files',
            data=request,
            files={'upload_file': open(request['upload_file'], 'rb')}
        )

    def get_file_api(self, file_id: str) -> Response:
        """
        Получение файла по идентификатору.
        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(f'/api/v1/files/{file_id}')

    def delete(self, file_id: str) -> Response:
        """
        Удаление файла по идентификатору.
        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.delete(f'/api/v1/files/{file_id}')

    def create_file(self, request: CreateFileRequestDict) -> CreateFileResponseDict:
        response = self.create_file_api(request)
        return response.json()

def get_files_client(user: AuthenticationUserDict) -> FileClient:
    """
    Функция создаёт экземпляр FileClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию FileClient.
    """
    return FileClient(client=get_private_http_client(user))