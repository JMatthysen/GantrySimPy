
"""

event base class

"""

class Event:
    def __init__(self, event_name, subscribers):
        self.event_name     = event_name
        self.subscribers    = subscribers

    def distribute_event(self):
        for subscriber in self.subscribers:
            subscriber.on_event(self.event_name)



"""

event_handler base class to ensure all subscribers have .on_event() function

"""

class EventHandler:
    @staticmethod
    def on_event(event):
        pass
