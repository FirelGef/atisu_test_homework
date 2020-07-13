import random
import string

import pytest

from tests_src.core import CoreTests
from tests_src.libs.user_lib import remove_all_users, add_user


class TestUserRemove(CoreTests):
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
            add_resp = add_user(user_dict)
            user_dict['user_id'] = add_resp['body']['user_id']
            self.users.append(user_dict)

    def test_user_remove(self):
        response = self.http_req('/remove', {'user_id': 5})
        self.assert_equal(response['status'], 200, '/remove status_code')
        self.assert_equal(response['body'], self.users[4], '/remove response.', regexp=True)
        response = self.http_req('/get', {'user_id': 5})
        self.assert_equal(response['status'], 400, '/get status_code')
        self.assert_equal(response['body'], 'invalid user id', '/get response.', regexp=True)

    def test_user_remove_after_remove(self):
        response = self.http_req('/remove', {'user_id': 6})
        self.assert_equal(response['status'], 200, '/remove status_code')
        self.assert_equal(response['body'], self.users[4], '/remove response.', regexp=True)
        response = self.http_req('/remove', {'user_id': 5})
        self.assert_equal(response['status'], 400, '/remove status_code')
        self.assert_equal(response['body'], 'invalid user id', '/remove response.', regexp=True)


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
        ('boolean_user_id', {'user_id': True}, 'invalid user id'),
    ])
    def test_user_remove_negative(self, name, params, expected_response):
        response = self.http_req('/remove', params)
        self.assert_equal(response['status'], 400, '/remove status_code')
        self.assert_equal(response['body'], expected_response, '/remove response.', regexp=True)
