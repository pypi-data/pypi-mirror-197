from collections import defaultdict

ORDER_DICT = None
# example_order = {
#     "c1" : [Order1, Order2, Order3]
# }


def clear_all():
    global ORDER_DICT
    ORDER_DICT = defaultdict(list)


def read_order_count(customer_email):
    return len(ORDER_DICT[customer_email])


def read_orders(customer_email):
    return ORDER_DICT[customer_email]


def read_order(customer_email, order_id):
    return ORDER_DICT[customer_email]


def save_order(order):
    ORDER_DICT[order.customer_email].append(order)


clear_all()
