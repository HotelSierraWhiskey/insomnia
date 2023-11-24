from smartcard.CardMonitoring import CardMonitor
from .observer import Observer
from functools import partial
import threading


class Insomnia(CardMonitor):
    def __init__(self, auth=None):
        super().__init__()
        self.auth = auth
        self.scan_event = threading.Event()

    def threading_event_callback(self, result):
        self.observer_result = result
        self.scan_event.set()

    def basic(self, *args, **kwargs):
        """
        For basic card operations that do not require authentication
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
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
        """
        Pre-authenticates cards configured for either AES or DES
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
                callback = partial(func, *args, **kwargs)
                observer = Observer(
                    callback=callback,
                    auth=self.auth,
                    threading_event=self.threading_event_callback,
                )
                self.addObserver(observer)
                self.deleteObserver(observer)
                return observer.result

            return wrapper

        return decorator
