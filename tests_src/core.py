import re
import requests
import configparser
from prettytable import PrettyTable

pettytb = []
method_name = dict(
        get=requests.get,
        post=requests.post
    )

class CoreTests:
    def assert_reg_dict_equal(self, actual, expected):
        assert sorted(actual.keys()) == sorted(expected.keys()), f'dict keys not equal. {actual} != {expected}'
        for key in actual.keys():
            assert_result = self.assert_regexp_equal(actual[key], expected[key])
            if not assert_result:
                pettytb.append((f'{key}: {type(actual[key])}{actual[key]}', f'{key}: {type(expected[key])}{expected[key]}'))

    def assert_equal(self, actual, expected, msg='', regexp=False):
        if regexp:
            if type(actual) == dict:
                self.assert_reg_dict_equal(actual, expected)
            elif type(actual) == list:
                self.assert_reg_lists_equal(actual, expected, msg)
            else:
                self.assert_regexp_equal(actual, expected)
        else:
            if actual != expected:
                pettytb.append((f'{type(actual)}{actual}', f'{type(expected)}{expected}'))

        table = self.generate_petty_table()
        if table:
            print(msg, '\n')
            raise AssertionError(table)

    def assert_regexp_equal(self, actual, expected):
        exp_types = [str, int]
        if expected not in exp_types:
            assert_result = re.match('^'+str(expected)+'$', str(actual))
            if not assert_result:
                pettytb.append((f'{type(actual)}{actual}', f'{type(expected)}{expected}'))
                return False
            return True
        else:
            assert_result = type(actual) == expected
            if not assert_result:
                pettytb.append((f'{type(actual)}{actual}', f'{expected}'))
                return False
            return True

    def generate_petty_table(self):
        if pettytb:
            table = PrettyTable(["actual", "expected"])
            for act, exp in pettytb:
                table.add_row([act, exp])

            return table

    @staticmethod
    def http_req(endpoint, params):
        parser = configparser.ConfigParser()
        parser.read('simple_config.ini')

        request_method = parser.get('request', 'method')
        request_scheme = parser.get('request', 'scheme')
        request_host = parser.get('request', 'host')
        request_port = parser.get('request', 'port')

        response = method_name[request_method](f'{request_scheme}://{request_host}:{request_port}{endpoint}', params)
        if response.status_code != 200:
            raise RuntimeError(f'/{endpoint}.response.status_code: {response.status_code}')

        return response.json()
