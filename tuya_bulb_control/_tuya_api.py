#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import hmac
import requests
from time import time
from hashlib import sha256
from .exceptions import AuthorizedError


class _TuyaApi:
    """
    Private class for API requests
    """

    def __init__(self, client_id: str, secret_key: str, region_key: str):
        self._client_id = client_id
        self._secret_key = secret_key
        self._region_key = region_key

        self._base_url = f"https://openapi.tuya{self._region_key}.com/v1.0"
        self.__sign_method: str = "HMAC-SHA256"

    @staticmethod
    def __generate_signature(msg: str, key: str) -> str:
        """
        Generates the signature required to send the request.

        :param msg: hmac.new(msg)
        :param key: hmac.new(key)
        :return: hexdigest string
        """
        output = (
            hmac.new(
                msg=bytes(msg, "latin-1"), key=bytes(key, "latin-1"), digestmod=sha256
            )
            .hexdigest()
            .upper()
        )

        return output

    @staticmethod
    def __get_timestamp() -> str:
        """
        Return the current timestamp * 1000.

        :return: timestamp * 1000
        """
        timestamp = str(int(time() * 1000))

        return timestamp

    def __request_template(self) -> dict:
        """
        Default request type.

        :return: default headers
        """

        t = self.__get_timestamp()
        access_token = self.__token()
        sign = self.__generate_signature(
            self._client_id + access_token + t, self._secret_key
        )

        default_headers = {
            "client_id": self._client_id,
            "access_token": access_token,
            "sign_method": self.__sign_method,
            "sign": sign,
            "t": t,
        }

        return default_headers

    def __token(self) -> str:
        """
        Get the access token.

        :return: access token
        """

        t = self.__get_timestamp()
        uri = self._base_url + "/token?grant_type=1"
        sign = self.__generate_signature(self._client_id + t, self._secret_key)

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
                raise AuthorizedError(
                    target=response["code"], msg=str(response["msg"]).capitalize()
                )

            try:
                token = response["result"]["access_token"]
            except KeyError:
                raise KeyError("Failed to get access_token")
            else:
                return token

    def _get(self, postfix: str) -> dict:
        """
        Performs a GET request at the specified address.

        :param postfix: request address. Example: /device/{device_id}/commands
        :return: response dict
        """

        uri = self._base_url + postfix
        headers = self.__request_template()

        try:
            response = requests.get(uri, headers=headers).json()
        except Exception:
            raise Exception
        else:
            return response

    def _post(self, postfix: str, body=None) -> dict:
        """
        Performs a POST request at specified address.

        :param postfix: request address. Example: /device/{device_id}/commands
        :param body: request body
        :return: response dict
        """

        if body is None:
            body = {}

        body = json.dumps(body)
        uri = self._base_url + postfix
        headers = self.__request_template()

        try:
            response = requests.post(uri, headers=headers, data=body).json()
        except Exception:
            raise Exception
        else:
            return response
