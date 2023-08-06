"""
rats.py
this follows interactor pattern.
implements both command executor and event listener

notes:
    this is the interactor Bob Martin talks about
    TODO revisit this after you build core and infrastructure (or domain/infrastructure)
    I will implement two flavors of interactor: command executor and event listener
    for now both flavors will be here
"""
from qb_core.common.plugin.plugin_manager import PluginManager
from qb_core.rats_pkg.cook import cook_entity
from qb_core.rats_pkg.cook.cook_model import Cook, CookAdded, CookRemoved
from qb_core.rats_pkg.plug_point_config import core_rats_plug_point_configuration
from qb_core.rats_pkg.signin import signin_service
from qb_core.rats_pkg.signup import signup_service
from qb_core.rats_pkg.restaurant import restaurant_entity
from qb_core.event_bus import event_bus_core, event_bus_events


def initialize_module():
    print(f'initializing rats module')
    PluginManager.setup_core_plugins(core_rats_plug_point_configuration)

    event_bus_core.register_emitter(event_bus_events.EVENT_COOK_ADDED, None)
    event_bus_core.register_emitter(event_bus_events.EVENT_MENU_UPLOADED, None)
    print(f'*** REGISTERING listener None added for event restaurant_rated')
    event_bus_core.register_listener(event_bus_events.EVENT_RESTAURANT_RATED, None)


def signup_initiate(manager_name, manager_email, restaurant_name):
    # ensure manager_name, manager_email, restaurant_name is not empty
    exists = restaurant_entity.does_restaurant_exist(restaurant_name)
    if exists:
        return "error", "restaurant already signed up"

    restaurant = restaurant_entity.create_restaurant(manager_name, manager_email, restaurant_name)
    verification_code, state = signup_service.send_verification_email(manager_email, f'{restaurant_name=}')
    restaurant.status = state
    restaurant_entity.save_restaurant(restaurant)

    return "success", "restaurant signup initiated"


def signup_verify(manager_email, restaurant_name, code):
    # ensure manager_name, manager_email, restaurant_name is not empty
    restaurant = restaurant_entity.read_restaurant(restaurant_name)
    if restaurant is None:
        return "error", f'invalid {restaurant_name=}'

    result, message = signup_service.verify(manager_email, f'{restaurant_name=}', code)
    if result == "error":
        return result, message

    restaurant.status = result
    restaurant_entity.save_restaurant(restaurant)
    return "success", "restaurant signup verified"


# WARNING: do not expose this to clients e.g. don't expose this as API end points or even
# lambdas.
# provided this to help write low-level tests
def _signup_get_verification_code(manager_email, restaurant_name):
    return signup_service._get_verification_code(manager_email, f'{restaurant_name=}')


def signup_complete(restaurant_name, address, cuisine_type):
    # ensure manager_name, manager_email, restaurant_name is not empty
    restaurant = restaurant_entity.read_restaurant(restaurant_name)
    if restaurant is None:
        return "error", f'invalid {restaurant_name=}'

    restaurant.address = address
    restaurant.cuisine_type = cuisine_type
    restaurant.status = "signed-up"
    restaurant_entity.save_restaurant(restaurant)
    return "success", "restaurant signed-up"


def signup(manager_email, password):
    return signin_service.signup(signin_service.ACTOR_RESTAURANT_MANAGER, manager_email, password)


def signin(manager_email, password):
    return signin_service.signin(signin_service.ACTOR_RESTAURANT_MANAGER, manager_email, password)


def add_cook(secure_token, cook_name, cook_email):
    # like anything else, do security checks first!
    # TODO Feature - Security verify security token

    restaurant = restaurant_entity.read_restaurant_by_manager_email(secure_token.email)

    # cook related functions
    cook = Cook()
    cook.init(name=cook_name, email=cook_email)
    cook_entity.add_cook(cook)

    # tie cook to the restaurant
    restaurant.cook_dict[cook.name] = cook
    restaurant_entity.save_restaurant(restaurant)

    # also, this is the place to do any cross-validations between different entities

    # this should be the last step so that we send this event exactly once
    # when all the steps above have completed
    event_bus_core.emit_event(event_bus_events.EVENT_COOK_ADDED, CookAdded(cook))
    return cook


def remove_cook(secure_token, cook):
    restaurant = restaurant_entity.read_restaurant_by_manager_email(secure_token.email)
    restaurant.cook_dict.pop(cook.email, None)
    restaurant_entity.save_restaurant(restaurant)
    cook_entity.remove_cook(cook)

    # this should be the last step so that we send this event exactly once
    # when all the steps above have completed
    event_bus_core.emit_event("cook_removed", CookRemoved(cook))


def upload_menu():
    pass


def view_order_status():
    return {
        "OrderA": {
            "id": "1001",
            "items": "1"
        },
        "OrderB": {
            "id": "1002",
            "items": "2"
        },
        "OrderC": {
            "id": "1003",
            "items": "3"
        },
    }


def restaurant_rated():
    pass
