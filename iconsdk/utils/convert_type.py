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

from iconsdk.exception import DataTypeException
from iconsdk.utils.hexadecimal import add_0x_prefix, remove_0x_prefix
from iconsdk.utils.type import is_integer, is_bytes, is_str


def convert_int_to_hex_str(value: int) -> str:
    """Converts an integer to hex string prefixed with '0x'."""
    if is_integer(value):
        return hex(value)
    else:
        raise DataTypeException("Data type should be integer.")


def convert_bytes_to_hex_str(value: bytes) -> str:
    """Converts bytes to hex string prefixed with '0x'."""
    if is_bytes(value):
        return add_0x_prefix(value.hex())
    else:
        raise DataTypeException("Data type should be bytes.")


def convert_hex_str_to_int(value: str) -> int:
    """Converts hex string prefixed with '0x' into int."""
    if is_str(value):
        return int(value, 16)
    else:
        raise DataTypeException("Data type should be string.")


def convert_hex_str_to_bytes(value: str) -> bytes:
    """Converts hex string prefixed with '0x' into bytes."""
    if is_str(value):
        return bytes.fromhex(remove_0x_prefix(value))
    else:
        raise DataTypeException("Data type should be string.")
