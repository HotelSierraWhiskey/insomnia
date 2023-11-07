from .apdu_utils.response_codes import apdu_response_codes
from smartcard.util import toHexString


class Response:
    def __init__(self, raw_response: list):
        self.data, sw1, sw2 = raw_response
        self.status = sw1, sw2

    def is_successful(self):
        return self.status in [(0x91, 0x00), (0x90, 0x00), (0x91, 0xAF)]

    def to_bytes(self):
        return bytearray(self.data)

    def to_string(self):
        return self.to_bytes().decode("utf-8")

    def to_hex_string(self, *args, **kwargs):
        return toHexString(self.data, *args, **kwargs)

    @property
    def response_code(self) -> str:
        try:
            return apdu_response_codes[self.status]
        except KeyError as e:
            return f"Undocumented response: {self.status}"


def dispatch(command: list, service) -> Response:
    raw_response = service.connection.transmit(command)
    response = Response(raw_response)
    return response
