from smartcard.CardMonitoring import CardObserver
from smartcard.util import toBytes
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException, CardConnectionException
from .config import config
from .dispatch import dispatch
from functools import partial


class Observer(CardObserver):
    def __init__(self, callback=None):
        self.callback = callback
        card_type = ATRCardType(toBytes(config.card_atr))
        card_request = CardRequest(timeout=config.timeout, cardType=card_type)
        self.service = card_request.waitforcard()
        self.service.connection.connect()

    def update(self, _, handlers):
        added, removed = handlers
        try:
            if added:
                if config.debug:
                    config.writer("--- Enter ---")
                send = partial(dispatch, service=self.service)
                self.callback(send=send)
                self.service.connection.disconnect()
            if removed:
                if config.debug:
                    config.writer("--- Exit ---")

        except (CardRequestTimeoutException, CardConnectionException) as e:
            config.writer(e)
