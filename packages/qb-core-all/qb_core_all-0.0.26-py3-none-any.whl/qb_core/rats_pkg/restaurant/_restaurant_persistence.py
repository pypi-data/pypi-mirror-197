import json

from qb_core.rats_pkg.restaurant.restaurant_model import Restaurant

RESTAURANT_DICT = {}


def read_restaurant_count():
    return len(RESTAURANT_DICT)


def read_restaurant(restaurant_name):
    return RESTAURANT_DICT.get(restaurant_name)


def read_restaurant_by_manager_email(manager_email):
    # for now do this the hard way, loop through data.
    # when you write actual persistence you can index this appropriately
    for restaurant in RESTAURANT_DICT.values():
        if restaurant.manager_email == manager_email:
            return restaurant
    return None


def save_restaurant(restaurant):
    RESTAURANT_DICT[restaurant.name] = restaurant


def print_all():
    print(f'{json.dumps(RESTAURANT_DICT, default=str)=}')

