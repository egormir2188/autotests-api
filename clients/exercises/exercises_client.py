from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client


class Exercise(TypedDict):
    """
    Описание структуры задания.
    """
    id: str
    title: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str


class GetExercisesQueryDict(TypedDict):
    """
    Описание структуры запроса для получения списка заданий курса.
    """
    courseId: str

class GetExercisesResponseDict(TypedDict):
    """
    Описание структуры ответа получения списка заданий
    """
    exercises: list[Exercise]

class GetExerciseResponseDict(TypedDict):
    """
    Описание структуры ответа создания/получения/обновлении задания
    """
    exercise: Exercise


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


class CreateExerciseResponseDict(GetExerciseResponseDict):
    """
    Описание структуры ответа обновления задания (полностью наследуется от GetExerciseResponseDict).
    """
    pass

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

class UpdateExerciseResponseDict(GetExerciseResponseDict):
    """
    Описание структуры ответа обновления задания (полностью наследуется от GetExerciseResponseDict).
    """
    pass

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

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseDict:
        get_exercise_response = self.get_exercise_api(exercise_id)
        return get_exercise_response.json()

    def get_exercises(self, query: GetExercisesQueryDict) -> GetExercisesResponseDict:
        get_exercises_response = self.get_exercises_api(query)
        return get_exercises_response.json()

    def create_exercise(self, request: CreateExerciseRequestDict) -> CreateExerciseResponseDict:
        create_exercise_response = self.create_exercise_api(request)
        return create_exercise_response.json()

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequestDict) -> UpdateExerciseResponseDict:
        update_exercise_response = self.update_exercise_api(exercise_id, request)
        return update_exercise_response.json()

def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))