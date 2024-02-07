import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegNegative(BaseCase):
    k=1
    exclude_params = [
        {'username': 'learnqa','firstName': 'learnqa',
            'lastName': 'learnqa', 'email': "vinkotov@example.com"
        },
        {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa',
         'lastName': 'learnqa'
         },
        {'password': '123',  'firstName': 'learnqa',
         'lastName': 'learnqa', 'email': "vinkotov@example.com"
         },
        {'password': '123', 'username': 'learnqa',
         'lastName': 'learnqa', 'email': "vinkotov@example.com"
         },
        {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa',
         'email': "vinkotov@example.com"
         },
    ]
    def test_creat_user_without_dog(self):
        email = 'without_dog'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode('utf-8') == f'Invalid email format', {response.content}

    def test_creat_user_one_symbol(self):

        data = {
            'password': '123',
            'username': 'l',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email':'vinkotov@example.com'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode('utf-8') == f"The value of 'username' field is too short", {response.content}
    def test_creat_user_long_name(self):
        long_str = "qwertyuiopasdfghjklzxcvbnm\
                    qwertyuiopasdfghjklzxcvbnm\
                    qwertyuiopasdfghjklzxcvbnm \
                    qwertyuiopasdfghjklzxcvbnm\
                    qwertyuiopasdfghjklzxcvbnm\
                    qwertyuiopasdfghjklzxcvbnm\
                    qwertyuiopasdfghjklzxcvbnm\
                    qwertyuiopasdfghjklzxcvbnm\
                    qwertyuiopasdfghjklzxcvbnm\
                    qwertyuiopasdfghjklzxcvbnm"

        data = {
            'password': '123',
            'username': long_str,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email':'vinkotov@example.com'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode('utf-8') == f"The value of 'username' field is too long", {response.content}

    @pytest.mark.parametrize('condition', exclude_params)
    def test_creat_user_without_param(self,condition):
            response = requests.post("https://playground.learnqa.ru/api/user/", data=condition)

            assert response.status_code == 400, f"Unexpected status code {response.status_code}"
            if 'password' not in condition:
                assert response.content.decode('utf-8') == f'The following required params are missed: password',{response.content}
            elif 'username' not in condition:
                assert response.content.decode('utf-8') == f'The following required params are missed: username', {
                    response.content}
            elif 'firstName' not in condition:
                assert response.content.decode('utf-8') == f'The following required params are missed: firstName', {
                    response.content}
            elif 'lastName' not in condition:
                assert response.content.decode('utf-8') == f'The following required params are missed: lastName', {
                    response.content}
            elif 'email' not in condition:
                assert response.content.decode('utf-8') == f'The following required params are missed: email', {
                    response.content}


"""
            assert response.content.decode('utf-8') == f'The following required params are missed: username', {response.content}
            assert response.content.decode('utf-8') == f'The following required params are missed: firstname', {response.content}
"""

