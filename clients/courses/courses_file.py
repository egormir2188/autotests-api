from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.files.files_cliet import File
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client
from clients.users.private_users_client import User


class Course(TypedDict):
    """
    Описание структуры курса.
    """
    id: str
    title: str
    maxScore: int
    minScore: int
    description: str
    previewFile: File
    estimatedTime: str
    createdByUser: User

class CreateCourseResponse(TypedDict):
    """
    Описание структуры ответа создания курса.
    """
    course: Course

class GetCoursesQueryDict(TypedDict):
    """
    Описание стрктуры запроса для получения списка курсов.
    """
    user_id: str

class CreateCourseRequestDict(TypedDict):
    """
    Описание структуры запроса для создания курса.
    """
    title: str
    maxScore: int
    minScore: int
    description: str
    previewFileId: str
    estimatedTime: str
    createdByUserId: str

class UpdateCourseRequestDict(TypedDict):
    title: str | None
    maxScore: int | None
    description: str | None
    estimatedTime: str | None

class CoursesClient(APIClient):
    """
    Клиент для работы с /api/v1/courses.
    """
    def get_courses_api(self, query: GetCoursesQueryDict) -> Response:
        """
        Метод для получения списка курсов.
        :param query: Словарь с user_id.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get('/api/v1/courses', params=query)

    def get_course_api(self, course_id: str) -> Response:
        """
        Метод для получения курса по его идентификатору.
        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(f'/api/v1/courses/{course_id}')

    def create_course_api(self, request: CreateCourseRequestDict) -> Response:
        """
        Метод для создания курса
        :param request: Словарь с title, maxScore, minScore, description, estimatedTime.
        previewFileId, createdByUserId.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post('/api/v1/courses', json=request)

    def update_course_api(self, course_id: str, request: UpdateCourseRequestDict) -> Response:
        """
        Метод для обновления курса
        :param course_id: Идентификатор курса
        :param request: Словарь с title, maxScore, minScore, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.patch(f'/api/v1/courses/{course_id}', json=request)

    def delete_course_api(self, course_id: str) -> Response:
        """
        Удаление курса курса по его идентификатору.
        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.delete(f'/api/v1/courses/{course_id}')

    def create_course(self, request: CreateCourseRequestDict):
        response = self.create_course_api(request)
        return response.json()

def get_course_client(user: AuthenticationUserDict) -> CoursesClient:
    """
    Функция создаёт экземпляр CoursesClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию CoursesClient.
    """
    return CoursesClient(client=get_private_http_client(user))