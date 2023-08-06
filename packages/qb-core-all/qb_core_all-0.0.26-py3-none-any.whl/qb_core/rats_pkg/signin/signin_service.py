from qb_core.rats_pkg.signin import _signin_persistence

ACTOR_RESTAURANT_MANAGER = "restaurant_manager"
ACTOR_CUSTOMER = "customer"
ACTOR_COOK = "cook"
ACTOR_DRIVER = "driver"


def signup(actor, email, password):
    return _signin_persistence.register_user(actor, email, password)


def signin(actor, email, password):
    return _signin_persistence.authenticate_user(actor, email, password)
