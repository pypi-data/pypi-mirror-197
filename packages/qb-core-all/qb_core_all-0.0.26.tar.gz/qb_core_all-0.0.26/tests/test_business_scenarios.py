"""
test_business_scenarios.py
use this module to test everything. not just unit tests but the whole app.
Why is this good
 * the whole app can run locally in a single process

TODO
 * Make sure each test is independent of the other.
"""
import asyncio
from datetime import datetime

import pytest

import core_main
from qb_core.common.plugin.plugin_manager import PluginManager
from qb_core.event_bus.event_bus_interface import EventBusInterface
from qb_core.ocra_pkg import ocra
from qb_core.oproc_pkg import oproc
from qb_core.rats_pkg import rats
from qb_core.rats_pkg.cook.cook_persistence_core import CookPersistenceCore
from qb_core.rats_pkg.cook import cook_persistence_core
from qb_core.rats_pkg.restaurant import _restaurant_persistence
from qb_core.rats_pkg.signin import _signin_persistence
from qb_core.rats_pkg.signup import _signup_persistence

print("lets test as we code")

"""
* this is the period the main thread pauses, typically after performing steps that
trigger an event. 
* by sleeping for this wait period we give asyncio opportunity to kick of listener
and the listner to complete it's steps.
* since we do in memory options in core, listener should take very short time 
* if listeners take longer increase this. 

* core event bus uses asyncio. it looks like ayncio works on 
one thread at a time (TODO is this right? research it, say print thread info)  
"""
PAUSE_PERIOD = 0.1

# _cook_persistence = CookPersistenceCore()
_cook_persistence = None


# NOTE: this test needs to be the first test as it initializes the app
@pytest.mark.asyncio
async def test_signup_happy_path_italian():
    core_main.initialize_app()
    global _cook_persistence
    _cook_persistence = PluginManager.get_plugin("cook_persistence_plug_point")

    _restaurant_persistence.print_all()
    manager_name = "Vinny Gambini"
    manager_email = "vinny@unreal.com"
    manager_password = "secret"
    restaurant_name = "Siciliano Ristorante"
    restaurant_address = "1 Pizza Way"
    restaurant_cuisine_type = "Italian"
    cooks = {
        "giada": {"name": "Giada De Laurentiis", "email": "gdl@unreal.com", "password": "secret"},
        "fabio": {"name": "Fabio Viviani", "email": "fabio@unreal.com", "password": "secret"}
    }
    result, message = rats.signup_initiate(manager_name, manager_email, restaurant_name)
    assert result == "success"
    assert message == "restaurant signup initiated"

    verification_code = rats._signup_get_verification_code(manager_email, restaurant_name)
    result, message = rats.signup_verify(manager_email, restaurant_name, verification_code)
    assert result == "success"
    assert message == "restaurant signup verified"

    result, message = rats.signup_complete(restaurant_name, restaurant_address, restaurant_cuisine_type)
    assert result == "success"
    assert message == "restaurant signed-up"

    rats.signup(manager_email, manager_password)

    manager_secure_token = rats.signin(manager_email, manager_password)
    cook_g = rats.add_cook(manager_secure_token, cooks["giada"]["name"], cooks["giada"]["email"])
    cook_f = rats.add_cook(manager_secure_token, cooks["fabio"]["name"], cooks["fabio"]["email"])
    assert _cook_persistence.read_cook_count() == 2

    rats.remove_cook(manager_secure_token, cook_g)
    assert _cook_persistence.read_cook_count() == 1

    assert _restaurant_persistence.read_restaurant_count() == 1

    _restaurant_persistence.print_all()

    """WIP these are not fully built but as you build them update the test cases"""
    rats.upload_menu()

    """OPROC cook giada signs in """
    result, message = oproc.signup(cooks["giada"]["email"], cooks["giada"]["password"])
    assert result == "success"
    assert message == "signed-up actor='cook', email='gdl@unreal.com'"

    """ 
    OPROC cook giada see if there is any open orders she needs to work on.
    and since no customer has placed an order, the queue shows empty.
    """

    """
    OCRA: customer Daren Daring signs in
    """
    customer_name = "Daren Daring"
    customer_email = "dd@unreal.com"
    customer_password = "password"
    result, message = ocra.signup(customer_email, customer_password)
    customer_secure_token = ocra.signin(customer_email, customer_password)
    assert customer_secure_token is not None

    customer_orders = ocra.read_orders(customer_secure_token)
    assert len(customer_orders) == 0
    """
    OCRA: customer Daren selects one item, and does checkout
    no payment, nothing. just simple checkout
    """
    result, message = ocra.checkout(customer_secure_token, "cheese pizza")
    assert result == "success"
    assert message == ""
    print(f'{datetime.now()}:ocra.checkout {result=}')

    customer_orders = ocra.read_orders(customer_secure_token)
    assert len(customer_orders) == 1
    print(f'{datetime.now()}:ocra.read_orders {len(customer_orders)=}')

    """give eventing a chance to get caught up"""
    print(f'{datetime.now()}:sleep for {PAUSE_PERIOD} seconds')
    await asyncio.sleep(PAUSE_PERIOD)

    print(f'{datetime.now()}:OPROC starting now. cook wants to the orders')
    """OPROC: cook giada now sees there is an order pending"""
    cook_secure_token = oproc.signin(cooks["giada"]["email"], cooks["giada"]["password"])
    assert cook_secure_token is not None
    orders = oproc.view_open_order_queue(cook_secure_token)
    assert len(orders) == 1

    rats.view_order_status()
    rats.restaurant_rated()
    print(f'{datetime.now()}:done with prepared test steps')
    print(f'{datetime.now()}:===============================================')


# NOTE: this test needs to be the second test as it expects previous method to initialize
@pytest.mark.asyncio
async def test_signup_happy_path_cuban():
    _restaurant_persistence.print_all()
    manager_name = "Pico Martinez"
    manager_email = "pmartinez@unreal.com"
    restaurant_name = "Cuba Casa"
    restaurant_address = "123 Havana Ave"
    restaurant_cuisine_type = "Cuban"
    result, message = rats.signup_initiate(manager_name, manager_email, restaurant_name)
    assert result == "success"
    assert message == "restaurant signup initiated"

    verification_code = rats._signup_get_verification_code(manager_email, restaurant_name)
    result, message = rats.signup_verify(manager_email, restaurant_name, verification_code)
    assert result == "success"
    assert message == "restaurant signup verified"

    result, message = rats.signup_complete(restaurant_name, restaurant_address, restaurant_cuisine_type)
    assert result == "success"
    assert message == "restaurant signed-up"

    # make test independent. right now it is dependent on first one
    assert _restaurant_persistence.read_restaurant_count() == 2
    _restaurant_persistence.print_all()


@pytest.fixture()
def setup_all_persistence():
    # making sure the test always starts with empty list
    _restaurant_persistence.RESTAURANT_DICT = {}
    _cook_persistence.clear_all()
    _signin_persistence.clear_all()
    _signup_persistence.clear_all()
    yield
    # making sure the test cleans up to an empty list
    _restaurant_persistence.RESTAURANT_DICT = {}
    _cook_persistence.COOK_DICT = {}
    _signin_persistence.clear_all()
    _signup_persistence.clear_all()


@pytest.mark.asyncio
async def test_signup_error_paths(setup_all_persistence):
    """
    in this path we will go through most of the steps but by going through error paths
    """
    core_main.initialize_app()

    _restaurant_persistence.print_all()
    manager_name = "Errico Errorprone"
    manager_email = "ee@unreal.com"
    manager_password = "secret"
    restaurant_name = "Earthy Flavors"
    restaurant_address = "N Delicious Way"
    restaurant_cuisine_type = "Fusion"
    typo_error = restaurant_name + "bad_string"

    cooks = {
        "sb": {"name": "sb", "email": "sb@unreal.com"}
    }
    result, message = rats.signup_initiate(manager_name, manager_email, restaurant_name)
    assert result == "success"
    assert message == "restaurant signup initiated"

    """
    Errico forgets he signed up, and he signs up again
    this time, we catch it and tell him the restaurant is already signed up
    """
    result, message = rats.signup_initiate(manager_name, manager_email, restaurant_name)
    assert result == "error"
    assert message == "restaurant already signed up"

    """
    user realizes his folly. he remembers he had started the process
    and resumes the verification process.
    """
    result, message = rats.signup_verify(manager_email, typo_error, "dont_know")
    assert result == "error"
    assert message == f'invalid restaurant_name=\'{typo_error}\''
    """
    he types in restaurant name wrong. he fixes that.
    BUT, he doesn't remember the verification code. he just guesses it
    """
    result, message = rats.signup_verify(manager_email, restaurant_name, "dont_know")
    assert result == "error"
    assert message == f'invalid key'

    """
    he now gets serious.
    he looks in his email inbox for the verification code
    he finds it and enters it
    """
    verification_code = rats._signup_get_verification_code(manager_email, restaurant_name)
    result, message = rats.signup_verify(manager_email, restaurant_name, verification_code)
    assert result == "success"
    assert message == "restaurant signup verified"

    """
    almost done with signup but he types incorrect restaurant name 
    """
    result, message = rats.signup_complete(typo_error, restaurant_address, restaurant_cuisine_type)
    assert result == "error"
    assert message == f'invalid restaurant_name=\'{typo_error}\''

    result, message = rats.signup_complete(restaurant_name, restaurant_address, restaurant_cuisine_type)
    assert result == "success"
    assert message == "restaurant signed-up"

    rats.signup(manager_email, manager_password)

    manager_secure_token = rats.signin(manager_email, manager_password)
    cook_g = rats.add_cook(manager_secure_token, cooks["sb"]["name"], cooks["sb"]["email"])
    assert _cook_persistence.read_cook_count() == 1

    rats.remove_cook(manager_secure_token, cook_g)
    assert _cook_persistence.read_cook_count() == 0


def test_empty():
    event_bus_default = EventBusInterface()
    event_bus_default.add_listener("dummy", None)
    event_bus_default.emit("dummy", {})
