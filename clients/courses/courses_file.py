from typing import TypedDict

from websockets import Response

from clients.api_client import APIClient


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
        return self.client.get('/api/v1/courses', params=query)

    def get_course_api(self, course_id: str) -> Response:
        """
        Метод для получения курса по его идентификатору.
        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.client.get(f'/api/v1/courses/{course_id}')

    def create_course_api(self, request: CreateCourseRequestDict) -> Response:
        """
        Метод для создания курса
        :param request: Словарь с title, maxScore, minScore, description, estimatedTime.
        previewFileId, createdByUserId.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.client.post('/api/v1/courses', json=request)

    def update_course_api(self, course_id: str, request: UpdateCourseRequestDict) -> Response:
        """
        Метод для обновления курса
        :param course_id, request: Словарь с title, maxScore, minScore, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.client.patch(f'/api/v1/courses/{course_id}', json=request)

    def delete_course_api(self, course_id: str) -> Response:
        """
        Удаление курса курса по его идентификатору.
        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.client.delete(f'/api/v1/courses/{course_id}')