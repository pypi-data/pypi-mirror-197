"""
basic things I need in an event bus
* emitter registers with EB it's intent emit an event
* it describes the event object
* one or more listener register with EB their intent to subscribe to an event
* emitter emits an event to EB
* EB invokes the listeners registered

this class acts as interface class
"""
from qb_core.event_bus.event_bus_default import EventBusDefault

# TODO make this conditional
#  if plugin is not configured (or configured to default) do this, else use plugin suggested event bus
system_event_bus = EventBusDefault()
print(f'*** initialized {system_event_bus=}')


def register_emitter(event_name, emitter_name):
    """
    use this method for registering the emitter
    """
    pass


def register_listener(event_name, listener):
    system_event_bus.add_listener(event_name, listener)


def emit_event(event_name, event):
    system_event_bus.emit(event_name, event)

