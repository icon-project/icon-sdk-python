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
from iconsdk.utils.convert_type import convert_params_value_to_hex_str


class Call:
    """
    Class `Call` for calling a SCORE API.
    Once an instance generated, it is read-only."""

    def __init__(self, from_: str, to: str, method: str, params: dict):
        self.__from = from_
        self.__to = to
        self.__method = method
        self.__params = params

    @property
    def from_(self) -> str:
        return self.__from

    @property
    def to(self) -> str:
        return self.__to

    @property
    def method(self) -> str:
        return self.__method

    @property
    def params(self) -> dict:
        return convert_params_value_to_hex_str(self.__params) if self.__params else None

    def to_dict(self) -> dict:
        return {"from_": self.from_, "to": self.to, "method": self.method, "params": self.params}


class CallBuilder:
    """
    Builder for a `Call` object.
    Once setting it, a value of any property can't be changed forever.
    """

    def __init__(self, from_: str = None, to: str = None, method: str = None, params: dict = None) -> Call:
        self._from_ = from_
        self._to = to
        self._method = method
        self._params = params

    def from_(self, from_: str) -> 'CallBuilder':
        self._from_ = from_
        return self

    def to(self, to: str) -> 'CallBuilder':
        self._to = to
        return self

    def method(self, method: str) -> 'CallBuilder':
        self._method = method
        return self

    def params(self, params: dict) -> 'CallBuilder':
        self._params = params
        return self

    def build(self) -> Call:
        return Call(self._from_, self._to, self._method, self._params)

    @classmethod
    def from_dict(cls, call_as_dict: dict) -> 'CallBuilder':
        """Returns a CallBuilder made from dict"""
        try:
            return cls(
                from_=call_as_dict['from_'] if "from_" in call_as_dict else None,
                to=call_as_dict['to'],
                method=call_as_dict['method'],
                params=call_as_dict['params'] if "params" in call_as_dict else None
            )
        except KeyError:
            raise DataTypeException("The input data invalid. Mapping key not found.")
