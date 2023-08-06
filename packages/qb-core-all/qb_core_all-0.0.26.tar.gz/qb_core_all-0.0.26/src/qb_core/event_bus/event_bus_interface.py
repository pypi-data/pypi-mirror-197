import asyncio
from collections import defaultdict


class EventBusInterface:
    def __init__(self):
        pass

    def add_listener(self, event_name, listener):
        pass

    # I don't think I need this
    # def remove_listener(self, event_name, listener):
    #     pass

    def emit(self, event_name, event):
        pass
