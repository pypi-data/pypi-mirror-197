from qb_core.rats_pkg.cook import cook_persistence_core


def add_cook(cook):
    _cook_persistence.save_cook(cook)


def remove_cook(cook):
    _cook_persistence.remove_cook(cook)
