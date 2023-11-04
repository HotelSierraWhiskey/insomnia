# Insomnia 🌃

## About
Insomnia wraps [pyscard](https://pyscard.sourceforge.io/) and [APDU Utils](https://github.com/HotelSierraWhiskey/apdu_utils) up into a tight and rather opinionated little package. All of pyscard's RFID monitoring objects are abstracted into a `card_task` decorator, which injects a command dispatcher into your top-level functions. Sessions still take place inside pyscard's card monitoring thread, as they usually do. Just decorate your function, and use the dispatcher to communicate with your DESFire card. That's it. 


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