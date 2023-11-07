from smartcard.CardMonitoring import CardMonitor
from .observer import Observer
from functools import partial
import threading


class card_task(CardMonitor):
    def __init__(self, func):
        super().__init__()
        self._func = func
        self.scan_event = threading.Event()

    def event_callback(self, result):
        self.observer_result = result
        self.scan_event.set()

    def __call__(self, *args, **kwargs):
        func = partial(self._func, *args, **kwargs)
        observer = Observer(func, self.event_callback)
        self.addObserver(observer)
        return observer.result
