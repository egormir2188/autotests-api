from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class CreateFileRequestDict(TypedDict):
    """
    Описание структуры запросы для создания файла.
    """
    filename: str
    directory: str
    upload_file: str

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
        return self.client.post(
            '/api/v1/files',
            data=request,
            files={'upload_files': open(request['upload_file'], 'rb')}
        )

    def get_file_api(self, file_id: str) -> Response:
        """
        Получение файла по идентификатору.
        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.client.post(f'/api/v1/files/{file_id}')

    def delete(self, file_id: str) -> Response:
        """
        Удаление файла по идентификатору.
        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.client.delete(f'/api/v1/files/{file_id}')