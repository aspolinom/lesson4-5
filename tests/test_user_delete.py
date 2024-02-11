import requests
import time
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):
    def test_delete_known_user(self):
       #LOGIN
       data = {
           'email': 'vinkotov@example.com',
           'password': '1234'
       }
       response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)

       auth_sid = self.get_cookie(response1, "auth_sid")
       token = self.get_headers(response1, "x-csrf-token")
       user_id = self.get_json_value(response1,"user_id")

       #DELETE

       response3 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
       )

       Assertions.assert_code_status( response3,400)
       assert response3.content.decode('utf-8') == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.',"You try delete protected users       "

    def test_delete_just_created_user(self):
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

        #DELETE

        response3 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}

        )

        Assertions.assert_code_status(response3,200)

        #GET
        response4 = response3 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response4,404)
        assert response3.content.decode('utf-8') == 'User not found', f"You delete users '{user_id}'"

    def test_delete_other_user(self):
        register_data = self.prepare_registration_data()
        name_begin = 'first'
        register_data['username'] = 'first'
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1,"id")

        user_id1 = self.get_json_value(response1,'id')

        #NEW USER
        time.sleep(5)
        register_data = self.prepare_registration_data()
        register_data['username'] = 'second'
        response2 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        user_id2 = self.get_json_value(response2,'id')

        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }

        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_headers(response3, "x-csrf-token")

        Assertions.assert_code_status(response3, 200)

        response4 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id1}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4,200)

        #GET
        response5 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id1}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response5,200)
        assert response5.content.decode('utf-8') != 'User not found', f"You delete users '{user_id1}'"


