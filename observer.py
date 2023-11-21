from smartcard.CardMonitoring import CardObserver
from smartcard.util import toBytes
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException, CardConnectionException
from .config import config
from .dispatch import dispatch
from .auth import Auth
from .apdu_utils.security_commands import *
from .apdu_utils.application_commands import *
from functools import partial


class Observer(CardObserver):
    def __init__(self, callback=None, auth: dict | None = None, threading_event=None):
        self.callback = callback
        self.auth = auth
        self.threading_event = threading_event
        self.send = None
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
                self.send = partial(dispatch, service=self.service)
                session_key = self.pre_auth()
                self.result = self.callback(send=self.send, session_key=session_key)
                self.service.connection.disconnect()
                self.threading_event(self.result)
            except CardConnectionException as e:
                if config.debug:
                    config.writer(e)
                return None

    def pre_auth(self) -> list | None:
        if not self.auth:
            return None
        try:
            key = self.auth["key"]
            key_number = self.auth["key_number"]
            response = self.send(command_aes_auth(key_number))
            authenticator = Auth(bytearray(key), "AES")
            submission = authenticator.authenticate(response.data)
            response = self.send(command_additional_frame(submission))
            session_key = authenticator.get_session_key(response.data)
            return session_key
        except Exception as e:
            config.writer(e)
