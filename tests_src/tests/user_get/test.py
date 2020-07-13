import random
import string
import pytest

from tests_src.core import CoreTests
from tests_src.libs.user_lib import remove_all_users, add_user, remove_user


class TestUserGet(CoreTests):
    def setup_class(cls):
        remove_all_users()
        cls.users = []

    def teardown_class(cls):
        remove_all_users()

    @pytest.fixture(scope='class', autouse=True)
    def fixture_generate_and_add_user(self):
        for i in range(10):
            name = ''.join(
                random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randrange(1, 50)))
            surname = ''.join(
                random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randrange(1, 50)))
            user_dict = {'name': name.title(), 'surname': surname.title()}
            add_user(user_dict)
            self.users.append(user_dict)

    def test_user_get(self):
        response = self.http_req('/get', {'user_id': 5})
        self.assert_equal(response['status'], 200, '/get status_code')
        self.assert_equal(response['body'], self.users[4], '/get response.', regexp=True)

    def test_user_get_after_remove(self):
        remove_user(3)
        response = self.http_req('/get', {'user_id': 3})
        self.assert_equal(response['status'], 400, '/get status_code')
        self.assert_equal(response['body'], 'invalid user id', '/get response.', regexp=True)

    @pytest.mark.parametrize(('name', 'params', 'expected_response'), [
        ('unknown_user_id', {'user_id': 123214}, 'invalid user id'),
        ('float_user_id', {'user_id': 1.2}, 'invalid user id'),
        ('missed_user_id', {}, 'missing parameter: user_id'),
        ('empty_user_id', {'user_id': ''}, 'invalid user id'),
        ('zero_user_id', {'user_id': 0}, 'invalid user id'),
        ('negative_id', {'user_id': -1}, 'invalid user id'),
        ('empty_list_id', {'user_id': '[]'}, 'invalid user id'),
        ('empty_dict_id', {'user_id': '{}'}, 'invalid user id'),
        ('empty_tuple_id', {'user_id': '()'}, 'invalid user id'),
        ('not_empty_list_id', {'user_id': '[1]'}, 'invalid user id'),
        ('not_empty_dict_id', {'user_id': '{"id": "1"}'}, 'invalid user id'),
        ('not_empty_tuple_id', {'user_id': '(1)'}, 'invalid user id'),
        ('boolean_user_id', {'user_id': 'True'}, 'invalid user id'),
    ])
    def test_user_get_negative(self, name, params, expected_response):
        response = self.http_req('/get', params)
        self.assert_equal(response['status'], 400, '/get status_code')
        self.assert_equal(response['body'], expected_response, '/get response.', regexp=True)
