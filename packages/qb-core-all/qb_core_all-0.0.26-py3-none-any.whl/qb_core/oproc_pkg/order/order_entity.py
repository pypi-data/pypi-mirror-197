from qb_core.oproc_pkg.order import _order_persistence


def read_open_orders():
    return _order_persistence.read_open_orders()


def save_order(order):
    print(f'OPROC order_entity.save_order called')
    _order_persistence.save_order(order)
    print(f'OPROC order_entity.save_order returns')
