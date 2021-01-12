#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hmac
from time import time
from hashlib import sha256


def generate_signature(msg: str, key: str) -> str:
    """
    Generates the signature required to send the request.

    :param msg: hmac.new(msg)
    :param key: hmac.new(key)
    :return: hexdigest string
    """
    output = hmac.new(
        msg=bytes(msg, 'latin-1'),
        key=bytes(key, 'latin-1'),
        digestmod=sha256
    ).hexdigest().upper()

    return output


def get_timestamp() -> str:
    """
    Return the current timestamp * 1000.

    :return: timestamp * 1000
    """
    timestamp = str(
        int(time() * 1000)
    )

    return timestamp
