import allure

from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema


class FileClient(APIClient):
    """
    Клиент для работы с /api/v1/files.
    """
    @allure.step('Create file')
    def create_file_api(self, request: CreateFileRequestSchema) -> Response:
        """
        Метода создания файла.
        :param request: Параметры запроса: filename, directory, upload_files.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(
            '/api/v1/files',
            data=request.model_dump(exclude={'upload_file'}),
            files={'upload_file': request.upload_file.read_bytes()}
        )

    @allure.step('Get file by id {file_id}')
    def get_file_api(self, file_id: str) -> Response:
        """
        Получение файла по идентификатору.
        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(f'/api/v1/files/{file_id}')

    @allure.step('Delete file by id {file_id}')
    def delete_file_api(self, file_id: str) -> Response:
        """
        Удаление файла по идентификатору.
        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.delete(f'/api/v1/files/{file_id}')

    def create_file(self, request: CreateFileRequestSchema) -> CreateFileResponseSchema:
        response = self.create_file_api(request)
        return CreateFileResponseSchema.model_validate_json(response.text)

def get_files_client(user: AuthenticationUserSchema) -> FileClient:
    """
    Функция создаёт экземпляр FileClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию FileClient.
    """
    return FileClient(client=get_private_http_client(user))