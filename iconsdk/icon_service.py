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

from iconsdk.builder.call_builder import Call
from iconsdk.builder.transaction_builder import Transaction
from iconsdk.converter import convert_block, convert_transaction, convert_transaction_result
from iconsdk.exception import AddressException, DataTypeException
from iconsdk.providers.provider import Provider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils import get_timestamp
from iconsdk.utils.convert_type import convert_int_to_hex_str
from iconsdk.utils.gen_tx_data import generate_data_value
from iconsdk.utils.hexadecimal import add_0x_prefix, remove_0x_prefix
from iconsdk.utils.validation import (
    is_block_height,
    is_hex_block_hash,
    is_predefined_block_value,
    is_score_address,
    is_wallet_address,
    is_T_HASH
)


class IconService:
    """
    The IconService class contains a set of API methods.
    It accepts a HTTPProvider which serves the purpose of 
    connecting to HTTP and HTTPS based JSON-RPC servers.
    """

    def __init__(self, provider: Provider):
        self.__provider = provider

    def get_block(self, value):
        """
        If param is height,
            1. Returns block information by block height
            2. Delegates to icx_getBlockByHeight RPC method

        Or block hash,
            1. Returns block information by block hash
            2. Delegates to icx_getBlockByHash RPC method

        Or string value same as `latest`,
            1. Returns the last block information
            2. Delegates to icx_getLastBlock RPC method

        :param value:
            Integer of a block height
            or hash of a block prefixed with '0x'
            or `latest`
        :return result: Block data
        """
        # by height
        if is_block_height(value):
            params = {'height': add_0x_prefix(hex(value))}
            result = self.__provider.make_request('icx_getBlockByHeight', params)
        # by hash
        elif is_hex_block_hash(value):
            params = {'hash': value}
            result = self.__provider.make_request('icx_getBlockByHash', params)
        # by value
        elif is_predefined_block_value(value):
            result = self.__provider.make_request('icx_getLastBlock')
        else:
            raise DataTypeException("It's unrecognized block reference:{0!r}.".format(value))

        convert_block(result)
        return result

    def get_total_supply(self):
        """
        Returns total ICX coin supply that has been issued
        Delegates to icx_getTotalSupply RPC method

        :return: Total number of ICX coins issued
        """
        result = self.__provider.make_request('icx_getTotalSupply')
        return int(remove_0x_prefix(result), 16)

    def get_balance(self, address: str):
        """
        Returns the ICX balance of the given EOA or SCORE.
        Delegates to icx_getBalance RPC method.

        :param address: An address of EOA or SCORE. type(str)
        :return: Number of ICX coins
        """
        if is_score_address(address) or is_wallet_address(address):
            params = {'address': address}
            result = self.__provider.make_request('icx_getBalance', params)
            return int(remove_0x_prefix(result), 16)
        else:
            raise AddressException("Address is wrong.")

    def get_score_api(self, address: str):
        """
        Returns SCORE's external API list.
        Delegates to icx_getScoreApi RPC method.

        :param address: A SCORE address to be examined
        :return: A list of API methods of the SCORE and its information
        """
        if not is_score_address(address):
            raise AddressException("SCORE Address is wrong.")

        params = {'address': address}
        return self.__provider.make_request('icx_getScoreApi', params)

    def get_transaction_result(self, tx_hash: str):
        """
        Returns the transaction result requested by transaction hash.
        Delegates to icx_getTransactionResult RPC method.

        :param tx_hash: Hash of a transaction prefixed with '0x'
        :return A transaction result object
        """
        if not is_T_HASH(tx_hash):
            raise DataTypeException("This hash value is unrecognized.")

        params = {'txHash': tx_hash}
        result = self.__provider.make_request('icx_getTransactionResult', params)
        convert_transaction_result(result)
        return result

    def get_transaction(self, tx_hash: str):
        """
        Returns the transaction information requested by transaction hash.
        Delegates to icx_getTransactionByHash RPC method.

        :param tx_hash: Transaction hash prefixed with '0x'
        :return: Information about a transaction
        """
        if not is_T_HASH(tx_hash):
            raise DataTypeException("This hash value is unrecognized.")

        params = {'txHash': tx_hash}
        result = self.__provider.make_request('icx_getTransactionByHash', params)
        convert_transaction(result)
        return result

    def call(self, call: object):
        """
        Calls SCORE's external function which is read-only without creating a transaction on Loopchain.
        Delegates to icx_call RPC method.

        :param call: Call object made by CallBuilder
        :return: Values returned by the executed SCORE function
        """
        if not isinstance(call, Call):
            raise DataTypeException("Call object is unrecognized.")

        params = {
            "from": call.from_,
            "to": call.to,
            "dataType": "call",
            "data": {
                "method": call.method
            }
        }

        if isinstance(call.params, dict):
            params["data"]["params"] = call.params

        return self.__provider.make_request('icx_call', params)

    def send_transaction(self, signed_transaction: SignedTransaction):
        """
        Sends the transaction.
        Delegates to icx_sendTransaction RPC method.

        :param signed_transaction: A signed transaction object
        :return: Transaction hash prefixed with '0x'
        """
        params = signed_transaction.signed_transaction_dict
        return self.__provider.make_request('icx_sendTransaction', params)

    def estimate_step(self, transaction: Transaction) -> int:
        """
        Returns an estimated step of how much step is necessary to allow the transaction to complete.

        :param transaction: Transaction
        :return: an estimated step
        """
        if not isinstance(transaction, Transaction):
            raise DataTypeException("Transaction object is unrecognized.")

        params = {
            "version": convert_int_to_hex_str(transaction.version) if transaction.version else "0x3",
            "from": transaction.from_,
            "to": transaction.to,
            "timestamp": convert_int_to_hex_str(
                transaction.timestamp) if transaction.timestamp else get_timestamp(),
            "nid": convert_int_to_hex_str(transaction.nid) if transaction.nid else "0x1"
        }

        if transaction.value is not None:
            params["value"] = convert_int_to_hex_str(transaction.value)

        if transaction.nonce is not None:
            params["nonce"] = convert_int_to_hex_str(transaction.nonce)

        if transaction.data_type is not None:
            params["dataType"] = transaction.data_type

        if transaction.data_type in ('deploy', 'call'):
            params["data"] = generate_data_value(transaction)
        elif transaction.data_type == 'message':
            params["data"] = transaction.data

        result = self.__provider.make_request('debug_estimateStep', params)
        return int(result, 16)
