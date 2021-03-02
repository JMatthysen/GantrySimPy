
"""

event base class

"""


class Event:
    def __init__(self, event_type, event_name, subscribers, data):
        self.event_name     = event_name


class EventBus:
    def __init__(self):
        self._event_sub_dict = {}  # a dictionary that joins an event name to a list of subscribers

        self._initialize_events()

    def _initialize_events(self):
        self.add_event("translation_event")
        self.add_event("position_change_event")
        self.add_event("view_screen_translation_event")
        self.add_event("view_screen_rotation_event")

    def post_event(self, event_name, data):
        #  a publisher will use this to declare that an event has occured

        if self._event_exists(event_name):
            self._distribute_event(event_name, data)
        else:
            pass

    def add_event(self, event_name):
        if self._event_exists(event_name):
            self._error_message(f"{event_name} already exists.")
        else:
            self._event_sub_dict[event_name] = list()

    def _distribute_event(self, event_name, data):
        # the even_bus "pipeline" will use this to distribute the fact that an
        # event has occurred to the subscribers to said event
        for sub in self.get_sub_list(event_name):
            sub.on_event(event_name, data)

    def subscribe(self, sub, event_name):
        # used by subs to be added to the subscription list of a specific event
        # Access the list connected to the event key, check if its already subscribed,
        # then subscribe (if necessary)
        if self._event_exists(event_name):
            if sub not in self._event_sub_dict[event_name]:
                self._event_sub_dict[event_name].append(sub)
            else:
                self._error_message(f"{sub.name}'s already a subscriber to {event_name}.")

    def _event_exists(self, event_name):
        if event_name in self._event_sub_dict:
            return True
        else:
            self._error_message(f"{event_name} is not an event, yet.")
            return False

    def get_sub_list(self, event_name):
        return self._event_sub_dict[event_name]

    @staticmethod
    def _error_message(error_message):
        # print(error_message)
        pass
"""     

event_handler base class to ensure all subscribers have .on_event() function

"""


class EventHandler:
    @staticmethod
    def on_event(event_name, data):
        print("No on_event setup")


"""
event list:
    translation_event
    position_change_event
"""