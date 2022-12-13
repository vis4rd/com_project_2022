from threading import Event, Thread


class CustomThread(Thread):
    def __init__(self, events: dict[str, Event], data: dict[str, str | None]):
        Thread.__init__(self, name=self.__class__.__name__)

        self.events = events
        self.data = data
