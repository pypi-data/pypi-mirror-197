SIGNUP_DICT = {}


def clear_all():
    SIGNIN_DICT = {}
    SIGNIN_SESSION = {}


def read_code(key):
    return SIGNUP_DICT.get(key)


def save_code(key, code):
    SIGNUP_DICT[key] = code


# hey, lets not get into the habit of printing sensitive info
# so turn this off
# WARNING never turn this ON
# def print_all():
#     print(f'{SIGNUP_DICT=}')
