import allure

from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, GetExercisesResponseSchema
from tools.assertions.base import assert_equal, assert_length
from clients.exercises.exercises_schema import ExerciseSchema
from clients.errors_schema import InternalErrorResponseSchema
from tools.assertions.errors import assert_internal_error_response


@allure.step('Check create exercise response')
def assert_create_exercise_response(
        request: CreateExerciseRequestSchema,
        response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на создание задания соответствует запросу.

    :param request: Исходный запрос на создание задания.
    :param response: Ответ API с данными задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(response.exercise.title, request.title, 'title')
    assert_equal(response.exercise.course_id, request.course_id, 'course_id')
    assert_equal(response.exercise.max_score, request.max_score, 'max_score')
    assert_equal(response.exercise.min_score, request.min_score, 'min_score')
    assert_equal(response.exercise.order_index, request.order_index, 'order_index')
    assert_equal(response.exercise.estimated_time, request.estimated_time, 'estimated_time')

@allure.step('Check exercise')
def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет, что фактические данные задания соответствуют ожидаемым.

    :param actual: Фактические данные задания.
    :param expected: Ожидаемые данные задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(actual.id, expected.id, 'id')
    assert_equal(actual.title, expected.title, 'title')
    assert_equal(actual.course_id, expected.course_id, 'course_id')
    assert_equal(actual.max_score, expected.max_score, 'max_score')
    assert_equal(actual.min_score, expected.min_score, 'min_score')
    assert_equal(actual.order_index, expected.order_index, 'order_index')
    assert_equal(actual.description, expected.description, 'description')
    assert_equal(actual.estimated_time, expected.estimated_time, 'estimated_time')

@allure.step('Check get exercise response')
def assert_get_exercise_response(
        get_exercise_response: GetExerciseResponseSchema,
        create_exercise_response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на получение задания соотвествует ответу на его создание.

    :param get_exercise_response: Ответ API при запросе задания.
    :param create_exercise_response: Ответ API при создании задания.
    :raises AssertionError: Если данные курсов не совпадают.
    """
    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)

@allure.step('Check get exercises response')
def assert_get_exercises_response(
        get_exercises_response: GetExercisesResponseSchema,
        create_exercises_responses: list[CreateExerciseResponseSchema]
):
    """
    Проверяет, что ответ на получение списка курсов соответствует ответам на их создание.

    :param get_exercises_response: Ответ API при запросе списка заданий.
    :param create_exercises_responses: Список API ответов при создании заданий.
    :raises AssertionError: Если данные курсов не совпадают.
    """
    assert_length(get_exercises_response.exercises, create_exercises_responses, 'exercises')

    for index, create_exercise_response in enumerate(create_exercises_responses):
        assert_exercise(get_exercises_response.exercises[index], create_exercise_response.exercise)

@allure.step('Check update exercise response')
def assert_update_exercise_response(request: UpdateExerciseRequestSchema, response: UpdateExerciseResponseSchema):
    """
    Проверяет, что ответ на обновление задания соответствует данным из запроса.

    :param request: Исходный запрос на обновление задания.
    :param response: Ответ API с обновленными данными задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    if request.title is not None:
        assert_equal(response.exercise.title, request.title, 'title')
    if request.description is not None:
        assert_equal(response.exercise.description, request.description, 'description')
    if request.max_score is not None:
        assert_equal(response.exercise.max_score, request.max_score, 'max_score')
    if request.min_score is not None:
        assert_equal(response.exercise.min_score, request.min_score, 'min_score')
    if request.estimated_time is not None:
        assert_equal(response.exercise.estimated_time, request.estimated_time, 'estimated_time')
    if request.order_index is not None:
        assert_equal(response.exercise.order_index, request.order_index, 'order_index')

@allure.step('Check get non existing exercise response')
def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    """
    Функция для проверки ошибки, если задание не найдено на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "File not found"
    """
    expected = InternalErrorResponseSchema(details='Exercise not found')
    assert_internal_error_response(actual, expected)