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
from iconsdk.utils.hexadecimal import remove_0x_prefix, is_0x_prefixed, is_lowercase_hex_string


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
    def from_(self) -> str:
        return self.__from

    @property
    def to(self) -> str:
        return self.__to

    @property
    def value(self) -> int:
        return self.__value

    @property
    def step_limit(self) -> int:
        return self.__step_limit

    @step_limit.setter
    def step_limit(self, step_limit: int):
        self.__step_limit = step_limit

    @property
    def nid(self) -> int:
        return self.__nid

    @property
    def nonce(self) -> int:
        return self.__nonce

    @property
    def version(self) -> int:
        return self.__version

    @property
    def timestamp(self) -> int:
        return self.__timestamp

    @property
    def data_type(self):
        return None

    @property
    def data(self):
        return None

    def to_dict(self) -> dict:
        return {"from_": self.from_, "to": self.to, "value": self.value, "step_limit": self.step_limit, "nid": self.nid,
                "nonce": self.nonce, "version": self.version, "timestamp": self.timestamp}


class DeployTransaction(Transaction):
    """Subclass `DeployTransaction`, making a transaction object for deploying SCORE which is read-only."""

    def __init__(self, from_: str, to: str, value: int, step_limit: int, nid: int, nonce: int, version: int,
                 timestamp: int, content_type: str, content: bytes, params: dict):
        Transaction.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
        self.__content_type = content_type

        # Content should not be empty.
        if not content:
            raise DataTypeException("Content type should be bytes.")

        self.__content = content
        self.__params = params

    @property
    def content_type(self) -> str:
        return self.__content_type

    @property
    def content(self) -> bytes:
        return self.__content

    @property
    def data_type(self) -> str:
        return "deploy"

    @property
    def params(self) -> dict:
        return self.__params

    def to_dict(self) -> dict:
        transaction_as_dict = super().to_dict()
        transaction_as_dict.update({"content_type": self.content_type, "content": self.content,
                                    "data_type": self.data_type, "params": self.params})
        return transaction_as_dict


class CallTransaction(Transaction):
    """Subclass `CallTransaction`, making a transaction object for calling a method in SCORE which is read-only."""

    def __init__(self, from_: str, to: str, value: int, step_limit: int, nid: int, nonce: int,
                 version: int, timestamp: int, method: str, params: dict):
        Transaction.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
        self.__method = method
        self.__params = params

    @property
    def method(self) -> str:
        return self.__method

    @property
    def data_type(self) -> str:
        return "call"

    @property
    def params(self) -> dict:
        return self.__params

    def to_dict(self) -> dict:
        transaction_as_dict = super().to_dict()
        transaction_as_dict.update({"method": self.method, "data_type": self.data_type, "params": self.params})
        return transaction_as_dict


class MessageTransaction(Transaction):
    """Subclass `MessageTransaction`, making a transaction object for sending a message which is read-only."""

    def __init__(self, from_: str, to: str, value: int, step_limit: int, nid: int, nonce: int, version: int,
                 timestamp: int, data: str):
        Transaction.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)

        if is_0x_prefixed(data) and is_lowercase_hex_string(remove_0x_prefix(data)):
            self.__data = data
        else:
            raise DataTypeException("Message data should be hex string prefixed with '0x'.")

    @property
    def data_type(self) -> str:
        return "message"

    @property
    def data(self) -> str:
        return self.__data

    def to_dict(self) -> dict:
        transaction_as_dict = super().to_dict()
        transaction_as_dict.update({"data_type": self.data_type, "data": self.data})
        return transaction_as_dict


class DepositTransaction(Transaction):
    """Subclass `DepositTransaction`, making a transaction object for depositing  and withdrawing"""

    def __init__(self, from_: str, to: str, value: int, step_limit: int, nid: int, nonce: int, version: int,
                 timestamp: int, action: str, id: str):
        Transaction.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
        self.__action = action
        self.__id = id

    @property
    def data_type(self) -> str:
        return "deposit"

    @property
    def action(self) -> str:
        return self.__action

    @property
    def id(self) -> str:
        return self.__id

    def to_dict(self) -> dict:
        transaction_as_dict = super().to_dict()
        transaction_as_dict.update({"data_type": self.data_type, "action": self.action, "id": self.id})
        return transaction_as_dict


class TransactionBuilder:
    """Builder for `Transaction` object"""

    def __init__(self, from_: str = None, to: str = None, value: int = None, step_limit: int = None, nid: int = None,
                 nonce: int = None, version: int = None, timestamp: int = None):
        self._from_ = from_
        self._to = to
        self._value = value
        self._step_limit = step_limit
        self._nid = nid
        self._nonce = nonce
        self._version = version
        self._timestamp = timestamp

    def from_(self, from_: str) -> 'TransactionBuilder':
        self._from_ = from_
        return self

    def to(self, to: str) -> 'TransactionBuilder':
        self._to = to
        return self

    def value(self, value: int) -> 'TransactionBuilder':
        self._value = value
        return self

    def step_limit(self, step_limit: int) -> 'TransactionBuilder':
        self._step_limit = step_limit
        return self

    def nid(self, nid: int) -> 'TransactionBuilder':
        self._nid = nid
        return self

    def nonce(self, nonce: int) -> 'TransactionBuilder':
        self._nonce = nonce
        return self

    def version(self, version: int) -> 'TransactionBuilder':
        self._version = version
        return self

    def timestamp(self, timestamp: int) -> 'TransactionBuilder':
        self._timestamp = timestamp
        return self

    def build(self) -> Transaction:
        if not self._to:
            raise DataTypeException("'to' should be required.")
        return Transaction(self._from_, self._to, self._value, self._step_limit, self._nid, self._nonce, self._version,
                           self._timestamp)

    @classmethod
    def from_dict(cls, transaction_as_dict: dict) -> 'TransactionBuilder':
        """Returns a TransactionBuilder made from dict"""
        try:
            return cls(
                from_=transaction_as_dict['from_'] if "from_" in transaction_as_dict else None,
                to=transaction_as_dict['to'],
                value=transaction_as_dict['value'] if "value" in transaction_as_dict else None,
                step_limit=transaction_as_dict['step_limit'] if "step_limit" in transaction_as_dict else None,
                nid=transaction_as_dict['nid'] if 'nid' in transaction_as_dict else None,
                nonce=transaction_as_dict["nonce"] if "nonce" in transaction_as_dict else None,
                version=transaction_as_dict["version"] if "version" in transaction_as_dict else None,
                timestamp=transaction_as_dict["timestamp"] if "timestamp" in transaction_as_dict else None
            )
        except KeyError:
            raise DataTypeException("The input data invalid. Mapping key not found.")


class DeployTransactionBuilder(TransactionBuilder):
    """Builder for `DeployTransaction` object"""

    def __init__(self, from_: str = None, to: str = None, value: int = None, step_limit: int = None, nid: int = None,
                 nonce: int = None, version: int = None, timestamp: int = None, content_type: str = None,
                 content: bytes = None,
                 params: dict = None):
        TransactionBuilder.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
        self._content_type = content_type
        self._content = content
        self._params = params

    def content_type(self, content_type: str) -> 'DeployTransactionBuilder':
        self._content_type = content_type
        return self

    def content(self, content: bytes) -> 'DeployTransactionBuilder':
        self._content = content
        return self

    def params(self, params: dict) -> 'DeployTransactionBuilder':
        self._params = params
        return self

    def build(self) -> DeployTransaction:
        if not self._content_type or not self._content:
            raise DataTypeException("'content_type' and 'content' should be required.")
        return DeployTransaction(self._from_, self._to, None, self._step_limit, self._nid, self._nonce, self._version,
                                 self._timestamp, self._content_type, self._content, self._params)

    @classmethod
    def from_dict(cls, transaction_as_dict: dict) -> 'DeployTransactionBuilder':
        """Returns a DeployTransactionBuilder made from dict"""
        try:
            cls = super().from_dict(transaction_as_dict)
            cls.content(transaction_as_dict['content'])
            cls.content_type(transaction_as_dict['content_type'])
            cls.params(transaction_as_dict['params'] if "params" in transaction_as_dict else None)
            return cls
        except KeyError:
            raise DataTypeException("The input data invalid. Mapping key not found.")


class CallTransactionBuilder(TransactionBuilder):
    """Builder for `CallTransaction` object"""

    def __init__(self, from_: str = None, to: str = None, value: int = None, step_limit: int = None, nid: int = None,
                 nonce: int = None, version: int = None, timestamp: int = None, method: str = None,
                 params: dict = None):
        TransactionBuilder.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
        self._method = method
        self._params = params

    def method(self, method: str) -> 'CallTransactionBuilder':
        self._method = method
        return self

    def params(self, params: dict) -> 'CallTransactionBuilder':
        self._params = params
        return self

    def build(self) -> CallTransaction:
        if not self._method:
            raise DataTypeException("'method' should be required.")
        return CallTransaction(self._from_, self._to, self._value, self._step_limit, self._nid, self._nonce,
                               self._version, self._timestamp, self._method, self._params)

    @classmethod
    def from_dict(cls, transaction_as_dict: dict) -> 'CallTransactionBuilder':
        """Returns a CallTransactionBuilder made from dict"""
        try:
            cls = super().from_dict(transaction_as_dict)
            cls.method(transaction_as_dict["method"])
            cls.params(transaction_as_dict["params"] if "params" in transaction_as_dict else None)
            return cls
        except KeyError:
            raise DataTypeException("The input data invalid. Mapping key not found.")


class MessageTransactionBuilder(TransactionBuilder):
    """Builder for `MessageTransaction` object"""

    def __init__(self, from_: str = None, to: str = None, value: int = None, step_limit: int = None, nid: int = None,
                 nonce: int = None, version: int = None, timestamp: int = None, data: str = None):
        TransactionBuilder.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
        self._data = data

    def data(self, data: str) -> 'MessageTransactionBuilder':
        self._data = data
        return self

    def build(self) -> MessageTransaction:
        if not self._data:
            raise DataTypeException("'data' should be required.")
        return MessageTransaction(self._from_, self._to, self._value, self._step_limit, self._nid, self._nonce,
                                  self._version,
                                  self._timestamp, self._data)

    @classmethod
    def from_dict(cls, transaction_as_dict: dict) -> 'MessageTransactionBuilder':
        """Returns a MessageTransactionBuilder made from dict"""
        try:
            cls = super().from_dict(transaction_as_dict)
            cls.data(transaction_as_dict["data"])
            return cls
        except KeyError:
            raise DataTypeException("The input data invalid. Mapping key not found.")


class DepositTransactionBuilder(TransactionBuilder):
    """Builder for `DepositTransaction` object"""

    def __init__(self, from_: str = None, to: str = None, value: int = None, step_limit: int = None, nid: int = None,
                 nonce: int = None, version: int = None, timestamp: int = None, action: str = None, id: str = None):
        TransactionBuilder.__init__(self, from_, to, value, step_limit, nid, nonce, version, timestamp)
        self._action = action
        self._id = id

    def action(self, action: str) -> 'DepositTransactionBuilder':
        self._action = action
        return self

    def id(self, id: str) -> 'DepositTransactionBuilder':
        self._id = id
        return self

    def build(self) -> DepositTransaction:
        if not self._action:
            raise DataTypeException("'action' should be provided. Available values are 'add' or 'withdraw'.")
        if self._action == "withdraw":
            if not self._id:
                raise DataTypeException("When action is 'withdraw', 'id' should be provided.")
            if self._value:
                raise DataTypeException("When action is 'withdraw'. 'value' should not be provided.")
        if self._action == "add" and not self._value:
            raise DataTypeException("When action is 'add', 'value' should be provided.")
        return DepositTransaction(self._from_, self._to, self._value, self._step_limit, self._nid, self._nonce,
                                  self._version, self._timestamp, self._action, self._id)

    @classmethod
    def from_dict(cls, transaction_as_dict: dict) -> 'DepositTransactionBuilder':
        """Returns a DepositTransactionBuilder made from dict"""
        try:
            cls = super().from_dict(transaction_as_dict)
            cls.action(transaction_as_dict["action"])
            cls.id(transaction_as_dict["id"] if "id" in transaction_as_dict else None)
            return cls
        except KeyError:
            raise DataTypeException("The input data invalid. Mapping key not found.")
