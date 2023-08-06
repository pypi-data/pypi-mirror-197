"""
oproc.py
this is Order Processor
"""
from datetime import datetime

from qb_core.event_bus import event_bus_core, event_bus_events
from qb_core.oproc_pkg.order import order_entity
from qb_core.oproc_pkg.order.order_model import Order
from qb_core.rats_pkg.signin import signin_service


def initialize_module():
    # this must be called exactly once, so put it here at the module level
    # can a module be imported more than once?
    print(f'*** REGISTERING listener handle_cooked added for event cook_added')
    event_bus_core.register_listener(event_bus_events.EVENT_COOK_ADDED, handle_cook_added)
    event_bus_core.register_listener(event_bus_events.EVENT_ORDER_CONFIRMED, handle_order_confirmed)


async def handle_cook_added(event_data):
    print(f'handle_cook_added called with {event_data=}')


async def handle_order_confirmed(event_data):
    try:
        print(
            f'{datetime.now()}:handle_order_confirmed called with {event_data=}. got order of type {type(event_data.order)}')
        oproc_order = Order()
        oproc_order.id = event_data.order.id
        oproc_order.customer_email = event_data.order.customer_email
        oproc_order.total_price = event_data.order.total_price
        oproc_order.items = event_data.order.items
        order_entity.save_order(oproc_order)
        print(f'{datetime.now()}:done saving order {order_entity.read_open_orders()=}')
        order_entity.read_open_orders()
    except Exception as ex:
        print(f'{datetime.now()}: caught {str(ex)}')


def signup(cook_email, password):
    return signin_service.signup(signin_service.ACTOR_COOK, cook_email, password)


def signin(cook_email, password):
    return signin_service.signin(signin_service.ACTOR_COOK, cook_email, password)


def view_open_order_queue(cook_secure_token):
    return order_entity.read_open_orders()
