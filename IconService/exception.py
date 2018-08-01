# -*- coding: utf-8 -*-
# Copyright 2017-2018 theloop Inc.
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
from typing import Optional
from enum import IntEnum, unique


@unique
class IconServiceExceptionCode(IntEnum):
    """Result code enumeration"""
    OK = 0
    KEY_STORE_ERROR = 1
    ADDRESS_ERROR = 2
    BALANCE_ERROR = 3

    def __str__(self) -> str:
        return str(self.name).capitalize().replace('_', ' ')


class IonServiceBaseException(BaseException):

    def __init__(self, message: Optional[str], code: IconServiceExceptionCode = IconServiceExceptionCode.OK):
        if message is None:
            message = str(code)
        self.__message = message
        self.__code = code

    @property
    def message(self):
        return self.__message

    @property
    def code(self):
        return self.__code

    def __str__(self):
        return f'{self.message} ({str(self.code)})'


class KeyStoreException(IonServiceBaseException):
    """"Error when making or loading a keystore file."""
    def __init__(self, message: Optional[str]):
        super().__init__(message, IconServiceExceptionCode.KEY_STORE_ERROR)


class AddressException(IonServiceBaseException):
    """Error when having an invalid address."""
    def __init__(self, message: Optional[str]):
        super().__init__(message, IconServiceExceptionCode.ADDRESS_ERROR)


class BalanceException(IonServiceBaseException):
    """Error when having an invalid balance."""
    def __init__(self, message: Optional[str]):
        super().__init__(message, IconServiceExceptionCode.BALANCE_ERROR)
