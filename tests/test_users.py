from http import HTTPStatus

from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.assertions.schema import validate_json_schema
from tools.assertions.base import assert_status_code
from tools.assertions.users import assert_create_user_response


def test_create_user():
    public_users_client =get_public_users_client()

    create_user_request = CreateUserRequestSchema()
    create_user_response = public_users_client.create_users_api(create_user_request)
    create_user_response_data = CreateUserResponseSchema.model_validate_json(create_user_response.text)

    assert_status_code(create_user_response.status_code, HTTPStatus.OK)
    assert_create_user_response(create_user_request, create_user_response_data)

    validate_json_schema(create_user_response.json(), create_user_response_data.model_json_schema())

