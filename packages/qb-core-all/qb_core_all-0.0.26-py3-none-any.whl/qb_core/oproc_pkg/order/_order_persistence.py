from collections import defaultdict

ORDER_LIST = []


def clear_all():
    global ORDER_LIST
    ORDER_LIST = []


def read_order_count(customer_email):
    return len(ORDER_LIST[customer_email])


def read_open_orders():
    open_orders = []
    for o in ORDER_LIST:
        # open_orders.append(o)
        if o.cook_assignment is None:
            open_orders.append(o)
    return open_orders


def save_order(order):
    print(f'OPROC order_persistence.save_order called')
    ORDER_LIST.append(order)
    print_all()
    print(f'OPROC order_persistence.save_order returns')


def print_all():
    print(f'{ORDER_LIST=}')


clear_all()
