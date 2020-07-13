from tests_src.core import CoreTests as ct


def remove_all_users():
    response = ct.http_req('/remove/all', {})
    if response['status'] != 200:
        raise RuntimeError(f'Failed to remove all users. Response text is {response}')
    return response


def get_user(user_id):
    response = ct.http_req('/get', {'user_id': user_id})
    if response['status'] != 200:
        raise RuntimeError(f'Failed to get user. Response text is {response}')
    return response

def remove_user(user_id):
    response = ct.http_req('/remove', {'user_id': user_id})
    if response['status'] != 200:
        raise RuntimeError(f'Failed to remove user. Response text is {response}')
    return response


def add_user(params):
    response = ct.http_req('/add', params)
    if response['status'] != 200:
        raise RuntimeError(f'Failed to add user. Response text is {response}')
    return response
