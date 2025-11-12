from dataclasses import field

import pytest
import allure

from http import HTTPStatus

from allure_commons.types import Severity
from pydantic import EmailStr

from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema, \
    UpdateUserRequestSchema, UpdateUserResponseSchema, CreateUserInvalidRequestSchema
from fixtures.users import UserFixture
from tools.assertions.schema import validate_json_schema
from tools.assertions.base import assert_status_code
from tools.assertions.users import assert_create_user_response, assert_get_user_response, assert_update_user_response, \
    assert_user_not_found_response, logger, assert_check_create_user_with_invalid_email_response, \
    assert_create_user_with_empty_response
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

    @allure.title('Get user')
    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    def test_get_user(self, function_user: UserFixture, private_users_client: PrivateUsersClient):
        response = private_users_client.get_users_api(function_user.response.user.id)
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data, function_user.response)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title('Update user')
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @pytest.mark.parametrize(
        'email, first_name, middle_name, last_name',
        [
            (fake.email(), fake.first_name(), fake.middle_name(), fake.last_name()),
            (fake.email(), None, None, None),
            (None, fake.first_name(), None, None),
            (None, None, fake.middle_name(), None),
            (None, None, None, fake.last_name())
        ]
    )
    def test_update_user(
            self,
            function_user: UserFixture,
            private_users_client: PrivateUsersClient,
            email: EmailStr,
            first_name: str,
            middle_name: str,
            last_name: str
    ):
        request = UpdateUserRequestSchema(
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name
        )
        response = private_users_client.update_user_api(function_user.response.user.id, request)
        response_data = UpdateUserResponseSchema.model_validate_json(response.text)
        logger.info(response_data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_user_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title('Delete user')
    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    def test_delete_user(self, function_user: UserFixture, private_users_client: PrivateUsersClient):
        delete_response = private_users_client.delete_user_api(function_user.response.user.id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = private_users_client.get_users_api(function_user.response.user.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_user_not_found_response(get_response_data)

        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

    @allure.title('Create user with incorrect email')
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_user_with_invalid_email(self, public_users_client: PublicUsersClient):
        request = CreateUserInvalidRequestSchema(email=fake.text())
        response = public_users_client.create_user_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_check_create_user_with_invalid_email_response(response_data, request)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title('Create user with empty first name')
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_user_with_empty_firstname(self, public_users_client: PublicUsersClient):
        request = CreateUserRequestSchema(first_name='')
        response = public_users_client.create_user_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_user_with_empty_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())
