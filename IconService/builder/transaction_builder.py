# -*- coding: utf-8 -*-
# Copyright 2017-2018 ICON Foundation
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
    def __init__(self, from_, to, value, step_limit, nonce):
        self.__from = from_
        self.__to = to
        self.__value = value
        self.__step_limit = step_limit
        self.__nonce = nonce

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
    def nonce(self):
        return self.__nonce


class DeployTransaction(Transaction):
    """Subclass `DeployTransaction`, making a transaction object for deploying SCORE which is read-only."""
    def __init__(self, from_, to, value, step_limit, nonce, content_type, content, params):
        Transaction.__init__(self, from_, to, value, step_limit, nonce)
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
    def params(self):
        return self.__params


class CallTransaction(Transaction):
    """Subclass `CallTransaction`, making a transaction object for calling a method in SCORE which is read-only."""
    def __init__(self, from_, to, value, step_limit, nonce, method, params):
        Transaction.__init__(self, from_, to, value, step_limit, nonce)
        self.__method = method
        self.__params = params

    @property
    def method(self):
        return self.__method

    @property
    def params(self):
        return self.__params


class MessageTransaction(Transaction):
    """Subclass `MessageTransaction`, making a transaction object for sending a message which is read-only."""
    def __init__(self, from_, to, value, step_limit, nonce, data):
        Transaction.__init__(self, from_, to, value, step_limit, nonce)
        self.__data = data

    @property
    def data(self):
        return self.__data


class IcxTransactionBuilder:
    """Builder for `Transaction` object"""
    def from_(self, from_):
        self.from_ = from_
        return self

    def to(self, to):
        self.to = to
        return self

    def value(self, value):
        self.value = value
        return self

    def step_limit(self, step_limit):
        self.step_limit = step_limit
        return self

    def nonce(self, nonce):
        self.nonce = nonce
        return self

    def build(self) -> Transaction:
        return Transaction(self.from_, self.to, self.value, self.step_limit, self.nonce)


class DeployTransactionBuilder(IcxTransactionBuilder):
    """Builder for `DeployTransaction` object"""

    def content_type(self, content_type):
        self.content_type = content_type
        return self

    def content(self, content):
        self.content = content
        return self

    def params(self, params):
        self.params = params
        return self

    def build(self) -> DeployTransaction:
        return DeployTransaction(self.from_, self.to, self.value, self.step_limit, self.nonce, self.content_type, self.content, self.params)


class CallTransactionBuilder(IcxTransactionBuilder):
    """Builder for `CallTransaction` object"""
    def method(self, method):
        self.method = method
        return self

    def params(self, params):
        self.params = params
        return self

    def build(self) -> CallTransaction:
        return CallTransaction(self.from_, self.to, self.value, self.step_limit, self.nonce, self.method, self.params)


class MessageTransactionBuilder(IcxTransactionBuilder):
    """Builder for `MessageTransaction` object"""
    def data(self, data):
        self.data = data
        return self

    def build(self) -> MessageTransaction:
        return MessageTransaction(self.from_, self.to, self.value, self.step_limit, self.nonce, self.data)
