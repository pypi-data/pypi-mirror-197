COOK_DICT = {}


def read_cook_count():
    return len(COOK_DICT)


def read_cook(cook_name):
    return COOK_DICT.get(cook_name)


def save_cook(cook):
    COOK_DICT[cook.name] = cook


def remove_cook(cook):
    COOK_DICT.pop(cook.name)


def print_all():
    print(f'{COOK_DICT=}')
