from smartcard.CardMonitoring import CardObserver
from smartcard.util import toBytes
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException, CardConnectionException
from .config import config
from .dispatch import dispatch
from .auth import Auth, DEFAULT_DES_KEY
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
        """
        If an authentication configuration is provided, this will attempt to auth with AES,
        If that doesn't work, the Observer will assume you're trying to authenticate a factory-fresh card,
        in which case it will try to auth with the default DES key (eight bytes of zero with key id zero)
        """
        if not self.auth:
            return None
        try:
            key = self.auth["MASTER_KEY"]
            key_number = self.auth["MASTER_KEY_NUMBER"]
            authenticator = Auth(bytearray(key), "AES")
            response = self.send(command_aes_auth(key_number))

            if not response.is_successful():
                authenticator = Auth(bytearray(DEFAULT_DES_KEY), "DES")
                response = self.send(command_des_auth([0x00]))
                if not response.is_successful():
                    if config.debug:
                        config.writer(
                            f"Could not authenticate: {response.response_code}. Double check your key number."
                        )

            submission = authenticator.authenticate(response.data)
            response = self.send(command_additional_frame(submission))
            session_key = authenticator.get_session_key(response.data)
            return session_key
        except Exception as e:
            config.writer(e)
