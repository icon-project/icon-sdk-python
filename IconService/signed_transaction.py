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

from IconService.wallet.wallet import Wallet
from IconService.libs.serializer import serialize
from IconService.builder.transaction_builder import Transaction
from IconService.utils import get_timestamp


class SignedTransaction:

    def __init__(self, transaction, wallet: Wallet):
        self.__transaction = transaction
        self.__wallet = wallet
        self.__signed_transaction_dict = self.to_dict(transaction)
        message_hash_bytes = serialize(self.__signed_transaction_dict)
        self.__signed_transaction_dict["signature"] = wallet.sign_message(message_hash_bytes)

    @property
    def signed_transaction_dict(self):
        return self.__signed_transaction_dict

    @staticmethod
    def to_dict(transaction: Transaction):

        dict_tx = {
            "version": "0x3",
            "from": transaction.from_,
            "to": transaction.to,
            "stepLimit": transaction.step_limit,
            "timestamp": str(get_timestamp()),
            "nid": transaction.nid,
            "nonce": transaction.nonce,
            "signature": "",
            "dataType": transaction.data_type,
            "data": transaction.data
        }

        if not isinstance(transaction.nonce, str):
            del dict_tx['nonce']

        if not transaction.data_type:
            del dict_tx['dataType']

        if not transaction.data:
            del dict_tx['data']

        return dict_tx

