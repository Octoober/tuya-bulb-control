#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import requests
from typing import NoReturn
from tuya_bulb_control._helpers import *
from .exceptions import Authorized


class _TuyaApi:
    """
    Private class for API requests
    """

    def __init__(self):
        self._client_id: str = ""
        self._secret_key: str = ""
        self._device_id: str = ""
        self.__base_url: str = ""
        self.__sign_method: str = "HMAC-SHA256"

    def __default_request(self) -> dict:
        """
        Default request type.

        :return: default headers
        """

        t = get_timestamp()
        access_token = self._authorized()["result"]["access_token"]
        sign = generate_signature(self._client_id + access_token + t, self._secret_key)

        default_headers = {
            "client_id": self._client_id,
            "access_token": access_token,
            "sign_method": self.__sign_method,
            "sign": sign,
            "t": t,
        }

        return default_headers

    def _set_region(self, region_key: str) -> NoReturn:
        """
        Set region key and creates a base_url.

        :param region_key: region key. Example: cn; us; eu; in
        """
        self.__base_url = f"https://openapi.tuya{region_key}.com/v1.0"

    def _authorized(self) -> dict:
        """
        Get the access token to execute requests.

        :return: access token
        """

        t = get_timestamp()
        uri = self.__base_url + "/token?grant_type=1"
        sign = generate_signature(self._client_id + t, self._secret_key)

        headers_pattern = {
            "client_id": self._client_id,
            "secret": self._secret_key,
            "sign_method": self.__sign_method,
            "sign": sign,
            "t": t,
        }

        try:
            response = requests.get(uri, headers=headers_pattern).json()
        except Exception:
            raise Exception
        else:
            if not response["success"]:
                note = (
                    "\nNote: One of the reasons for the error is "
                    "an incorrect client_id or secret_key."
                    if response["code"] == 1004
                    else ""
                )

                raise Authorized(
                    code=response["code"],
                    message=str(response["msg"]).capitalize() + note,
                )

            return response

    def _get(self, postfix: str) -> dict:
        """
        Performs a GET request at the specified address.

        :param postfix: request address. Example: /device/{device_id}/commands
        :return: answer
        """

        uri = self.__base_url + postfix
        headers_pattern = self.__default_request()

        try:
            response = requests.get(uri, headers=headers_pattern).json()
        except Exception:
            raise Exception
        else:
            return response

    def _post(self, postfix: str, body=None) -> dict:
        """
        Performs a POST request at specified address.

        :param postfix: request address. Example: /device/{device_id}/commands
        :param body: request body
        :return: answer
        """

        if body is None:
            body = {}

        body = json.dumps(body)
        uri = self.__base_url + postfix
        headers_pattern = self.__default_request()

        try:
            response = requests.post(uri, headers=headers_pattern, data=body).json()
        except Exception:
            raise Exception
        else:
            return response

    def get_status(self, device_id: str = None) -> dict:
        """
        Get device status.

        :param device_id: device id
        :return: status dict
        """
        device_id = self._device_id if device_id is None else device_id

        response = self._get(postfix=f"/devices/{device_id}/status")["result"]

        return response

    def get_control(self, device_id: str = None) -> dict:
        """
        Commands that are applicable to this device.

        :param device_id: device id
        :return: functions dict
        """

        device_id = self._device_id if device_id is None else device_id

        response = self._get(f"/devices/{device_id}/functions")["result"]["functions"]

        return response
