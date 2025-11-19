import allure

from clients.authentication.authentication_schema import LoginResponseSchema
from clients.errors_schema import InternalErrorResponseSchema
from tools.assertions.base import assert_equal, assert_is_true
from tools.logger import get_logger


logger = get_logger('AUTHENTICATION_ASSERTIONS')

@allure.step('Check login response')
def assert_login_response(response: LoginResponseSchema):
    """
    Проверяет корректность ответа при успешной авторизации.

    :param response: Объект ответа с токенами авторизации.
    :raises AssertionError: Если какое-либо из условий не выполняется.
    """
    logger.info('Check login response')

    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")

@allure.step('Check login non existing user')
def assert_login_incorrect_user_data(actual: InternalErrorResponseSchema):
    """
    Проверяет корректность ответа авторизации несуществующего пользователя.
    :param actual: Объект ответа с ошибкойю.
    :raise assertion: Если формулировка ошибки не совпадает
    """
    logger.info('Check login non existing user')

    expected = InternalErrorResponseSchema(details='Invalid credentials')

    assert_equal(actual, expected, 'details')