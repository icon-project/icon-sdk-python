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

from enum import IntEnum, unique
from typing import Optional, Any


@unique
class IconServiceExceptionCode(IntEnum):
    """Result code enumeration"""
    OK = 0
    KEY_STORE_ERROR = 1
    ADDRESS_ERROR = 2
    BALANCE_ERROR = 3
    DATA_TYPE_ERROR = 4
    JSON_RPC_ERROR = 5
    ZIP_MEMORY_ERROR = 6
    URL_ERROR = 7

    def __str__(self) -> str:
        return str(self.name).capitalize().replace('_', ' ')


class IconServiceBaseException(BaseException):

    def __init__(self, message: Optional[str],code: IconServiceExceptionCode = IconServiceExceptionCode.OK):
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
        return f'{self.message}'


class KeyStoreException(IconServiceBaseException):
    """"Error when making or loading a keystore file."""

    def __init__(self, message: Optional[str]):
        super().__init__(message, IconServiceExceptionCode.KEY_STORE_ERROR)


class AddressException(IconServiceBaseException):
    """Error when having an invalid address."""

    def __init__(self, message: Optional[str]):
        super().__init__(message, IconServiceExceptionCode.ADDRESS_ERROR)


class BalanceException(IconServiceBaseException):
    """Error when having an invalid balance."""

    def __init__(self, message: Optional[str]):
        super().__init__(message, IconServiceExceptionCode.BALANCE_ERROR)


class DataTypeException(IconServiceBaseException):
    """Error when data type is invalid."""

    def __init__(self, message: Optional[str]):
        super().__init__(message, IconServiceExceptionCode.DATA_TYPE_ERROR)


class JSONRPCException(IconServiceBaseException):
    """Error when get JSON-RPC Error Response."""
    def __init__(self,
                 message: Optional[str],
                 code: Optional[int] = None,
                 data: Any = None,
                 ):
        super().__init__(message, IconServiceExceptionCode.JSON_RPC_ERROR)
        self.__code = code
        self.__data = data

    JSON_PARSE_ERROR            = -32700
    RPC_INVALID_REQUEST         = -32600
    RPC_METHOD_NOT_FOUND        = -32601
    RPC_INVALID_PARAMS          = -32602
    RPC_INTERNAL_ERROR          = -32603

    SYSTEM_ERROR                = -31000
    SYSTEM_POOL_OVERFLOW        = -31001
    SYSTEM_TX_PENDING           = -31002
    SYSTEM_TX_EXECUTING         = -31003
    SYSTEM_TX_NOT_FOUND         = -31004
    SYSTEM_LACK_OF_RESOURCE     = -31005
    SYSTEM_REQUEST_TIMEOUT      = -31006
    SYSTEM_HARD_TIMEOUT         = -31007

    @property
    def rpc_code(self) -> Optional[int]:
        return self.__code

    @property
    def rpc_data(self) -> Any:
        return self.__data

    def __repr__(self):
        return f"JSONRPCException(message={self.message!r},code={self.rpc_code},data={self.rpc_data})"

    @staticmethod
    def score_error(code):
        if code is None:
            return 0
        if -30000 > code > -31000:
            return -30000 - code
        return 0

class ZipException(IconServiceBaseException):
    """"Error while write zip in memory"""

    def __init__(self, message: Optional[str]):
        super().__init__(message, IconServiceExceptionCode.ZIP_MEMORY_ERROR)


class URLException(IconServiceBaseException):
    """Error regarding invalid URL"""

    def __init__(self, message: Optional[str]):
        super().__init__(message, IconServiceExceptionCode.URL_ERROR)

class HTTPError(IconServiceBaseException):
    """"Error regarding HTTP Error"""
    def __init__(self, message: str, status: int):
        super().__init__(message, IconServiceExceptionCode.JSON_RPC_ERROR)
        self.__status = status

    @property
    def status(self):
        return self.__status

    @property
    def ok(self):
        return 0 <= self.__status < 300

    def __repr__(self):
        return f'HTTPError(message={self.message!r}, status={self.status!r})'
