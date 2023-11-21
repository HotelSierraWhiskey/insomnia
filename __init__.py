from smartcard.CardMonitoring import CardMonitor
from .observer import Observer
from functools import partial
import threading


class Insomnia(CardMonitor):
    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.scan_event = threading.Event()

    def threading_event_callback(self, result):
        self.observer_result = result
        self.scan_event.set()

    def basic(self, *args, **kwargs):
        def decorator(func):
            def wrapper():
                callback = partial(func, *args, **kwargs)
                observer = Observer(
                    callback=callback, threading_event=self.threading_event_callback
                )
                self.addObserver(observer)
                self.deleteObserver(observer)
                return observer.result

            return wrapper

        return decorator

    def authenticate(self, *args, **kwargs):
        def decorator(func):
            def wrapper():
                callback = partial(func, *args, **kwargs)
                observer = Observer(
                    callback=callback,
                    auth=self.config,
                    threading_event=self.threading_event_callback,
                )
                self.addObserver(observer)
                self.deleteObserver(observer)
                return observer.result

            return wrapper

        return decorator
