# Insomnia 🌃

## About
Insomnia wraps [pyscard](https://pyscard.sourceforge.io/) and [APDU Utils](https://github.com/HotelSierraWhiskey/apdu_utils) up into one package. All of pyscard's RFID monitoring objects are abstracted into a `card_task` decorator, which provides your functions with a command dispatcher. Sessions still take place inside pyscard's card monitoring thread, as they usually do. Just decorate your function, and use the dispatcher to communicate with your DESFire card. That's it. 


### Example
```python
from insomnia import card_task
from insomnia.apdu_utils.application_commands import command_select_application


@card_task
def check_application(application_id, **kwargs):
    send = kwargs.get("send")
    response = send(command_select_application(application_id))
    # do something with response
```