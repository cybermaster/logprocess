"""
page.py
"""


class Page(object):
    """
    Page object will create the list of events that associated with the auth key

    :param name: the auth ID in the LogEntry object
    :param events: list of events for that auth ID
    """

    def __init__(self, name=None, events=None):
        self.name = name
        self.events = events or []

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.name == other.name and self.events == self.events

    def add(self, x):
        return self.events.append(x)

    @property
    def eventstring(self):
        return ", ".join(self.events)