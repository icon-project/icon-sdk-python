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

from hashlib import sha3_256
from base64 import b64encode
from IconService.wallet.wallet import Wallet
from IconService.libs.serializer import serialize
from IconService.builder.transaction_builder import Transaction
from IconService.utils import get_timestamp
from IconService.utils.hexadecimal import add_0x_prefix, convert_int_to_hex_str, convert_params_value_to_hex_str


class SignedTransaction:

    def __init__(self, transaction: Transaction, wallet: Wallet):
        """Converts raw transaction into the signed transaction object having a signature.

        :param transaction: A transaction object not having a signature field yet
        :param wallet: A wallet object
        """
        self.__signed_transaction_dict = self.to_dict(transaction, wallet)
        message_hash = sha3_256(serialize(self.__signed_transaction_dict)).digest()
        signature = wallet.sign(message_hash)
        self.__signed_transaction_dict["signature"] = b64encode(signature).decode()

    @property
    def signed_transaction_dict(self):
        return self.__signed_transaction_dict

    @staticmethod
    def to_dict(transaction, wallet: Wallet=None):
        """Converts an instance of the transaction into a dictionary"""
        dict_tx = {
            "version": convert_int_to_hex_str(transaction.version) if transaction.version else "0x3",
            "from": transaction.from_ if transaction.from_ else wallet.get_address(),
            "stepLimit": convert_int_to_hex_str(transaction.step_limit),
            "timestamp": convert_int_to_hex_str(transaction.timestamp) if transaction.timestamp else get_timestamp(),
            # Network ID ("0x1" for Main net, "0x2" for Test net, etc)
            "nid": convert_int_to_hex_str(transaction.nid) if transaction.nid else "0x1"
        }

        if transaction.to is not None:
            dict_tx["to"] = transaction.to

        # value can be 0
        if transaction.value is not None:
            dict_tx["value"] = convert_int_to_hex_str(transaction.value)

        if transaction.nonce is not None:
            dict_tx["nonce"] = convert_int_to_hex_str(transaction.nonce)

        if transaction.data_type is not None:
            dict_tx["dataType"] = transaction.data_type

        if transaction.data_type in ('deploy', 'call', 'message'):
            dict_tx["data"] = generate_data_value(transaction)
        return dict_tx


def generate_data_value(transaction):
    """
    Generates data value in transaction from the other data like content_type, content, method or params
    by data types such as deploy, call, message.
    """
    if transaction.data_type == "deploy":
        # Content's data type is bytes and return value is hex string prefixed with '0x'.
        data = {
            "contentType": transaction.content_type,
            "content": add_0x_prefix(transaction.content.hex())
        }
        # Params is an optional property.
        if transaction.params:
            data["params"] = convert_params_value_to_hex_str(transaction.params)
    elif transaction.data_type == "call":
        data = {"method": transaction.method}
        # Params is an optional property.
        if transaction.params:
            data["params"] = convert_params_value_to_hex_str(transaction.params)
    else:  # When data type is message
        data = add_0x_prefix(transaction.data.encode().hex())
    return data
