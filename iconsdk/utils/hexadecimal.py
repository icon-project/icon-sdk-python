# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module is reference to `hexadecimal`.
It is used for

- value starting with `0x`
- an address of a wallet starting with 'hx'
- an address of SCORE starting with 'cx'
"""
from re import match

from iconsdk.exception import DataTypeException
from iconsdk.utils.type import is_str


def is_0x_prefixed(value: str) -> bool:
    if not is_str(value):
        raise DataTypeException("Value type must be str. Got: {0}".format(repr(value)))
    return value.startswith('0x')


def remove_0x_prefix(value: str) -> str:
    if is_0x_prefixed(value):
        return value[2:]
    return value


def add_0x_prefix(value: str) -> str:
    if is_0x_prefixed(value):
        return value
    return '0x' + value


def is_hx_prefixed(value: str) -> bool:
    """Used for checking an address of a wallet."""
    if not is_str(value):
        raise DataTypeException("Value type must be str. Got: {0}.".format(repr(value)))
    return value.startswith('hx')


def remove_hx_prefix(value: str) -> str:
    if is_hx_prefixed(value):
        return value[2:]
    return value


def add_hx_prefix(value: str) -> str:
    if is_hx_prefixed(value):
        return value
    return 'hx' + value


def is_cx_prefixed(value: str) -> bool:
    """Used for checking an address of SCORE."""
    if not is_str(value):
        raise DataTypeException("Value type must be str. Got: {0}.".format(repr(value)))
    return value.startswith("cx")


def remove_cx_prefix(value: str) -> str:
    if is_cx_prefixed(value):
        return value[2:]
    return value


def add_cx_prefix(value: str) -> str:
    if is_cx_prefixed(value):
        return value
    return 'cx' + value


def is_lowercase_hex_string(value: str) -> bool:
    """Check whether value is hexadecimal format or not

    :param value: text
    :return: True(lowercase hexadecimal) otherwise False
    """
    try:
        result = None
        if isinstance(value, str):
            result = match('[0-9a-f]+', value)
        return result is not None and len(result.group(0)) == len(value)
    except Exception:
        raise DataTypeException("Not lowercase hex string. Get: {0}.".format(repr(value)))
