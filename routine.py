from smartcard.CardMonitoring import CardObserver
from smartcard.util import toBytes
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException, CardConnectionException


class Routine(CardObserver):
    def __init__(self, callback_in=None, callback_out=None):
        self.callback_in = callback_in
        self.callback_out = callback_out
        self.card_type = ATRCardType(toBytes("3B 81 80 01 80 80"))

    def update(self, _, handlers):
        added_cards, removed_cards = handlers
        try:
            if added_cards:
                card_request = CardRequest(timeout=10, cardType=self.card_type)
                service = card_request.waitforcard()
                service.connection.connect()
                if self.callback_in:
                    self.callback_in(service=service)
                service.disconnect()
                return
        except (CardRequestTimeoutException, CardConnectionException) as e:
            print(e)

        if removed_cards:
            if self.callback_out:
                self.callback_out(self.out_args)
