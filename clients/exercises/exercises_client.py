from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
from clients.exercises.exercises_schema import GetExercisesQuerySchema, GetExerciseResponseSchema, GetExercisesResponseSchema,CreateExerciseRequestSchema, CreateExerciseResponseSchema,UpdateExerciseRequestSchema, UpdateExerciseResponseSchema


class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises.
    """
    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """
        Метод для получения списка заданий курса.
        :param query: Словарь с course_id.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get('/api/v1/exercises', params=query.model_dump(by_alias=True))

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод для получения задания по его идентификатору.
        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(f'/api/v1/exercises/{exercise_id}')

    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """
        Метод для создания задания.
        :param request: Слоаврь: title, courseId, maxScore, minScore, orderIndex, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post('/api/v1/exercises', json=request.model_dump(by_alias=True))

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response:
        """
        Метод для изменения задания.
        :param exercise_id: Идентификатор задания.
        :param request: Слоаврь с title, maxScore, minScore, orderIndex, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.patch(f'/api/v1/exercises/{exercise_id}', json=request.model_dump(by_alias=True))

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод для удаление задания по его идентификатору.
        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.delete(f'/api/v1/exercises/{exercise_id}')

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseSchema:
        get_exercise_response = self.get_exercise_api(exercise_id)
        return get_exercise_response.json()

    def get_exercises(self, query: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
        get_exercises_response = self.get_exercises_api(query)
        return GetExercisesResponseSchema.model_validate_json(get_exercises_response.text)

    def create_exercise(self, request: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        create_exercise_response = self.create_exercise_api(request)
        return CreateExerciseResponseSchema.model_validate_json(create_exercise_response.text)

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> UpdateExerciseResponseSchema:
        update_exercise_response = self.update_exercise_api(exercise_id, request)
        return UpdateExerciseResponseSchema.model_validate_json(update_exercise_response.text)

def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))