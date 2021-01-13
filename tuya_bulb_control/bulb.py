#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from ._tuya_api import _TuyaApi
from .exceptions import ValueNotInRange, ModeNotExists


class Bulb(_TuyaApi):
    """
    Allows you to control the operation of your smart light bulb.

    :param client_id: your client id
    :param secret_key: your secret key
    :param region_key: your region key. Example: cn; us; eu; in
    :param device_id: your device id
    """

    def __init__(
        self, client_id: str, secret_key: str, region_key: str, device_id: str = None
    ):
        super().__init__()
        self._client_id = client_id
        self._secret_key = secret_key
        self._device_id = device_id

        self._set_region(region_key)

    def work_mode(self, mode: str = None, device_id: str = None) -> dict:
        """
        Select work mode.
        You can get a list of mods from get_control()[1]['values']['range']

        :param mode: work mode. For example: white; colour; scene; music
        :param device_id: device id
        :raise KeyError: if the bulb doesn't support work mode
        :raise tuya_bulb_control.exceptions.ModeNotExists: if work mode doesn't exist
        :return: response dict
        """

        try:
            control = json.loads(self.get_control(device_id=device_id)[1]["values"])
            target = control["range"]
        except KeyError:
            raise KeyError
        else:
            find_mode = [True for x in target if x == mode]

            if not find_mode:
                raise ModeNotExists(mode=mode)

            mode = target[0] if mode is None else mode
            body = {"commands": [{"code": "work_mode", "value": mode}]}
            device_id = self._device_id if device_id is None else device_id
            response = self._post(f"/devices/{device_id}/commands", body=body)

            return response

    def color(
        self,
        hue_color: int = None,
        saturation: int = None,
        value: int = None,
        device_id: str = None,
    ) -> dict:
        """
        Color mode settings.

        :param hue_color: hue color from 0 to 360.
        :param saturation: percentage saturation from 0 to 100
        :param value: percentage brightness from 0 to 100
        :param device_id: your device id
        :raise tuya_bulb_control.exceptions.ValueNotInRange: if the value is out of range
        :return: response dict or bool
        """

        device_id = self._device_id if device_id is None else device_id

        if hue_color and hue_color > 360:
            raise ValueNotInRange(
                message=f"{hue_color} -> The value must be between 0 and 360"
            )

        if saturation and saturation > 100:
            raise ValueNotInRange(
                message=f"{saturation} -> The value must be between 0 and 100"
            )

        if value and value > 100:
            raise ValueNotInRange(
                message=f"{value} -> The value must be between 0 and 100"
            )

        if hue_color is None or saturation is None or value is None:
            current_value = json.loads(
                [
                    x["value"]
                    for x in self.get_status()
                    if x["code"] == "colour_data_v2"
                ][0]
            )

            hue_color = current_value["h"] if hue_color is None else hue_color
            saturation = current_value["s"] / 10 if saturation is None else saturation
            value = current_value["v"] / 10 if value is None else value

        body = {
            "commands": [
                {
                    "code": "colour_data_v2",
                    "value": {"h": hue_color, "s": saturation * 10, "v": value * 10},
                }
            ]
        }
        response = self._post(postfix=f"/devices/{device_id}/commands", body=body)

        return response

    def switch(self, status: bool = None, device_id: str = None) -> dict:
        """
        ON or OFF the device.

        :param status: explicit status indication
        :param device_id: device id
        :return: response dict
        """

        if status is None:
            status = not [
                x["value"] for x in self.get_status() if x["code"] == "switch_led"
            ][0]

        body = {"commands": [{"code": "switch_led", "value": status}]}
        device_id = self._device_id if device_id is None else device_id
        response = self._post(postfix=f"/devices/{device_id}/commands", body=body)

        return response

    def temperature(self, value: int, device_id: str = None) -> dict:
        """
        Color temperature.

        :param device_id: device id
        :param int value: percentage from 0 to 100. For example: 0 = warm or 100 = cold
        :raise tuya_bulb_control.exceptions.ValueNotInRange: if the value is out of range
        :return: response dict or bool
        """

        if value > 100:
            raise ValueNotInRange(
                message=f"{value} -> The value must be between 0 and 100"
            )

        body = {"commands": [{"code": "temp_value_v2", "value": value * 10}]}
        device_id = self._device_id if device_id is None else device_id
        response = self._post(postfix=f"/devices/{device_id}/commands", body=body)

        return response

    def bright(self, value: int, device_id: str = None) -> dict:
        """
        Brightness level.

        :param str device_id: device id
        :param int value: percentage from 1 to 100
        :raise tuya_bulb_control.exceptions.ValueNotInRange: if the value is out of range
        :return: response dict or bool
        """

        if value < 1 or value > 100:
            raise ValueNotInRange(
                message=f"{value} -> The value must be between 1 and 100"
            )

        body = {"commands": [{"code": "bright_value_v2", "value": value * 10}]}
        device_id = self._device_id if device_id is None else device_id
        response = self._post(postfix=f"/devices/{device_id}/commands", body=body)

        return response

    def switch_timer(self, value: int, device_id: str = None) -> dict:
        """
        On or Off this device by timer.

        :param str device_id: device id
        :param value: minutes. From 0 to 1440 (24 hours). To cancel the timer, pass value=0
        :raise tuya_bulb_control.exceptions.ValueNotInRange: if the value is out of range
        :return: response dict or bool
        """

        if value > 1440:
            raise ValueNotInRange(
                message=f"{value} -> The value must be between 1 and 1440"
            )

        value = value * 60
        body = {"commands": [{"code": "countdown_1", "value": value}]}
        device_id = self._device_id if device_id is None else device_id
        response = self._post(postfix=f"/devices/{device_id}/commands", body=body)

        return response

    def blink(self, steps: int, device_id: str = None) -> dict:
        """
        Blinks the set numbers of times.
        Running in line.

        :param str device_id: device id
        :param int steps: number of blinks
        :return: response dict or bool
        """
        steps = steps * 2
        steps = steps if steps % 2 == 0 else steps + 1
        device_id = self._device_id if device_id is None else device_id
        request_status = None

        for _ in range(steps):
            request_status = self.switch(device_id=device_id)

        return request_status
