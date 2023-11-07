from smartcard.CardMonitoring import CardObserver
from smartcard.util import toBytes
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException, CardConnectionException
from .config import config
from .dispatch import dispatch
from functools import partial


class Observer(CardObserver):
    def __init__(self, callback=None, event_callback=None):
        self.callback = callback
        self.event_callback = event_callback
        card_type = ATRCardType(toBytes(config.card_atr))
        card_request = CardRequest(timeout=config.timeout, cardType=card_type)
        self.result = None

        try:
            self.service = card_request.waitforcard()
            self.service.connection.connect()
        except (CardRequestTimeoutException, CardConnectionException) as e:
            if config.debug:
                config.writer(e)
            return None

    def update(self, _, handlers):
        added, _ = handlers
        if added:
            try:
                send = partial(dispatch, service=self.service)
                self.result = self.callback(send=send)
                self.service.connection.disconnect()
                self.event_callback(self.result)
            except CardConnectionException as e:
                if config.debug:
                    config.writer(e)
                return None
