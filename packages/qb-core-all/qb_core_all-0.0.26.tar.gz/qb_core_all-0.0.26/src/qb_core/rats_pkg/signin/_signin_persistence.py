from collections import defaultdict
from random import randrange

from qb_core.rats_pkg.signin.secure_context import SecureToken

SIGNIN_DICT = None
SIGNIN_SESSION = None


def clear_all():
    global SIGNIN_DICT
    SIGNIN_DICT = defaultdict(dict)
    global SIGNIN_SESSION
    SIGNIN_SESSION = defaultdict(list)


def authenticate_user(actor, email, password):
    secure_token = None
    if SIGNIN_DICT[actor].get(email) == password:
        secure_token = SecureToken()
        secure_token.email = email
        secure_token.access_token = generate_token()
        secure_token.refresh_token = generate_token()
        # NICE_TODO Feature - Security set this to a proper time 5 minutes
        secure_token.access_token_expires_at = 5 * 60
        # NICE_TODO Feature - Security set this to a proper time 30 minutes
        secure_token.refresh_token_expires_at = 30 * 60
        # only one session per user/email
        SIGNIN_SESSION[email] = secure_token
    return secure_token


def register_user(actor, email, password):
    # print(f'{actor=}, {email=}')
    SIGNIN_DICT[actor][email] = password
    # print('done adding stuff')
    return "success", f'signed-up {actor=}, {email=}'


# hey, lets not get into the habit of printing sensitive info
# so turn this off
# WARNING never turn this ON
# def print_all():
#     print(f'{SIGNIN_DICT=}')


def generate_token():
    r1 = randrange(10)
    r2 = randrange(10)
    r3 = randrange(10)
    r4 = randrange(10)
    r5 = randrange(10)
    r6 = randrange(10)
    r7 = randrange(10)
    r8 = randrange(10)
    r9 = randrange(10)
    r = str(r1) + str(r2) + str(r3) + str(r4) + str(r5) + str(r6) + str(r7) + str(r8) + str(r9)
    return r


clear_all()
