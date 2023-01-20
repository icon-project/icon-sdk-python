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
from typing import Union, Tuple, Any, List

from iconsdk.builder.call_builder import Call
from iconsdk.builder.transaction_builder import Transaction
from iconsdk.exception import AddressException, DataTypeException
from iconsdk.providers.provider import Provider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils import get_timestamp
from iconsdk.utils.convert_type import convert_int_to_hex_str
from iconsdk.utils.converter import convert, \
    get_block_template_to_convert_transactions_for_genesis
from iconsdk.utils.gen_tx_data import generate_data_value
from iconsdk.utils.hexadecimal import add_0x_prefix, remove_0x_prefix
from iconsdk.utils.templates import BLOCK_0_1a, BLOCK_0_3, TRANSACTION_RESULT, TRANSACTION, BLOCK_0_1A_VERSION
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
    DEFAULT_BLOCK_VERSION = BLOCK_0_1A_VERSION

    def __init__(self, provider: Provider):
        self.__provider = provider

    def get_block(self, value: Union[int, str], full_response: bool = False,
                  block_version: str = DEFAULT_BLOCK_VERSION) -> dict:
        """
        If param is height,
            1. Returns block information by block height
            2-1. Delegates to icx_getBlockByHeight RPC method (When Block Version is 0.1a)
            2-2. Delegates to icx_getBlock RPC method (When Block Version is 0.3)

        Or block hash,
            1. Returns block information by block hash
            2-1. Delegates to icx_getBlockByHash RPC method (When Block Version is 0.1a)
            2-2. Delegates to icx_getBlock RPC method (When Block Version is 0.3)

        Or string value same as `latest`,
            1. Returns the last block information
            2-1. Delegates to icx_getLastBlock RPC method (When Block Version is 0.1a)
            2-2. Delegates to icx_getBlock RPC method (When Block Version is 0.3)

        :param value:
            Integer of a block height
            or hash of a block prefixed with '0x'
            or `latest`
        :param full_response:
            Boolean to check whether get naive dict or refined data from server
        :param block_version:
            returning block format version

        :return result: Block data
        """

        # Nested method of returning right name of API method
        def return_infos_by_block_version(_prev_method: str) -> Tuple[str, Any, bool]:
            """ Returns API method name, block template, bool of full print by block version

            :param _prev_method: previous API methods.
                    For instance, icx_getBlockByHeight, icx_getBlockByHash and icx_getLastBlock
            :return: method name, block template, bool of full print
            """
            new_method = "icx_getBlock"
            if block_version == self.DEFAULT_BLOCK_VERSION:
                return _prev_method, BLOCK_0_1a, False
            else:
                return new_method, BLOCK_0_3, True

        # by height
        if is_block_height(value):
            params = {'height': add_0x_prefix(hex(value))}
            prev_method = 'icx_getBlockByHeight'
        # by hash
        elif is_hex_block_hash(value):
            params = {'hash': value}
            prev_method = 'icx_getBlockByHash'
        # last block
        elif is_predefined_block_value(value):
            params = None
            prev_method = 'icx_getLastBlock'
        else:
            raise DataTypeException("It's unrecognized block reference:{0!r}.".format(value))

        method, block_template, full_print = return_infos_by_block_version(prev_method)
        result = self.__provider.make_request(method, params, full_response)

        if not full_response:
            block_template = get_block_template_to_convert_transactions_for_genesis(result, block_template)
            result = convert(result, block_template, full_print)

        return result

    def get_total_supply(self, height: int = None, full_response: bool = False) -> Union[dict, int]:
        """
        Returns total ICX coin supply that has been issued
        Delegates to icx_getTotalSupply RPC method

        :param height: Block height
        :param full_response: Boolean to check whether get naive dict or refined data from server
        :return: Total number of ICX coins issued
        """

        params = {}
        if height is not None:
            params["height"] = hex(height)

        result = self.__provider.make_request('icx_getTotalSupply', params, full_response=full_response)

        if full_response:
            return result
        else:
            return int(remove_0x_prefix(result), 16)

    def get_balance(self, address: str, height: int = None, full_response: bool = False) -> Union[dict, int]:
        """
        Returns the ICX balance of the given EOA or SCORE.
        Delegates to icx_getBalance RPC method.

        :param address: An address of EOA or SCORE. type(str)
        :param height: Block height. type(int)
        :param full_response: Boolean to check whether get naive dict or refined data from server
        :return: Number of ICX coins
        """
        if is_score_address(address) or is_wallet_address(address):
            params = {'address': address}
            if height is not None:
                params["height"] = hex(height)

            result = self.__provider.make_request('icx_getBalance', params, full_response)

            if full_response:
                return result
            else:
                return int(remove_0x_prefix(result), 16)
        else:
            raise AddressException("Address is wrong.")

    def get_score_api(self, address: str, height: int = None, full_response: bool = False) -> Union[dict, list]:
        """
        Returns SCORE's external API list.
        Delegates to icx_getScoreApi RPC method.

        :param address: A SCORE address to be examined
        :param height: Block height
        :param full_response: Boolean to check whether get naive dict or refined data from server
        :return: A list of API methods of the SCORE and its information
        """
        if not is_score_address(address):
            raise AddressException("SCORE Address is wrong.")

        params = {'address': address}
        if height is not None:
            params['height'] = hex(height)
        return self.__provider.make_request('icx_getScoreApi', params, full_response)

    def get_score_status(self, address: str, height: int = None, full_response: bool = False) -> dict:
        """
        Returns SCORE's status.
        Delegates to icx_getScoreStatus RPC method.

        :param address: A SCORE address to be examined
        :param height: Block height
        :param full_response: Boolean to check whether get naive dict or refined data from server
        :return: Status information
        """
        if not is_score_address(address):
            raise AddressException("SCORE Address is wrong.")

        params = {'address': address}
        if height is not None:
            params['height'] = hex(height)
        return self.__provider.make_request('icx_getScoreStatus', params, full_response)

    def get_transaction_result(self, tx_hash: str, full_response: bool = False) -> dict:
        """
        Returns the transaction result requested by transaction hash.
        Delegates to icx_getTransactionResult RPC method.

        :param tx_hash: Hash of a transaction prefixed with '0x'
        :param full_response: Boolean to check whether get naive dict or refined data from server
        :return A transaction result object
        """
        if not is_T_HASH(tx_hash):
            raise DataTypeException("This hash value is unrecognized.")

        params = {'txHash': tx_hash}
        result = self.__provider.make_request('icx_getTransactionResult', params, full_response)

        if not full_response:
            result = convert(result, TRANSACTION_RESULT)

        return result

    def wait_transaction_result(self, tx_hash: str, full_response: bool = False) -> dict:
        """
        Returns the result of a transaction specified by the transaction hash like get_transaction_result,
        but waits for some time to get the transaction result instead of returning immediately
        if there is no finalized result.
        Delegates to icx_WaitTransactionResult RPC method.

        :param tx_hash: Hash of a transaction prefixed with '0x'
        :param full_response: Boolean to check whether get naive dict or refined data from server
        :return A transaction result object
        """
        if not is_T_HASH(tx_hash):
            raise DataTypeException("This hash value is unrecognized.")

        params = {'txHash': tx_hash}
        result = self.__provider.make_request('icx_waitTransactionResult', params, full_response)

        if not full_response:
            result = convert(result, TRANSACTION_RESULT)

        return result

    def get_transaction(self, tx_hash: str, full_response: bool = False) -> dict:
        """
        Returns the transaction information requested by transaction hash.
        Delegates to icx_getTransactionByHash RPC method.

        :param tx_hash: Transaction hash prefixed with '0x'
        :param full_response: Boolean to check whether get naive dict or refined data from server
        :return: Information about a transaction
        """
        if not is_T_HASH(tx_hash):
            raise DataTypeException("This hash value is unrecognized.")

        params = {'txHash': tx_hash}
        result = self.__provider.make_request('icx_getTransactionByHash', params, full_response)

        if not full_response:
            result = convert(result, TRANSACTION)

        return result

    def call(self, call: object, full_response: bool = False) -> Union[dict, str]:
        """
        Calls SCORE's external function which is read-only without creating a transaction.
        Delegates to icx_call RPC method.

        :param call: Call object made by CallBuilder
        :param full_response: Boolean to check whether get naive dict or refined data from server
        :return: Values returned by the executed SCORE function
        """
        if not isinstance(call, Call):
            raise DataTypeException("Call object is unrecognized.")

        params = {
            "to": call.to,
            "dataType": "call",
            "data": {
                "method": call.method
            }
        }

        if call.from_ is not None:
            params["from"] = call.from_

        if isinstance(call.params, dict):
            params["data"]["params"] = call.params

        if call.height is not None:
            params["height"] = call.height

        return self.__provider.make_request('icx_call', params, full_response)

    def send_transaction(self, signed_transaction: SignedTransaction, full_response: bool = False) -> Union[dict, str]:
        """
        Sends the transaction.
        Delegates to icx_sendTransaction RPC method.

        :param signed_transaction: A signed transaction object
        :param full_response: Boolean to check whether get naive dict or refined data from server
        :return: Transaction hash prefixed with '0x'
        """
        params = signed_transaction.signed_transaction_dict
        return self.__provider.make_request('icx_sendTransaction', params, full_response)

    def send_transaction_and_wait(self, signed_transaction: SignedTransaction, full_response: bool = False) -> dict:
        """
        Sends a transaction like icx_sendTransaction, then it will wait for the result of it for specified time.
        Delegates to icx_sendTransactionAndWait RPC method.

        :param signed_transaction: A signed transaction object
        :param full_response: Boolean to check whether get naive dict or refined data from server
        :return A transaction result object
        """
        params = signed_transaction.signed_transaction_dict
        result = self.__provider.make_request('icx_sendTransactionAndWait', params, full_response)

        if not full_response:
            result = convert(result, TRANSACTION_RESULT)

        return result

    def estimate_step(self, transaction: Transaction, full_response: bool = False) -> int:
        """
        Returns an estimated step of how much step is necessary to allow the transaction to complete.

        :param transaction: a raw transaction
        :param full_response: a boolean indicating whether or not it returns refined data
        :return: an estimated step
        """
        if not isinstance(transaction, Transaction):
            raise DataTypeException("Transaction object is unrecognized.")

        params = {
            "version": convert_int_to_hex_str(transaction.version) if transaction.version else "0x3",
            "from": transaction.from_,
            "to": transaction.to,
            "timestamp": convert_int_to_hex_str(transaction.timestamp) if transaction.timestamp else get_timestamp(),
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

        result = self.__provider.make_request('debug_estimateStep', params, full_response)
        return result if full_response else int(result, 16)

    def get_trace(self, tx_hash: str) -> dict:
        """
        Get trace of the transaction

        :param tx_hash: Transaction hash prefixed with '0x'
        :return: trace
        """

        if not is_T_HASH(tx_hash):
            raise DataTypeException("This hash value is unrecognized.")

        params = {'txHash': tx_hash}
        result = self.__provider.make_request('debug_getTrace', params)
        return result

    def get_data_by_hash(self, _hash: str) -> str:
        """
        Returns data by hash.
        It can be used to retrieve data based on the hash algorithm (SHA3-256).
        Following data can be retrieved by a hash.
            - BlockHeader with the hash of the block
            - Validators with BlockHeader.NextValidatorsHash
            - Votes with BlockHeader.VotesHash
            - etc…
        Delegates to icx_getDataByHash RPC method.
        https://github.com/icon-project/goloop/blob/master/doc/btp_extension.md#icx_getdatabyhash

        :param _hash: The hash value of the data to retrieve
        :return: A data object
        """
        params = {'hash': _hash}
        return self.__provider.make_request('icx_getDataByHash', params)

    def get_block_header_by_height(self, height: int) -> str:
        """
        Returns block header for specified height.
        Delegates to icx_getBlockHeaderByHeight RPC method.
        https://github.com/icon-project/goloop/blob/master/doc/btp_extension.md#icx_getblockheaderbyheight

        :param height: The height of the block
        :return: A block header object
        """
        params = {'height': hex(height)}
        return self.__provider.make_request('icx_getBlockHeaderByHeight', params)

    def get_votes_by_height(self, height: int) -> str:
        """
        Returns votes for the block specified by height.
        Delegates to icx_getVotesByHeight RPC method.
        https://github.com/icon-project/goloop/blob/master/doc/btp_extension.md#icx_getvotesbyheight

        :param height: The height of the block for votes
        :return: A votes object
        """
        params = {'height': hex(height)}
        return self.__provider.make_request('icx_getVotesByHeight', params)

    def get_proof_for_result(self, _hash: str, index: int) -> str:
        """
        Returns proof for the receipt. Proof, itself, may include the receipt.
        Delegates to icx_getProofForResult RPC method.
        https://github.com/icon-project/goloop/blob/master/doc/btp_extension.md#icx_getproofforresult

        :param _hash: The hash value of the block including the result
        :param index: Index of the receipt in the block. 0 for the first
        :return: A proof object
        """
        params = {
            'hash': _hash,
            'index': hex(index),
        }
        return self.__provider.make_request('icx_getProofForResult', params)

    def get_proof_for_events(self, _hash: str, index: int, events: List[str] = []) -> dict:
        """
        Returns proof for the receipt and the events in it. The proof may include the data itself.
        Delegates to icx_getProofForEvents RPC method.
        https://github.com/icon-project/goloop/blob/master/doc/btp_extension.md#icx_getproofforevents

        :param _hash: The hash value of the block including the result
        :param index: Index of the receipt in the block. 0 for the first
        :param events: List of indexes of the events in the receipt
        :return: A proof object
        """
        params = {
            'hash': _hash,
            'index': hex(index),
            'events': events,
        }
        return self.__provider.make_request('icx_getProofForEvents', params)

    def get_btp_network_info(self, id: int, height: int = None) -> dict:
        """
        Returns BTP Network information for specified height and ID.
        Delegates to btp_getNetworkInfo RPC method.
        https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#btp_getNetworkInfo

        :param id: The id of the BTP network
        :param height: The height of the main block
        :return: A BTP Network information object
        """
        params = {'id': hex(id)}
        if height is not None:
            params['height'] = hex(height)
        return self.__provider.make_request('btp_getNetworkInfo', params)

    def get_btp_network_type_info(self, id: int, height: int = None) -> dict:
        """
        Returns BTP Network Type information for specified height and ID.
        Delegates to btp_getNetworkTypeInfo RPC method.
        https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#btp_getNetworkTypeInfo

        :param id: The id of the BTP network type
        :param height: The height of the main block
        :return: A BTP Network Type information object
        """
        params = {'id': hex(id)}
        if height is not None:
            params['height'] = hex(height)
        return self.__provider.make_request('btp_getNetworkTypeInfo', params)

    def get_btp_messages(self, height: int, network_id: int) -> list:
        """
        Returns BTP messages for specified height and network ID.
        Delegates to btp_getMessages RPC method.
        https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#btp_getMessages

        :param height: The height of the main block
        :param network_id: The id of the BTP network
        :return: A BTP Messages object
        """
        params = {'height': hex(height), 'networkID': hex(network_id)}
        return self.__provider.make_request('btp_getMessages', params)

    def get_btp_header(self, height: int, network_id: int) -> str:
        """
        Returns BTP block header for specified height and network ID.
        Delegates to btp_getHeader RPC method.
        https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#btp_getHeader

        :param height: The height of the main block
        :param network_id: The id of the BTP network
        :return: A Base64 encoded BTP block header
        """
        params = {'height': hex(height), 'networkID': hex(network_id)}
        return self.__provider.make_request('btp_getHeader', params)

    def get_btp_proof(self, height: int, network_id: int) -> str:
        """
        Returns BTP block proof for specified height and network ID.
        Delegates to btp_getHeader RPC method.
        https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#btp_getProof

        :param height: The height of the main block
        :param network_id: The id of the BTP network
        :return: A Base64 encoded BTP block proof
        """
        params = {'height': hex(height), 'networkID': hex(network_id)}
        return self.__provider.make_request('btp_getProof', params)

    def get_btp_source_information(self) -> dict:
        """
        Returns BTP source network information.
        Delegates to btp_getSourceInformation RPC method.
        https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#btp_getSourceInformation

        :return: A BTP network information object
        """
        return self.__provider.make_request('btp_getSourceInformation')
