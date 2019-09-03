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

from collections import Mapping
from numbers import Number

bytes_types = (bytes, bytearray)
integer_types = (int,)
str_types = (str,)
string_types = (bytes, str, bytearray)


def is_integer(value) -> bool:
    return isinstance(value, integer_types) and not isinstance(value, bool)


def is_bytes(value) -> bool:
    return isinstance(value, bytes_types)


def is_str(value) -> bool:
    return isinstance(value, str_types)


def is_boolean(value) -> bool:
    return isinstance(value, bool)


def is_dict(obj) -> bool:
    return isinstance(obj, Mapping)


def is_list(obj) -> bool:
    return isinstance(obj, list)


def is_tuple(obj) -> bool:
    return isinstance(obj, tuple)


def is_null(obj) -> bool:
    return obj is None


def is_number(obj) -> bool:
    return isinstance(obj, Number)
