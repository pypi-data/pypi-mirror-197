from qb_core.ocra_pkg.customer import _customer_persistence


def add_customer(customer):
    _customer_persistence.save_customer(customer)


def remove_customer(customer):
    _customer_persistence.remove_customer(customer)
