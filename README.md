# Insomnia 🌃

## About
Insomnia wraps [pyscard](https://pyscard.sourceforge.io/) and [APDU Utils](https://github.com/HotelSierraWhiskey/apdu_utils) into one package. All of pyscard's RFID monitoring objects are abstracted into an `Insomnia` object, instances of which can be used to decorate your functions. Sessions still take place inside pyscard's card monitoring thread, as they usually do. Just decorate your function, and use the dispatcher to communicate with your DESFire card. That's it. 


### Basic Example
```python
from insomnia import Insomnia
from insomnia.apdu_utils.application_commands import command_select_application

app = Insomnia()

@app.basic()
def check_application(application_id, **kwargs):
    send = kwargs.get("send")
    response = send(command_select_application(application_id))
    return response
```

### Example using Pre-Authentication
```python
from insomnia import Insomnia


config = {
    "key": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "key_number": [0]
}

app = Insomnia(config)

@app.authenticate()
def get_session_key(**kwargs):
    session_key = kwargs.get("session_key")
    return session_key
```