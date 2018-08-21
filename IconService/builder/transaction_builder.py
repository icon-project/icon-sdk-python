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

from IconService.utils.hexadecimal import add_0x_prefix, convert_int_to_hex_str


class Transaction:
    """Super class `Transaction` which is read-only."""
    def __init__(self, from_, to, value, step_limit, nid, nonce=None):
        self.__from = from_
        self.__to = to
        self.__value = value
        self.__step_limit = step_limit
        self.__nid = nid
        self.__nonce = nonce

    @property
    def from_(self):
        return self.__from

    @property
    def to(self):
        return self.__to

    @property
    def value(self):
        return convert_int_to_hex_str(self.__value) if self.__value else self.__value

    @property
    def step_limit(self):
        return convert_int_to_hex_str(self.__step_limit) if self.__step_limit else self.__step_limit

    @property
    def nid(self):
        return convert_int_to_hex_str(self.__nid) if self.__nid else self.__nid

    @property
    def nonce(self):
        return convert_int_to_hex_str(self.__nonce) if self.__nonce else self.__nonce

    @property
    def data_type(self):
        return None

    @property
    def data(self):
        return None


class DeployTransaction(Transaction):
    """Subclass `DeployTransaction`, making a transaction object for deploying SCORE which is read-only."""
    def __init__(self, from_, to, value, step_limit, nid, nonce, content_type, content: bytes, params: dict):
        Transaction.__init__(self, from_, to, value, step_limit, nid, nonce)
        self.__content_type = content_type
        self.__content = content
        self.__params = params

    @property
    def content_type(self):
        return self.__content_type

    @property
    def content(self):
        return self.__content

    @property
    def data_type(self):
        return "deploy"

    @property
    def data(self):
        # Content's data type is bytes and return value is hex string prefixed with '0x'.
        data = {"contentType": self.__content_type,
                "content": add_0x_prefix(self.__content.hex())}
        # Params is an optional property which is parameters of methods, on_install() and on_update().
        if self.__params:
            data["params"]: self.__params
        return data


class CallTransaction(Transaction):
    """Subclass `CallTransaction`, making a transaction object for calling a method in SCORE which is read-only."""
    def __init__(self, from_, to, value, step_limit, nid, nonce, method, params: dict):
        Transaction.__init__(self, from_, to, value, step_limit, nid, nonce)
        self.__method = method
        self.__params = params

    @property
    def method(self):
        return self.__method

    @property
    def data_type(self):
        return "call"

    @property
    def data(self):
        data = {"method": self.__method}
        # params is optional property
        if self.__params:
            data["params"] = self.__params
        return data


class MessageTransaction(Transaction):
    """Subclass `MessageTransaction`, making a transaction object for sending a message which is read-only."""
    def __init__(self, from_, to, value, step_limit, nid, nonce, data: str):
        # data's type is str and return value is hex string prefixed with '0x'
        Transaction.__init__(self, from_, to, value, step_limit, nid, nonce)
        self.__data = data

    @property
    def data_type(self):
        return "message"

    @property
    def data(self):
        return add_0x_prefix(self.__data.encode().hex())


class IcxTransactionBuilder:
    """Builder for `Transaction` object"""

    def __init__(self, from_=None, to=None, value=None, step_limit=None, nid=None, nonce=None):
        self._from_ = from_
        self._to = to
        self._value = value
        self._step_limit = step_limit
        self._nid = nid
        self._nonce = nonce

    def from_(self, from_):
        self._from_ = from_
        return self

    def to(self, to):
        self._to = to
        return self

    def value(self, value):
        self._value = value
        return self

    def step_limit(self, step_limit):
        self._step_limit = step_limit
        return self

    def nid(self, nid):
        self._nid = nid
        return self

    def nonce(self, nonce):
        self._nonce = nonce
        return self

    def build(self) -> Transaction:
        return Transaction(self._from_, self._to, self._value, self._step_limit, self._nid, self._nonce)


class DeployTransactionBuilder(IcxTransactionBuilder):
    """Builder for `DeployTransaction` object"""

    def __init__(self, from_=None, to=None, value=None, step_limit=None, nid=None, nonce=None,
                 content_type=None, content: bytes=None, params=None):
        IcxTransactionBuilder.__init__(self, from_, to, value, step_limit, nid, nonce)
        self._content_type = content_type
        self._content = content
        self._params = params

    def content_type(self, content_type):
        self._content_type = content_type
        return self

    def content(self, content):
        self._content = content
        return self

    def params(self, params):
        self._params = params
        return self

    def build(self) -> DeployTransaction:
        return DeployTransaction(self._from_, self._to, None, self._step_limit, self._nid, self._nonce,
                                 self._content_type, self._content, self._params)


class CallTransactionBuilder(IcxTransactionBuilder):
    """Builder for `CallTransaction` object"""

    def __init__(self, from_=None, to=None, value=None, step_limit=None, nid=None, nonce=None,
                 method=None, params: dict =None):
        IcxTransactionBuilder.__init__(self, from_, to, value, step_limit, nid, nonce)
        self._method = method
        self._params = params

    def method(self, method):
        self._method = method
        return self

    def params(self, params):
        self._params = params
        return self

    def build(self) -> CallTransaction:
        return CallTransaction(self._from_, self._to, None, self._step_limit, self._nid, self._nonce,
                               self._method, self._params)


class MessageTransactionBuilder(IcxTransactionBuilder):
    """Builder for `MessageTransaction` object"""
    def __init__(self, from_=None, to=None, value=None, step_limit=None, nid=None, nonce=None,
                 data=None):
        IcxTransactionBuilder.__init__(self, from_, to, value, step_limit, nid, nonce)
        self._data = data

    def data(self, data):
        self._data = data
        return self

    def build(self) -> MessageTransaction:
        return MessageTransaction(self._from_, self._to, None, self._step_limit, self._nid, self._nonce,
                                  self._data)
