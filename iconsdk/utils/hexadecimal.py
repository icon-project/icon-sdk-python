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

from iconsdk.utils.type import is_str, is_integer, is_bytes
from iconsdk.exception import DataTypeException


def is_0x_prefixed(value):
    if not is_str(value):
        raise DataTypeException("Value type must be str. Got: {0}".format(repr(value)))
    return value.startswith('0x')


def remove_0x_prefix(value):
    if is_0x_prefixed(value):
        return value[2:]
    return value


def add_0x_prefix(value):
    if is_0x_prefixed(value):
        return value
    return '0x' + value


def is_hx_prefixed(value):
    """Used for checking an address of a wallet."""
    if not is_str(value):
        raise DataTypeException("Value type must be str. Got: {0}.".format(repr(value)))
    return value.startswith('hx')


def remove_hx_prefix(value):
    if is_hx_prefixed(value):
        return value[2:]
    return value


def add_hx_prefix(value):
    if is_hx_prefixed(value):
        return value
    return 'hx' + value


def is_cx_prefixed(value):
    """Used for checking an address of SCORE."""
    if not is_str(value):
        raise DataTypeException("Value type must be str. Got: {0}.".format(repr(value)))
    return value.startswith("cx")


def remove_cx_prefix(value):
    if is_cx_prefixed(value):
        return value[2:]
    return value


def add_cx_prefix(value):
    if is_cx_prefixed(value):
        return value
    return 'cx' + value


def convert_int_to_hex_str(value: int):
    try:
        if is_integer(value):
            return add_0x_prefix(hex(value))
        else:
            raise DataTypeException("Data's type should be integer.")
    except KeyError:
        raise DataTypeException("Data type is wrong.")


def convert_bytes_to_hex_str(value: bytes):
    try:
        if is_bytes(value):
            return add_0x_prefix(value.hex())
        else:
            raise DataTypeException("Data's type should be bytes.")
    except KeyError:
        raise DataTypeException("Data type is wrong.")


def convert_params_value_to_hex_str(params: dict):
    """Converts params' values into hex str prefixed with '0x'."""
    new_params = params
    for key, value in params.items():
        if isinstance(value, int):
            new_params[key] = convert_int_to_hex_str(value)
        elif isinstance(value, bytes):
            new_params[key] = convert_bytes_to_hex_str(value)
    return new_params
