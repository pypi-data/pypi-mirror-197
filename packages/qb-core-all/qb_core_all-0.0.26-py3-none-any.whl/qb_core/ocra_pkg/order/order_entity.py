from qb_core.ocra_pkg.order import _order_persistence


def read_orders(customer_email):
    return _order_persistence.read_orders(customer_email)


def save_order(order):
    print(f'OCRA save_order')
    _order_persistence.save_order(order)
