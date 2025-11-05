import pytest
import allure

from http import HTTPStatus

from allure_commons.types import Severity

from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from fixtures.users import UserFixture
from tools.assertions.schema import validate_json_schema
from tools.assertions.base import assert_status_code
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.fakers import fake
from tools.allure.tags import AllureTag
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory


@pytest.mark.users
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.USERS)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.USERS)
class TestUsers:
    @allure.title('Create user')
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @pytest.mark.parametrize('email_domain', ['mail.ru', 'gmail.com', 'example.com'])
    def test_create_user(self, email_domain: str, public_users_client: PublicUsersClient):
        create_user_request = CreateUserRequestSchema(email=fake.email(email_domain))
        create_user_response = public_users_client.create_user_api(create_user_request)
        create_user_response_data = CreateUserResponseSchema.model_validate_json(create_user_response.text)

        assert_status_code(create_user_response.status_code, HTTPStatus.OK)
        assert_create_user_response(create_user_request, create_user_response_data)

        validate_json_schema(create_user_response.json(), create_user_response_data.model_json_schema())

    @allure.title('Get user me')
    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    def test_get_user_me(self, function_user: UserFixture, private_users_client: PrivateUsersClient):
        response = private_users_client.get_user_me_api()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data, function_user.response)

        validate_json_schema(response.json(), response_data.model_json_schema())