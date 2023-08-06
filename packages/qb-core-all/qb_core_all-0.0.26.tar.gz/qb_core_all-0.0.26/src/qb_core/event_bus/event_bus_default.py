import asyncio
from collections import defaultdict

from qb_core.event_bus.event_bus_interface import EventBusInterface


class EventBusDefault(EventBusInterface):
    def __init__(self):
        self.listeners = defaultdict(set)

    def add_listener(self, event_name, listener):
        self.listeners[event_name].add(listener)

    # I don't think I need this
    # def remove_listener(self, event_name, listener):
    #     self.listeners[event_name].remove(listener)
    #     if len(self.listeners[event_name]) == 0:
    #         del self.listeners[event_name]

    def emit(self, event_name, event):
        listeners = self.listeners.get(event_name, [])
        print(f'emitting {event_name=} with {str(event)=} to {len(listeners)} listeners')
        for listener in listeners:
            print(f'{event_name=} with {event=} sent to {str(listener)}')
            asyncio.create_task(listener(event))
            # # asyncio suggests this pattern
            # # https://docs.python.org/3/library/asyncio-task.html#creating-tasks
            # Save a reference to the result of this function, to avoid a task disappearing mid execution.
            # The event loop only keeps weak references to tasks.
            # A task that isn’t referenced elsewhere may get garbage-collected at any time, even before it’s done.
            # For reliable “fire-and-forget” background tasks, gather them in a collection
            # task = asyncio.create_task(some_coro(param=i))
            # # Add task to the set. This creates a strong reference.
            # background_tasks.add(task)
            #
            # # To prevent keeping references to finished tasks forever,
            # # make each task remove its own reference from the set after
            # # completion:
            # task.add_done_callback(background_tasks.discard)
