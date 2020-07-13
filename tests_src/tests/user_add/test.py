import pytest

from tests_src.core import CoreTests
from tests_src.libs.user_lib import remove_all_users, get_user, remove_user


class TestUserAdd(CoreTests):
    def setup_class(cls):
        remove_all_users()

    def teardown_class(cls):
        remove_all_users()

    @pytest.mark.parametrize(('name', 'params', 'expected_response'), [
        ('simple_user',
         {'name': 'John', 'surname': 'Smith'},
         {'name': 'John', 'surname': 'Smith', 'user_id': int}),
        ('lower_name',
         {'name': 'john', 'surname': 'Smith'},
         {'name': 'John', 'surname': 'Smith', 'user_id': int}),
        ('lower_surname',
         {'name': 'John', 'surname': 'smith'},
         {'name': 'John', 'surname': 'Smith', 'user_id': int}),
        ('short_name',
         {'name': 'j', 'surname': 'Smith'},
         {'name': 'J', 'surname': 'Smith', 'user_id': int}),
        ('short_surname',
         {'name': 'John', 'surname': 's'},
         {'name': 'John', 'surname': 'S', 'user_id': int}),
        ('long_name',
         {'name': 'j' * 50, 'surname': 'Smith'},
         {'name': 'J' + 'j' * 49, 'surname': 'Smith', 'user_id': int}),
        ('long_surname',
         {'name': 'John', 'surname': 's' * 50},
         {'name': 'John', 'surname': 'S' + 's' * 49, 'user_id': int}),
        ('different_case_name',
         {'name': 'jOhN', 'surname': 'Smith'},
         {'name': 'John', 'surname': 'Smith', 'user_id': int}),
        ('different_case_surname',
         {'name': 'John', 'surname': 'sMItH'},
         {'name': 'John', 'surname': 'Smith', 'user_id': int}),
        ('name_with_spaces',
         {'name': ' John    ', 'surname': 'Smith'},
         {'name': 'John', 'surname': 'Smith', 'user_id': int}),
        ('surname_with_spaces',
         {'name': 'John', 'surname': '    Smith  '},
         {'name': 'John', 'surname': 'Smith', 'user_id': int}),
        ('cyrillic_name',
         {'name': 'Вова', 'surname': 'Smith'},
         {'name': 'Вова', 'surname': 'Smith', 'user_id': int}),
        ('cyrillic_surname',
         {'name': 'John', 'surname': 'Иванов'},
         {'name': 'John', 'surname': 'Иванов', 'user_id': int}),
        # ('second_test'),
    ])
    def test_user_add(self, name, params, expected_response):
        response = self.http_req('/add', params)
        self.assert_equal(response['status'], 200, '/add status_code')
        self.assert_equal(response['body'], expected_response, '/add response.', regexp=True)
        get_resp = get_user(response['body']['user_id'])
        expected_response.pop('user_id')
        self.assert_equal(get_resp['body'], expected_response, '/get response.', regexp=True)

    def test_add_user_after_remove(self):
        users_ids = []
        for surname in ['First', 'Second', 'Third']:
            response = self.http_req('/add', {'name': 'John', 'surname': surname})
            self.assert_equal(response['status'], 200, '/add status_code')
            users_ids.append(response['body']['user_id'])

        remove_user(users_ids[1])
        second_response = self.http_req('/add', {'name': 'John', 'surname': 'Last'})
        self.assert_equal(second_response['status'], 200, '/add status_code')
        self.assert_equal(second_response['body'],
                          {'name': 'John', 'surname': 'Last', 'user_id': users_ids[-1] + 1},
                          '/add response.', regexp=True)

    def test_add_user_on_deleted_position(self):
        users_ids = []
        for surname in ['First', 'Second', 'Third']:
            response = self.http_req('/add', {'name': 'John', 'surname': surname})
            self.assert_equal(response['status'], 200, '/add status_code')
            users_ids.append(response['body']['user_id'])

        remove_user(users_ids[-1])
        second_response = self.http_req('/add', {'name': 'John', 'surname': 'Last'})
        self.assert_equal(second_response['status'], 200, '/add status_code')
        self.assert_equal(second_response['body'],
                          {'name': 'John', 'surname': 'Last', 'user_id': users_ids[-1]},
                          '/add response.', regexp=True)

    @pytest.mark.parametrize(('name', 'params', 'expected_response'), [
        ('empty_user', {'name': '', 'surname': ''}, 'invalid parameter'),
        ('empty_name', {'name': '', 'surname': 'Smith'}, 'invalid parameter'),
        ('empty_surname', {'name': 'John', 'surname': ''}, 'invalid parameter'),
        ('name_with_spaces', {'name': 'J oh n', 'surname': 'Smith'}, 'invalid parameter'),
        ('surname_with_spaces', {'name': 'John', 'surname': 'S mi   th'}, 'invalid parameter'),
        ('missed_name', {'surname': 'Smith'}, 'missing parameter'),
        ('missed_surname', {'name': 'John'}, 'missing parameter'),
        ('without_surname', {}, 'missing parameter'),
        ('to_long_name', {'name': 'j' * 51, 'surname': 'Smith'}, 'invalid parameter'),
        ('to_long_surname', {'name': 'John', 'surname': 's' * 51}, 'invalid parameter'),
        ('name_with_int', {'name': 'Jo1hn', 'surname': 'Smith'}, 'invalid parameter'),
        ('surname_with_int', {'name': 'John', 'surname': 'Smi2th'}, 'invalid parameter'),
        ('int_name', {'name': '123', 'surname': 'Smith'}, 'invalid parameter'),
        ('int_surname', {'name': 'John', 'surname': '123'}, 'invalid parameter'),
        ('empty_[]_name', {'name': '[]', 'surname': 'Smith'}, 'invalid parameter'),
        ('empty_[]_surname', {'name': 'John', 'surname': '[]'}, 'invalid parameter'),
        ('empty_{}_name', {'name': '{}', 'surname': 'Smith'}, 'invalid parameter'),
        ('empty_{}_surname', {'name': 'John', 'surname': '{}'}, 'invalid parameter'),
        ('empty_()_name', {'name': '()', 'surname': 'Smith'}, 'invalid parameter'),
        ('empty_()_surname', {'name': 'John', 'surname': '())'}, 'invalid parameter'),
        ('not_empty_[]_name', {'name': '["John"]', 'surname': 'Smith'}, 'invalid parameter'),
        ('not_empty_[]_surname', {'name': 'John', 'surname': '["Smith"]'}, 'invalid parameter'),
        ('not_empty_{}_name', {'name': '{"name": "John"}', 'surname': 'Smith'}, 'invalid parameter'),
        ('not_empty_{}_surname', {'name': 'John', 'surname': '{"surname": "Smith"}'}, 'invalid parameter'),
        ('not_empty_()_name', {'name': '("John")', 'surname': 'Smith'}, 'invalid parameter'),
        ('not_empty_()_surname', {'name': 'John', 'surname': '("Smith"))'}, 'invalid parameter'),
        ('name_sql_injection', {'name': 'John\'', 'surname': 'Smith'}, 'invalid parameter'),
        ('surname_sql_injection', {'name': 'John', 'surname': 'Smith\''}, 'invalid parameter'),
    ])
    def test_user_add_negative(self, name, params, expected_response):
        response = self.http_req('/add', params)
        self.assert_equal(response['status'], 400, '/add status_code')
        self.assert_equal(response['body'], expected_response, '/add response.', regexp=True)
