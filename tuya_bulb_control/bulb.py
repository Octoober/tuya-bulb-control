#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import colorsys
from ._tuya_api import _TuyaApi
from .exceptions import ModeNotSupported, FunctionNotSupported, ArgumentError


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
        super().__init__(
            client_id=client_id, secret_key=secret_key, region_key=region_key
        )
        self._device_id = device_id

    def _function_exists(self, code_name: str, device_id: str) -> bool:
        """
        Check if a functions exists.
        Use KeyError exception to catch error.

        :param code_name: function name
        :param device_id: device id
        :raise FunctionNotSupported: if function not supported
        :return: state
        """
        functions = self.functions(device_id=device_id)

        try:
            state = [True for item in functions if code_name == item["code"]][0]
        except (KeyError, IndexError):
            raise FunctionNotSupported(target=code_name)

        return state

    def _available_values(self, code_name: str, device_id: str):
        """
        Get all available values.

        :param code_name: function name
        :param device_id: device id
        :return: value
        """
        values = [
            item["values"]
            for item in self.functions(device_id=device_id)
            if item["code"] == code_name
        ][0]

        return values

    def _template(
        self,
        value: int,
        code_name: str,
        device_id: str,
    ) -> dict:
        """
        Brightness level for multi-version.

        :param value:
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :raise tuya_bulb_control.exceptions.ValueNotInRange: if the value is out of range
        :return: response dict or bool
        """
        device_id = self._check_device_id(device_id)

        body = {"commands": [{"code": code_name, "value": value}]}
        response = self._post(postfix=f"/devices/{device_id}/commands", body=body)

        return response

    def _check_device_id(self, device_id: str) -> str:
        """
        Check device id.

        :param device_id: device id
        :return: current device id
        :raise ArgumentError: if device_id is empty
        """
        device_id = self._device_id if device_id is None else device_id

        if not device_id:
            raise ArgumentError(
                target=device_id, msg="Argument device_id must not be empty."
            )

        return device_id

    @staticmethod
    def _make_body(code_name: str, value) -> dict:
        """
        Template for requests.

        :param code_name: code name
        :param value: value
        :return:
        """
        body = {
            "commands": [
                {
                    "code": code_name,
                    "value": value,
                }
            ]
        }

        return body

    def set_work_mode(
        self, mode_name: str, check: bool = True, device_id: str = None
    ) -> dict:
        """
        Select work mode.
        You can get a list of mods from tuya_bulb_control.Bulb.functions()
        Uses code: work_mode

        :param mode_name: mode name. For example: white; colour; scene; music
        :param check: check if your device supports this mode.
            Default: True == Always check. Set to False if you are sure the device supports the mode.
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :raise KeyError: if the bulb doesn't support work mode
        :raise tuya_bulb_control.exceptions.ModeNotExists: if work mode doesn't exist
        :return: response dict
        """
        code_name = "work_mode"
        device_id = self._check_device_id(device_id)

        if not check:
            self._function_exists(code_name=code_name, device_id=device_id)
            available_values = json.loads(
                self._available_values(code_name=code_name, device_id=device_id)
            )["range"]

            if not [item for item in available_values if item == mode_name]:
                raise ModeNotSupported(target=mode_name)

        body = self._make_body(code_name=code_name, value=mode_name)
        response = self._post(f"/devices/{device_id}/commands", body=body)

        return response

    def set_colour(self, rgb: tuple, check: bool = None, device_id: str = None) -> dict:
        """
        Colour mode settings.
        Uses code: colour_data

        :param rgb: rgb coordinates
        :param check: check if your device supports this mode.
            Default: True == Always check. Set to False if you are sure the device supports the mode.
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :raise tuya_bulb_control.exceptions.ValueNotInRange: if the value is out of range
        :return: response dict
        """
        code_name = "colour_data"
        device_id = self._check_device_id(device_id)

        if not check:
            self._function_exists(code_name=code_name, device_id=device_id)

        h, s, v = colorsys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)

        body = self._make_body(code_name, {"h": h * 360, "s": s * 255, "v": v * 255})
        response = self._post(postfix=f"/devices/{device_id}/commands", body=body)

        return response

    def set_colour_v2(
        self, rgb: tuple, check: bool = None, device_id: str = None
    ) -> dict:
        """
        Colour mode settings.
        Uses code: colour_data_v2

        :param rgb: rgb coordinates
        :param check: check if your device supports this mode.
            Default: True == Always check. Set to False if you are sure the device supports the mode.
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :raise tuya_bulb_control.exceptions.ValueNotInRange: if the value is out of range
        :return: response dict
        """
        code_name = "colour_data_v2"
        device_id = self._check_device_id(device_id)

        if not check:
            self._function_exists(code_name=code_name, device_id=device_id)

        h, s, v = colorsys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)

        body = self._make_body(
            code_name=code_name, value={"h": h * 360, "s": s * 1000, "v": v * 1000}
        )
        response = self._post(postfix=f"/devices/{device_id}/commands", body=body)

        return response

    def set_toggle(
        self, state: bool = None, check: bool = True, device_id: str = None
    ) -> dict:
        """
        Turn ON or OFF the bulb.
        Uses code: switch_led

        :param state: explicit status indication
        :param check: check if your device supports this mode.
            Default: True == Always check. Set to False if you are sure the device supports the mode.
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :return: response dict
        """
        code_name = "switch_led"
        device_id = self._check_device_id(device_id)

        if check:
            self._function_exists(code_name=code_name, device_id=device_id)

        if state is None:
            state = not self.current_value(code_name=code_name, device_id=device_id)

        body = self._make_body(code_name=code_name, value=state)
        response = self._post(postfix=f"/devices/{device_id}/commands", body=body)

        return response

    def set_toggle_timer(
        self, value: int, check: bool = None, device_id: str = None
    ) -> dict:
        """
        On or Off this device by timer.
        Uses code: countdown_1

        :param value: minutes. From 0-1440 (24 hours). To cancel the timer, pass value=0
        :param check: check if your device supports this mode.
            Default: True == Always check. Set to False if you are sure the device supports the mode.
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :raise tuya_bulb_control.exceptions.ValueNotInRange: if the value is out of range
        :return: response dict or bool
        """
        code_name = "countdown_1"
        device_id = self._check_device_id(device_id)

        if value > 1440:
            raise ValueError(f"{code_name} -> The value must be between 0-1440")

        if not check:
            self._function_exists(code_name=code_name, device_id=device_id)

        value = value * 60  # To seconds

        body = self._make_body(code_name=code_name, value=value)
        response = self._post(postfix=f"/devices/{device_id}/commands", body=body)

        return response

    def turn_on(self, check: bool = True, device_id: str = None) -> dict:
        """
        Turn ON the bulb.
        Uses code: switch_led

        :param check: check if your device supports this mode.
            Default: True == Always check. Set to False if you are sure the device supports the mode.
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :return: response status dict
        """

        device_id = self._check_device_id(device_id)
        response = self.set_toggle(state=True, check=check, device_id=device_id)

        return response

    def turn_off(self, check: bool = True, device_id: str = None) -> dict:
        """
        Turn OFF the bulb.
        Uses code: switch_led

        :param check: check if your device supports this mode.
            Default: True == Always check. Set to False if you are sure the device supports the mode.
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :return: response status dict
        """

        device_id = self._check_device_id(device_id)
        response = self.set_toggle(state=False, check=check, device_id=device_id)

        return response

    def set_colour_temp(
        self, value: int, check: bool = None, device_id: str = None
    ) -> dict:
        """
        Colour temperature.
        Uses code: temp_value

        :param value: percentage from 25-255. For example: 25 = warm or 255 = cold
        :param check: check if your device supports this mode.
            Default: True == Always check. Set to False if you are sure the device supports the mode.
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :raise tuya_bulb_control.exceptions.ValueNotInRange: if the value is out of range
        :return: response dict or bool
        """
        code_name = "temp_value"

        if value < 25 or value > 255:
            raise ValueError(f"{value} -> The value not in rage 25-255")

        if not check:
            self._function_exists(code_name=code_name, device_id=device_id)

        response = self._template(value=value, code_name=code_name, device_id=device_id)

        return response

    def set_colour_temp_v2(
        self, value: int, check: bool = None, device_id: str = None
    ) -> dict:
        """
        Colour temperature.
        Uses code: temp_value_v2

        :param value: percentage from 0-100. For example: 0 = warm or 100 = cold
        :param check: check if your device supports this mode.
            Default: True == Always check. Set to False if you are sure the device supports the mode.
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :raise tuya_bulb_control.exceptions.ValueNotInRange: if the value is out of range
        :return: response dict or bool
        """
        code_name = "temp_value_v2"

        if value < 0 or value > 100:
            raise ValueError(f"{value} -> The value not in rage 0-100")

        if not check:
            self._function_exists(code_name=code_name, device_id=device_id)

        response = self._template(
            value=value * 10, code_name=code_name, device_id=device_id
        )

        return response

    def set_bright(self, value: int, check: bool = None, device_id: str = None) -> dict:
        """
        Brightness level.
        Uses code: bright_value

        :param value: percentage from 25-255
        :param check: check if your device supports this mode.
            Default: True == Always check. Set to False if you are sure the device supports the mode.
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :raise tuya_bulb_control.exceptions.ValueNotInRange: if the value is out of range
        :return: response dict or bool
        """
        code_name = "bright_value"

        if value < 25 or value > 255:
            raise ValueError(f"{value} -> The value not in rage 25-255")

        if not check:
            self._function_exists(code_name=code_name, device_id=device_id)

        response = self._template(value=value, code_name=code_name, device_id=device_id)

        return response

    def set_bright_v2(
        self, value: int, check: bool = None, device_id: str = None
    ) -> dict:
        """
        Brightness level. v2 only.
        Uses code: bright_value_v2

        :param value: percentage from 1-100
        :param check: check if your device supports this mode.
            Default: True == Always check. Set to False if you are sure the device supports the mode.
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :raise tuya_bulb_control.exceptions.ValueNotInRange: if the value is out of range
        :return: response dict or bool
        """
        code_name = "bright_value_v2"

        if value < 1 or value > 100:
            raise ValueError(f"{value} -> The value not in rage 1-100")

        if not check:
            self._function_exists(code_name=code_name, device_id=device_id)

        response = self._template(
            value=value * 10, code_name=code_name, device_id=device_id
        )

        return response

    def state(self, device_id: str = None) -> dict:
        """
        Get all current state of the bulb.

        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :return: response status dict
        """
        device_id = self._check_device_id(device_id)
        response = self._get(postfix=f"/devices/{device_id}/status")["result"]

        return response

    def functions(self, device_id: str = None) -> dict:
        """
        Get all available functions for this bulb.

        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :return: response functions dict
        """
        device_id = self._check_device_id(device_id)
        response = self._get(f"/devices/{device_id}/functions")["result"]["functions"]

        return response

    def current_value(self, code_name: str, device_id: str = None):
        """
        Get value the selected function.

        :param code_name: name to find
        :param device_id: select device_id for this action only. tuya_bulb_control.Bulb(device_id) will be ignored
        :return: value
        """
        try:
            value = [
                item["value"]
                for item in self.state(device_id)
                if item["code"] == code_name
            ][0]
        except (IndexError, KeyError):
            raise FunctionNotSupported(target=code_name)

        return value
