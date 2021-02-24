
"""

event base class

"""


class Event:
    def __init__(self, event_type, event_name, subscribers):
        self.event_type     = event_type
        self.event_name     = event_name
        self.subscribers    = subscribers

    def publish_event(self, data):
        for subscriber in self.subscribers:
            subscriber.on_event(self.event_type, self.event_name, data)


"""

event_handler base class to ensure all subscribers have .on_event() function

"""


class EventHandler:
    @staticmethod
    def on_event( event_type, event_name, data):
        print("No on_event setup")
