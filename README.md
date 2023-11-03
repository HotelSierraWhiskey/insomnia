# Insomnia 🌃

## About
Use Insomnia's `card_task` decorator create DESFire card communication sessions. Simple.

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