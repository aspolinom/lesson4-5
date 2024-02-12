from lib.my_requests import MyRequests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
@allure.epic("Registration cases")
class TestUserRegister(BaseCase):

    @allure.description("This test succesfully regisration user by prepare_registration_data")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/",data=data)

        Assertions.assert_code_status(response,200)
        Assertions.assert_json_has_key(response,"id")

    @allure.description("This test regisration user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

