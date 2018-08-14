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

from IconService.utils.validation import is_block_height, \
    is_hex_block_hash, is_predefined_block_value, is_score_address, is_wallet_address, \
    is_T_HASH
from IconService.exception import AddressException, DataTypeException
from IconService.providers.provider import Provider
from IconService.utils.hexadecimal import add_0x_prefix, remove_0x_prefix
from IconService.builder.call_builder import Call
from IconService.signed_transaction import SignedTransaction


class IconService:

    def __init__(self, provider: Provider):
        self.__provider = provider

    def get_block(self, value: str):
        """
        If param is height, it is equivalent to icx_getBlockByHeight.
        Or block hash, it is equivalent to icx_getBlockByHash.
        Or string value same as `latest`, it is equivalent to icx_getLastBlock.

        :param value: height or hash or `latest`. type(str)
        :return result: block information.
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

        return result

    def get_total_supply(self):
        """It is equivalent to icx_getTotalSupply.

        :return:
        """
        result = self.__provider.make_request('icx_getTotalSupply')
        return int(remove_0x_prefix(result), 16)

    def get_balance(self, address: str):
        """
        It is equivalent to icx_getBalance.
        It is available to both SCORE address and wallet address.

        :param address: SCORE address or wallet address. type(str)
        :return response:
        """

        if is_score_address(address) or is_wallet_address(address):
            params = {'address': address}
            result = self.__provider.make_request('icx_getBalance', params)
            print(result)
            return int(remove_0x_prefix(result), 16)
        else:
            raise AddressException("Address is wrong.")

    def get_score_api(self, address: str):
        """It is equivalent to icx_getScoreApi.

        :param address: SCORE address
        :return response:
        """
        if is_score_address(address):
            params = {'address': address}
            return self.__provider.make_request('icx_getScoreApi', params)
        else:
            raise AddressException("SCORE Address is wrong.")

    def get_transaction_result(self, tx_hash: str):
        """It is equivalent to icx_getTransactionResult.

        :param tx_hash: transaction hash prefixed with `0x`. type(str)
        :return response:
        """
        if is_T_HASH(tx_hash):
            params = {'txHash': tx_hash}
            return self.__provider.make_request('icx_getTransactionResult', params)
        else:
            raise DataTypeException("This hash value is unrecognized.")

    def get_transaction(self, tx_hash: str):
        """It is equivalent to icx_getTransactionByHash.

        :param tx_hash:
        :return:
        """
        if is_T_HASH(tx_hash):
            params = {'txHash': tx_hash}
            return self.__provider.make_request('icx_getTransactionByHash', params)
        else:
            raise DataTypeException("This hash value is unrecognized.")

    def call(self, call: object):
        """It is equivalent to icx_call.

        :param call:
        :return:
        """
        if isinstance(call, Call):
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
        else:
            raise DataTypeException("Call object is unrecognized.")

    def send_transaction(self, signed_transaction: SignedTransaction):
        """It is equivalent to icx_sendTransaction.

        :param signed_transaction:
        :return:
        """

        params = signed_transaction.signed_transaction_dict
        return self.__provider.make_request('icx_sendTransaction', params)



