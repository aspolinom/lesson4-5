import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        #REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1,"id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1,'id')

        #LOGIN
        login_data = {
            'email':email,
            'password':password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed Name"

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName":new_name}
        )

        Assertions.assert_code_status(response3,200)

        #GET
        response4 = response3 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_not_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        email = register_data['email']
        first_name = register_data['firstName']
        password = "12345"
        user_id = 2

        # LOGIN
        login_data = {
           'email': email,
           'password': password
           }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        Assertions.assert_code_status(response2, 400)

    def test_edit_correct_data_another_user(self):
        #REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1,"id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1,'id')

        #LOGIN
        login_data = {
            'email':email,
            'password':password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed Name"

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/2",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName":new_name}
        )

        #GET
        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/2",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid})
        print(response4.content)


        Assertions.assert_code_status(response4,200)
        Assertions.assert_json_has_not_key(
            response4,
            "firstName"
        )

    def test_edit_user_bad_email(self):
        #REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1,"id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1,'id')

        #LOGIN
        email.replace("@",'2')
        em1=email[0:-13]+email[-11:-1]
        login_data = {
            'email':email,
            'password':password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        #EDIT
        new_name = em1

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/2",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"email":new_name}
        )

        #GET
        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/2",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response4,200)
        Assertions.assert_json_has_not_key(
            response4,
            "email"
        )
    def test_edit_created_user_short_name(self):
        #REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1,"id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1,'id')

        #LOGIN
        login_data = {
            'email':email,
            'password':password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        #EDIT
        new_name = "C"

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName":new_name}
        )

        Assertions.assert_code_status(response3,400)

        #GET
        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            "learnqa",
            "Wrong name of the user after edit"
        )


