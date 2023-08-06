"""
ocra.py
this follows interactor pattern.
implements both command executor and event listener

see common notes in rats.py
"""
from qb_core.ocra_pkg.order import order_entity
from qb_core.ocra_pkg.order.order_model import Order, OrderItem, OrderAdded
from qb_core.rats_pkg.signin import signin_service
from qb_core.event_bus import event_bus_core, event_bus_events


def initialize_module():
    event_bus_core.register_emitter(event_bus_events.EVENT_ORDER_CONFIRMED, None)
    event_bus_core.register_emitter(event_bus_events.EVENT_RESTAURANT_RATED, None)
    event_bus_core.register_emitter(event_bus_events.EVENT_DRIVER_RATED, None)

    print(f'*** REGISTERING listener None added for event menu_uploaded')
    event_bus_core.register_listener(event_bus_events.EVENT_MENU_UPLOADED, None)


def signup(customer_email, password):
    return signin_service.signup(signin_service.ACTOR_CUSTOMER, customer_email, password)


def signin(customer_email, password):
    return signin_service.signin(signin_service.ACTOR_CUSTOMER, customer_email, password)


def checkout(secure_token, order_item_name):
    order = Order()
    # TODO how to generate this number
    order.id = "123123"
    order.customer_email = secure_token.email
    order_item = OrderItem()
    order_item.item_name = order_item_name
    order_item.quantity = 1
    order_item.price = 9.99
    order.items.append(order_item)
    order_entity.save_order(order)

    # this should be the last step so that we send this event exactly once
    # when all the steps above have completed
    event_bus_core.emit_event(event_bus_events.EVENT_ORDER_CONFIRMED, OrderAdded(order))

    return "success", ""


def read_orders(secure_token):
    return order_entity.read_orders(secure_token.email)
