DEFAULT_WRITER = print
DEFAULT_CARD_ATR = "3B 81 80 01 80 80"
DEFAULT_TIMEOUT = 5.0


class Config:
    debug = True
    writer = DEFAULT_WRITER
    card_atr = DEFAULT_CARD_ATR
    timeout = DEFAULT_TIMEOUT


config = Config()
