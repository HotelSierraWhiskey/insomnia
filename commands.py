from apdu_utils.security_commands import *
from apdu_utils.application_commands import *
from apdu_utils.file_commands import *
from apdu_utils.data_commands import *
from dispatch import dispatch
from functools import partial
from auth import Auth
from routine import Routine


def get_uid(callback=None) -> Routine:
    def task(service=None):
        send = partial(dispatch, service=service)
        send(command_get_version())
        send(command_additional_frame())
        resp = send(command_additional_frame())
        if not resp.is_successful():
            return
        if callback:
            callback(resp)

    routine = Routine(partial(task))
    return routine


def select_root_application(callback=None) -> Routine:
    def task(service=None):
        send = partial(dispatch, service=service)
        resp = send(command_select_root_application())
        if not resp.is_successful():
            return
        if callback:
            callback(resp)

    routine = Routine(partial(task))
    return routine


def select_application(aid: list, callback=None) -> Routine:
    def task(service=None):
        send = partial(dispatch, service=service)
        resp = send(command_select_application(aid))
        if not resp.is_successful():
            return
        if callback:
            callback(resp)

    routine = Routine(partial(task))
    return routine


def aes_authenticate(key: list, key_id: list = [0x00], callback=None) -> Routine:
    def task(service=None):
        send = partial(dispatch, service=service)
        auth = Auth(bytearray(key), "AES")
        resp = send(command_aes_auth(key_id))
        if not resp.is_successful():
            return

        submission = auth.authenticate(resp)
        resp = send(command_additional_frame(submission))
        if not resp.is_successful():
            return

        if callback:
            session_key = auth.get_session_key(resp)
            callback(session_key)

    routine = Routine(partial(task))
    return routine
