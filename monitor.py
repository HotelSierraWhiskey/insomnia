from smartcard.CardMonitoring import CardMonitor
from time import sleep


class Monitor(CardMonitor):
    def __init__(self, timeout: float = 3.0):
        super().__init__()
        self.timeout = timeout

    def start(self, task):
        self.addObserver(task)
        sleep(self.timeout)
        self.deleteObserver(task)
