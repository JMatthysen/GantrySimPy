
"""

event base class

"""


class Event:
    def __init__(self, event_type, event_name, subscribers, data):
        self.event_type     = event_type
        self.event_name     = event_name
        self.data           = data


class EventBus:
    def __init__(self):
        self.publishers = list()

    def post_event(self, event_name, data):


class Publisher:
    def __init__(self, events, subscribers):
        self.events     = events
        self.subscribers = subscribers




"""

event_handler base class to ensure all subscribers have .on_event() function

"""


class EventHandler:
    @staticmethod
    def on_event(event):
        print("No on_event setup")
