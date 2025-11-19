import allure

from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema, ValidationErrorSchema
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, UpdateUserRequestSchema, \
    UpdateUserResponseSchema, CreateUserInvalidRequestSchema
from clients.users.users_schema import GetUserResponseSchema, UserSchema
from tools.assertions.base import assert_equal
from tools.assertions.errors import assert_internal_error_response, assert_validation_error_response
from tools.logger import get_logger


logger = get_logger('USERS_ASSERTIONS')

@allure.step('Check create user response')
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    """
    Проверяет, что ответ на создание пользователя соответствует запросу.

    :param request: Исходный запрос на создание пользователя.
    :param response: Ответ API с данными пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check create user response')

    assert_equal(response.user.email, request.email, 'email')
    assert_equal(response.user.first_name, request.first_name, 'first_name')
    assert_equal(response.user.middle_name, request.middle_name, 'middle_name')
    assert_equal(response.user.last_name, request.last_name, 'last_name')

@allure.step('Check user')
def assert_user(actual: UserSchema, expected: UserSchema):
    """
    Функция проверяет заданную UserSchema
    :param actual: Заданная UserSchema.
    :param expected: Ожидаемая UserSchema.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check user')

    assert_equal(actual.id, expected.id, 'id')
    assert_equal(actual.email, expected.email, 'email')
    assert_equal(actual.first_name, expected.first_name, 'first_name')
    assert_equal(actual.middle_name, expected.middle_name, 'middle_name')
    assert_equal(actual.last_name, expected.last_name, 'last_name')

@allure.step('Check get user response')
def assert_get_user_response(
        get_user_response: GetUserResponseSchema,
        create_user_response: CreateUserResponseSchema
):
    """
    Проверяет, что ответ на запрос информации о пользователе соотвествует ожидаемой информаии.
    :param get_user_response: Ответ от API с данными пользователя.
    :param create_user_response: Ответ от API с данными создания пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check get user response')

    assert_user(get_user_response.user, create_user_response.user)

@allure.step('Check update user response')
def assert_update_user_response(
        request: UpdateUserRequestSchema,
        response: UpdateUserResponseSchema
):
    """
    Проверяет, что ответ на обновление пользователя соответствует данным из запроса.

    :param request: Исходный запрос на обновление пользователя.
    :param response: Ответ API с обновленными данными пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check update user response')

    if request.email is not None:
        assert_equal(response.user.email, request.email, 'email')
    if request.first_name is not None:
        assert_equal(response.user.first_name, request.first_name, 'first_name')
    if request.middle_name is not None:
        assert_equal(response.user.middle_name, request.middle_name, 'middle_name')
    if request.last_name is not None:
        assert_equal(response.user.last_name, request.last_name, 'last_name')

@allure.step('Check get non existing user response')
def assert_user_not_found_response(actual: InternalErrorResponseSchema):
    """
    Функция для проверки ошибки, если пользователь не найден на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "File not found".
    """
    logger.info('Check get non existing user response')

    expected = InternalErrorResponseSchema(details='Invalid or expired token')
    assert_internal_error_response(actual, expected)

@allure.step('Check create user with invalid email response')
def assert_check_create_user_with_invalid_email_response(actual: ValidationErrorResponseSchema, request: CreateUserInvalidRequestSchema):
    """
    Функция для проверки ошибки, если пльзователь создается с некорректным email.
    :param actual: Фактический ответ.
    :param request: Запрос на создание пользователя.
    :raise AssertionError: Если фактический результат не соотвествует ошибке "value is not a valid email address: An email address must have an @-sign.".
    """
    logger.info('Check create user with invalid email response')

    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type='value_error',
                location=[
                    "body",
                    "email"
                ],
                message='value is not a valid email address: An email address must have an @-sign.',
                input=request.email,
                context={
                    "reason": "An email address must have an @-sign."
                }
            )
        ]
    )

    assert_validation_error_response(actual, expected)

@allure.step('Check create user with empty first name response')
def assert_create_user_with_empty_response(actual: ValidationErrorResponseSchema):
    """
    Функция для проверки ответа при создании пользователя с пустым именем.
    :param actual: Фактический результат.
    :raise AssertionError: Если фактический результат не соотвествует ошибке "String should have at least 1 character"
    """
    logger.info('Check create user with empty first name response')

    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type='string_too_short',
                location=[
                    "body",
                    "firstName"
                ],
                message='String should have at least 1 character',
                input='',
                context={
                    "min_length": 1
                }
            )
        ]
    )

    assert_validation_error_response(actual, expected)
