from typing import TypedDict

from websockets import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client


class GetExercisesQueryDict(TypedDict):
    """
    Описание структуры запроса для получения списка заданий курса.
    """
    course_id: str

class CreateExerciseRequestDict(TypedDict):
    """
    Описание структуры запроса для создания задания.
    """
    title: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str

class UpdateExerciseRequestDict(TypedDict):
    """
    Описание структуры запроса для обновления задания.
    """
    title: str | None
    maxScore: int | None
    minScore: int | None
    orderIndex: int | None
    description: str | None
    estimatedTime: str | None

class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises.
    """
    def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
        """
        Метод для получения списка заданий курса.
        :param query: Словарь с course_id.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get('/api/v1/exercises', params=query)

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод для получения задания по его идентификатору.
        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(f'/api/v1/exercises/{exercise_id}')

    def create_exercise_api(self, request: CreateExerciseRequestDict) -> Response:
        """
        Метод для создания задания.
        :param request: Слоаврь: title, courseId, maxScore, minScore, orderIndex, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post('/api/v1/exercises', json=request)

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestDict) -> Response:
        """
        Метод для изменения задания.
        :param exercise_id: Идентификатор задания.
        :param request: Слоаврь с title, maxScore, minScore, orderIndex, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.patch(f'/api/v1/exercises/{exercise_id}', json=request)

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод для удаление задания по его идентификатору.
        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.delete(f'/api/v1/exercises/{exercise_id}')

def get_exercises_client(user: AuthenticationUserDict) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))