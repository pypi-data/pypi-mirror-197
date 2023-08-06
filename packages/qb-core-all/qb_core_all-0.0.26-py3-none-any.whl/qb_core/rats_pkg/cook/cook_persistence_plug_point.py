

# this interface defines all the possible access patterns and write
# patterns for the cook object
# the plugin that implements this interface can use this information
# to define the appropriate storage and efficient ways to provide the
# handle data with that storage
class CookPersistenceInterface:
    def __init__(self):
        pass

    def read_cook_count(self):
        pass

    def read_cook(self, cook_name):
        pass

    def save_cook(self, cook):
        pass

    def remove_cook(self, cook):
        pass

    def print_all(self):
        pass
