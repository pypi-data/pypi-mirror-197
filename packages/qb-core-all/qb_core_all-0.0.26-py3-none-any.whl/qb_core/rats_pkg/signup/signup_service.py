from random import randrange

from qb_core.rats_pkg.signup import _signup_persistence


def generate_code():
    r1 = randrange(10)
    r2 = randrange(10)
    r3 = randrange(10)
    r4 = randrange(10)
    r5 = randrange(10)
    r6 = randrange(10)
    r = str(r1) + str(r2) + str(r3) + str(r4) + str(r5) + str(r6)
    return r


def send_verification_email(email, tag):
    code = generate_code()
    # NICE_TODO Feature - Security send email
    print(f'TODO send email to {email}')
    print(f'TODO persist state {code=}, {tag=}')
    key = make_key(email, tag)
    _signup_persistence.save_code(key, code)
    state = "pending_verification"
    return code, state


def verify(email, tag, code):
    key = make_key(email, tag)
    if _signup_persistence.read_code(key) == code:
        state = "verified"
    else:
        state = "error"
    return state, "invalid key"


def make_key(email, tag):
    return f'{email=}#{tag=}'


def _get_verification_code(email, tag):
    key = make_key(email, tag)
    return _signup_persistence.read_code(key)
