from collections import defaultdict

from qb_core.rats_pkg.cook.cook_persistence_plug_point import CookPersistenceInterface

cook_dict = {}


class CookPersistenceCore(CookPersistenceInterface):
    def __init__(self):
        pass

    @staticmethod
    def clear_all():
        global cook_dict
        cook_dict = defaultdict(dict)

    def read_cook_count(self):
        return len(cook_dict)

    def read_cook(self, cook_name):
        return cook_dict.get(cook_name)

    def save_cook(self, cook):
        cook_dict[cook.name] = cook

    def remove_cook(self, cook):
        cook_dict.pop(cook.name)

    def print_all(self):
        print(f'{cook_dict=}')


def get_implementation():
    return CookPersistenceCore()