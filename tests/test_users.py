import pytest
from http import HTTPStatus

from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from fixtures.users import UserFixture
from tools.assertions.schema import validate_json_schema
from tools.assertions.base import assert_status_code
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.fakers import fake

@pytest.mark.users
@pytest.mark.regression
@pytest.mark.parametrize('email', [
    'mail.ru',
    'gmail.com',
    'example.com'
])
def test_create_user(email: str, public_users_client: PublicUsersClient):
    create_user_request = CreateUserRequestSchema(email=fake.email(email))
    create_user_response = public_users_client.create_user_api(create_user_request)
    create_user_response_data = CreateUserResponseSchema.model_validate_json(create_user_response.text)

    assert_status_code(create_user_response.status_code, HTTPStatus.OK)
    assert_create_user_response(create_user_request, create_user_response_data)

    validate_json_schema(create_user_response.json(), create_user_response_data.model_json_schema())


@pytest.mark.users
@pytest.mark.regression
def test_get_users_me(function_user: UserFixture, private_users_client: PrivateUsersClient):
    response = private_users_client.get_users_me_api()
    response_data = GetUserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_get_user_response(response_data, function_user.response)

    validate_json_schema(response.json(), response_data.model_json_schema())