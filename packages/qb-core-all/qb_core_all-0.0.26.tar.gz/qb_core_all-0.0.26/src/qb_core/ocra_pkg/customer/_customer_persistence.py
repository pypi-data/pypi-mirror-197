CUSTOMER_DICT = {}


def read_customer_count():
    return len(CUSTOMER_DICT)


def read_customer(customer_name):
    return CUSTOMER_DICT.get(customer_name)


def save_customer(customer):
    CUSTOMER_DICT[customer.email] = customer


def remove_customer(customer):
    CUSTOMER_DICT.pop(customer.email)


def print_all():
    print(f'{CUSTOMER_DICT=}')
