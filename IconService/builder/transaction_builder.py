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


class Transaction:
    """Super class `Transaction` which is read-only."""

    def __init__(self, from_: str, to: str, value: int, step_limit: int, nid: int, nonce: int, version: int,
                 timestamp: int):
        self.__from = from_
        self.__to = to
        self.__value = value
        self.__step_limit = step_limit
        self.__nid = nid
        self.__nonce = nonce
        self.__version = version
        self.__timestamp = timestamp


    @property
    def from_(self):
        return self.__from

    @property
    def to(self):
        return self.__to

    @property
    def value(self):
        return self.__value

    @property
    def step_limit(self):
        return self.__step_limit

    @property
    def nid(self):
        return self.__nid

    @property
    def nonce(self):
        return self.__nonce

    @property
    def version(self):
        return self.__version

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def data_type(self):
        return None

    @property
    def data(self):
        return None


class DeployTransaction(Transaction):
    """Subclass `DeployTransaction`, making a transaction object for deploying SCORE which is read-only."""
    def __init__(self, from_: str, to: str, value: int, step_limit: int, nid: int, nonce: int, version: int,
                 timestamp: int, content_type: str, content: bytes, params: dict):
        Transaction.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
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
    def params(self):
        return self.__params


class CallTransaction(Transaction):
    """Subclass `CallTransaction`, making a transaction object for calling a method in SCORE which is read-only."""
    def __init__(self, from_: str, to: str, value: int, step_limit: int, nid: int, nonce: int,
                 version: int, timestamp: int, method: str, params: dict):
        Transaction.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
        self.__method = method
        self.__params = params

    @property
    def method(self):
        return self.__method

    @property
    def data_type(self):
        return "call"

    @property
    def params(self):
        return self.__params


class MessageTransaction(Transaction):
    """Subclass `MessageTransaction`, making a transaction object for sending a message which is read-only."""
    def __init__(self, from_: str, to: str, value: int, step_limit: int, nid: int, nonce: int, version: int,
                 timestamp: int, data: str):
        Transaction.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
        self.__data = data

    @property
    def data_type(self):
        return "message"

    @property
    def data(self):
        return self.__data


class TransactionBuilder:
    """Builder for `Transaction` object"""

    def __init__(self, from_: str=None, to: str=None, value: int=None, step_limit: int=None, nid: int=None,
                 nonce: int=None, version: int=None, timestamp: int=None):
        self._from_ = from_
        self._to = to
        self._value = value
        self._step_limit = step_limit
        self._nid = nid
        self._nonce = nonce
        self._version = version
        self._timestamp = timestamp

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

    def version(self, version):
        self._version = version
        return self

    def timestamp(self, timestamp):
        self._timestamp = timestamp
        return self

    def build(self) -> Transaction:
        return Transaction(self._from_, self._to, self._value, self._step_limit, self._nid, self._nonce, self._version,
                           self._timestamp)


class DeployTransactionBuilder(TransactionBuilder):
    """Builder for `DeployTransaction` object"""

    def __init__(self, from_: str=None, to: str=None, value: int=None, step_limit: int=None, nid: int=None,
                 nonce: int=None, version: int=None, timestamp: int=None, content_type: str=None, content: bytes=None,
                 params: dict=None):
        TransactionBuilder.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
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
        return DeployTransaction(self._from_, self._to, None, self._step_limit, self._nid, self._nonce, self._version,
                                 self._timestamp, self._content_type, self._content, self._params)


class CallTransactionBuilder(TransactionBuilder):
    """Builder for `CallTransaction` object"""

    def __init__(self, from_: str=None, to: str=None, value: int=None, step_limit: int=None, nid: int=None,
                 nonce: int=None, version: int=None, timestamp: int=None, method: str=None, params: dict =None):
        TransactionBuilder.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
        self._method = method
        self._params = params

    def method(self, method):
        self._method = method
        return self

    def params(self, params):
        self._params = params
        return self

    def build(self) -> CallTransaction:
        return CallTransaction(self._from_, self._to, None, self._step_limit, self._nid, self._nonce, self._version,
                               self._timestamp, self._method, self._params)


class MessageTransactionBuilder(TransactionBuilder):
    """Builder for `MessageTransaction` object"""
    def __init__(self, from_: str=None, to: str=None, value: int=None, step_limit: int=None, nid: int=None,
                 nonce: int=None, version: int=None, timestamp: int=None, data: str=None):
        TransactionBuilder.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
        self._data = data

    def data(self, data):
        self._data = data
        return self

    def build(self) -> MessageTransaction:
        return MessageTransaction(self._from_, self._to, None, self._step_limit, self._nid, self._nonce, self._version,
                                  self._timestamp, self._data)
