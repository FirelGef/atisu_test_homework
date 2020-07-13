import pytest
import configparser


def pytest_addoption(parser):
    """
    Метод добавляет кастомные ключи в запуск тестов
    """
    parser.addoption('--method', action='store', default='get')


def edit_parser(list_of_fields):
    """
    Метод для замены значений в simple_config.ini
    """
    parser = configparser.ConfigParser()

    parser.read('simple_config.ini')

    for section, field, value in list_of_fields:
        parser.set(section, field, value)
        with open('simple_config.ini', 'w') as configfile:
            parser.write(configfile)


@pytest.fixture(scope='session', autouse=True)
def request_method(request):
    """
    Выбор метода в зависимости от ключа "--method" default=get
    :return: requests.%method%
    """
    method = request.config.getoption('--method')
    edit_parser([('request', 'method', method.lower())])

    def fin():
        edit_parser([('request', 'method', 'get')])

    request.addfinalizer(fin)

