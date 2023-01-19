# -*- coding: utf-8 -*-
# Copyright 2020 ICON Foundation Inc.
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

from __future__ import annotations

from typing import Any

from ...wallet.wallet import Wallet

BASE_TYPES = {bool, bytes, int, str, Wallet}
TYPE_NAME_TO_TYPE = {_type.__name__: _type for _type in BASE_TYPES}


def is_base_type(value: type) -> bool:
    try:
        return value in BASE_TYPES
    except:
        return False


def name_to_type(type_name: str) -> type:
    return TYPE_NAME_TO_TYPE[type_name]


def isinstance_ex(value: Any, _type: type) -> bool:
    if not isinstance(value, _type):
        return False

    if type(value) is bool and _type is not bool:
        return False

    return True


def base_object_to_str(value: Any) -> str:
    if isinstance(value, Wallet):
        return value.get_address()
    elif isinstance(value, int):
        return hex(value)
    elif isinstance(value, bytes):
        return bytes_to_hex(value)
    elif isinstance(value, bool):
        return hex(value)
    elif isinstance(value, str):
        return value

    raise TypeError(f"Unsupported type: {type(value)}")


def object_to_str(value: Any) -> Any | None:
    if is_base_type(type(value)):
        return base_object_to_str(value)

    if isinstance(value, list):
        return [object_to_str(i) for i in value]

    if isinstance(value, dict):
        return {k: object_to_str(value[k]) for k in value}

    if value is None:
        return None

    raise TypeError(f"Unsupported type: {type(value)}")


def bytes_to_hex(value: bytes, prefix: str = "0x") -> str:
    return f"{prefix}{value.hex()}"
