from smartcard.CardMonitoring import CardMonitor
from .config import config
from .observer import Observer
from functools import partial
from time import sleep


class card_task(CardMonitor):
    def __init__(self, func, timeout: float = config.timeout):
        super().__init__()
        self._func = func
        self.timeout = timeout

    def __call__(self, *args, **kwargs):
        func = partial(self._func, *args, **kwargs)
        observer = Observer(func)
        self.addObserver(observer)
        sleep(self.timeout)