"""
this module has everything needed to represent Restaurant entity
this is similar to service object in spring boot

"""
# TODO figure how to wire this so that AWS flavor of the app can use DyanamoDB
from qb_core.rats_pkg.restaurant import _restaurant_persistence
from qb_core.rats_pkg.restaurant.restaurant_model import Restaurant


def does_restaurant_exist(name):
    r = _restaurant_persistence.read_restaurant(name)
    return r is not None


def create_restaurant(manager_name, manager_email, restaurant_name):
    r = Restaurant()
    r.init(manager_name=manager_name, manager_email=manager_email, name=restaurant_name)
    return r


def read_restaurant(restaurant_name):
    r = _restaurant_persistence.read_restaurant(restaurant_name)
    return r


def read_restaurant_by_manager_email(manager_email):
    r = _restaurant_persistence.read_restaurant_by_manager_email(manager_email)
    return r


def save_restaurant(restaurant):
    _restaurant_persistence.save_restaurant(restaurant)
