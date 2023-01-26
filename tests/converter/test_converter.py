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
from unittest import TestCase, skip

from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.utils.convert_type import add_0x_prefix
from iconsdk.utils.converter import convert, convert_value, get_block_template_to_convert_transactions_for_genesis
from iconsdk.utils.templates import (TRANSACTION_RESULT, TRANSACTION, BLOCK_0_1a, BLOCK_0_3, BLOCK_0_1A_VERSION,
                                     BLOCK_0_3_VERSION)
from tests.converter.example_blocks_0_1a import (BLOCK_0_1A_V3_0, BLOCK_0_1A_V3_1, BLOCK_0_1A_V3_2, BLOCK_0_1A_V2_0,
                                                 BLOCK_0_1A_V2_1, BLOCK_0_1A_V2_2, BLOCK_0_1A_V2_3, BLOCK_GENESIS_V3_0,
                                                 BLOCK_GENESIS_V3_1, BLOCK_GENESIS_V2_0)
from tests.converter.example_blocks_0_3 import (BLOCK_0_3_V3_0, BLOCK_0_3_V3_1, BLOCK_0_3_V3_2, BLOCK_0_3_V3_3)
from tests.converter.example_transactions import (TRANSACTION_0, TRANSACTION_1, TRANSACTION_2, TRANSACTION_3,
                                                  TRANSACTION_4, TRANSACTION_5)
from tests.converter.example_tx_results import (TX_RESULT_0, TX_RESULT_1, TX_RESULT_2, TX_RESULT_3)
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST, VERSION_FOR_TEST


@skip("TestConverter MUST work without network")
class TestConverter(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        Sets multiple blocks, transactions and tx results for converting tests

        - From both 'Mainnet' and 'Testnet'
        - Kind of Blocks
            - Genesis (o)
            - Transaction version is RPC V2 && Block version is V0.1a (o)
            - Transaction version is RPC V3 && Block version is V0.1a (o)
            - Transaction version is RPC V3 && Block version is V3 with block sample (o)
        - Kind of transactions called 'confirmed_transaction_list' on Block
            - Genesis (o)
            - RPC V2 (o)
            - RPC V3 (o)
        - Kind of Transactions
            - RPC V2 (o)
            - RPC V3 (o)
        - Kind of Transaction results
            - RPC V2 (o)
            - PRC V3 (o)
        """
        cls.domains = ["https://testwallet.icon.foundation", "https://wallet.icon.foundation"]
        cls.blocks_0_1a, cls.transactions_on_blocks, cls.transactions, cls.transaction_results = list(), list(), list(), list()

        for domain in cls.domains:
            buf_blocks, buf_transactions_on_blocks, buf_transactions, buf_transaction_results \
                = cls._set_samples(cls, domain=domain)
            cls.blocks_0_1a.extend(buf_blocks)
            cls.transactions_on_blocks.extend(buf_transactions_on_blocks)
            cls.transactions.extend(buf_transactions)
            cls.transaction_results.extend(buf_transaction_results)

        tx_results = [TX_RESULT_0, TX_RESULT_1, TX_RESULT_2, TX_RESULT_3]
        transactions = [TRANSACTION_0, TRANSACTION_1, TRANSACTION_2, TRANSACTION_3, TRANSACTION_4, TRANSACTION_5]
        blocks_0_1a = [BLOCK_0_1A_V3_0, BLOCK_0_1A_V3_1, BLOCK_0_1A_V3_2, BLOCK_0_1A_V2_0, BLOCK_0_1A_V2_1,
                       BLOCK_0_1A_V2_2,
                       BLOCK_0_1A_V2_3, BLOCK_GENESIS_V3_0, BLOCK_GENESIS_V3_1, BLOCK_GENESIS_V2_0]

        cls.transaction_results.extend(tx_results)
        cls.transactions.extend(transactions)
        cls.blocks_0_1a.extend(blocks_0_1a)
        cls.blocks_0_3 = [BLOCK_0_3_V3_0, BLOCK_0_3_V3_1, BLOCK_0_3_V3_2, BLOCK_0_3_V3_3]

    @staticmethod
    def _set_target_heights():
        block_height_of_genesis = 0
        block_height_of_transaction_rpc_v2 = 50
        block_height_of_transaction_rpc_v3 = 600000
        range_height = 100

        buf_heights = list()
        buf_heights.append(block_height_of_genesis)
        start_block_heights = [block_height_of_transaction_rpc_v2, block_height_of_transaction_rpc_v3]
        for start_block_height in start_block_heights:
            buf_heights.extend([height for height in range(start_block_height, start_block_height + range_height)])
        return buf_heights

    @staticmethod
    def _set_samples(self, domain: str) -> (list, list, list, list):
        buf_blocks = list()
        buf_transactions_on_blocks = list()  # block's transaction list which means confirmed transaction list
        buf_transactions = list()  # return value of 'get_transaction'
        buf_transaction_results = list()  # return value of 'get_transaction_result'

        icon_service = IconService(HTTPProvider(domain, VERSION_FOR_TEST))
        target_block_heights = self._set_target_heights()
        for height in target_block_heights:
            block = icon_service.get_block(height, full_response=True)
            block = block['result']
            buf_blocks.append(block)
            for transaction in block[
                'confirmed_transaction_list' if block['version'] == BLOCK_0_1A_VERSION else 'transactions']:
                buf_transactions_on_blocks.append(transaction)

                if ('tx_hash' or 'txHash') in transaction:
                    tx_hash = transaction['tx_hash' if 'tx_hash' in transaction else 'txHash']
                    tx_hash = add_0x_prefix(tx_hash)
                    tx = icon_service.get_transaction(tx_hash, full_response=True)
                    tx = tx['result']
                    buf_transactions.append(tx)
                    tx_result = icon_service.get_transaction_result(tx_hash, full_response=True)
                    tx_result = tx_result['result']
                    buf_transaction_results.append(tx_result)

        return buf_blocks, buf_transactions_on_blocks, buf_transactions, buf_transaction_results

    def test_converter_blocks(self):
        """
        Test with different sample blocks which are made from JSON RPC API V2 or V3
        and with the genesis block.
        """
        for block in self.blocks_0_1a:
            # test for block version 0.1a
            block_template = get_block_template_to_convert_transactions_for_genesis(block, BLOCK_0_1a)
            converted_block = convert(block, block_template)
            self.assertTrue(validate_block(block_template, block, converted_block))

            # test for block version 0.3
            block_template = get_block_template_to_convert_transactions_for_genesis(block, BLOCK_0_3)
            converted_block = convert(block, block_template, True)
            self.assertTrue(validate_block(block_template, block, converted_block))

        for block in self.blocks_0_3:
            block_template = get_block_template_to_convert_transactions_for_genesis(block, BLOCK_0_3)
            converted_block = convert(block, block_template, True)
            self.assertTrue(validate_block(block_template, block, converted_block))

    def test_converter_transactions(self):
        """
        Test with different sample transactions which made from JSON RPC API V2 or V3.
        """
        for transaction in self.transactions:
            converted_transaction = convert(transaction, TRANSACTION)
            self.assertTrue(validate_transaction(TRANSACTION, transaction, converted_transaction))

    def test_converter_tx_results(self):
        """Test for multiple types of transaction results by validating it"""
        for tx_result in self.transaction_results:
            converted_transaction_result = convert(tx_result, TRANSACTION_RESULT)
            self.assertTrue(validate_transaction_result(TRANSACTION_RESULT, tx_result, converted_transaction_result))

    def test_integrate_converter(self):
        """
        Test integrating for the converter which checks that all of the data
        about the block, transaction, and transaction result have the right format.

        [Purpose]
        Check all of the data about the block, transaction, and transaction result.

        [Scenario]
        1. Get the last block data and validate the block data.
        2. Get all of the transaction data on that block and validate the transaction data.
        3. Get all of the transaction result data on that transaction and validate the transaction result data.
        4. Repeatedly, get the other blocks from the last to the first and validate all of three kinds of the data.
        """
        test_domains = self.domains + [BASE_DOMAIN_URL_V3_FOR_TEST]
        max_block_height = 100
        for domain in test_domains:
            icon_service = IconService(HTTPProvider(domain, VERSION_FOR_TEST))
            last_block_height = icon_service.get_block("latest")["height"]
            block_versions = [BLOCK_0_1A_VERSION, BLOCK_0_3_VERSION]
            for block_version in block_versions:
                if block_version == BLOCK_0_1A_VERSION:
                    block_template = BLOCK_0_1a
                    key_name_of_transactions = 'confirmed_transaction_list'
                else:
                    # After Mainnet apply for block 0.3, remove this remark right away.
                    continue

                    block_template = BLOCK_0_3
                    key_name_of_transactions = 'transactions'

                for height in range(last_block_height if last_block_height < max_block_height else max_block_height):
                    # Check block
                    block = icon_service.get_block(height, full_response=True, block_version=block_version)
                    block = block['result']
                    converted_block = icon_service.get_block(height, block_version=block_version)
                    block_template = get_block_template_to_convert_transactions_for_genesis(block, block_template)
                    self.assertTrue(validate_block(block_template, block, converted_block))

                    if block["height"] == 0:
                        continue

                    for transaction_in_block in converted_block[key_name_of_transactions]:
                        # Check transaction result
                        tx_result = icon_service.get_transaction_result(transaction_in_block["txHash"], True)
                        tx_result = tx_result['result']
                        converted_transaction_result = icon_service.get_transaction_result(
                            transaction_in_block["txHash"])
                        self.assertTrue(
                            validate_transaction_result(TRANSACTION_RESULT, tx_result, converted_transaction_result))

                        # Check transaction
                        transaction = icon_service.get_transaction(transaction_in_block["txHash"], True)
                        transaction = transaction['result']
                        converted_transaction = icon_service.get_transaction(transaction_in_block["txHash"])
                        self.assertTrue(validate_transaction(TRANSACTION, transaction, converted_transaction))


def validate_block(template: dict, org_data: dict, converted_data: dict):
    """Validate the block data has right returning format."""
    optional_keys = ("next_leader")
    return validate(template, org_data, converted_data, optional_keys)


def validate_transaction(template: dict, org_data: dict, converted_data: dict):
    """Validate the transaction data has right returning format."""

    def check_when_datatype_is_deploy_if_data_content_type_is_bytes(key, _converted_data):
        if key == "data" and key in _converted_data and _converted_data["dataType"] == "deploy" and not isinstance(
                _converted_data[key]["content"], bytes):
            return False
        return True

    optional_keys = ("data", "dataType", "nid", "nonce", "fee", "stepLimit", "nid", "version", "timestamp", "value")
    deleted_keys = ("tx_hash", "method")
    additional_checking_func = check_when_datatype_is_deploy_if_data_content_type_is_bytes
    return validate(template, org_data, converted_data, optional_keys, deleted_keys,
                    additional_checking_func=additional_checking_func)


def validate_transaction_result(template: dict, org_data: dict, converted_data: dict):
    """Validate the transaction result data has right returning format."""

    def check_if_code_type_is_converted_to_int_when_failure(key, _converted_data):
        if key == "failure" and key in _converted_data and not isinstance(_converted_data[key]["code"], int):
            return False
        return True

    optional_keys = ("failure", "scoreAddress", "eventLogs", "logsBloom")
    additional_checking_func = check_if_code_type_is_converted_to_int_when_failure
    return validate(template, org_data, converted_data, optional_keys,
                    additional_checking_func=additional_checking_func)


def _get_tx_hash_key(key: str, org_data: dict) -> str:
    """
    If key is 'txHash' and it is not in original data in dict but 'tx_hash' is in,
    it returns 'tx_hash' for a new key.

    :param key: key in dict
    :param org_data: original data in dict
    :return: new key named 'tx_hash' or original key
    """
    org_keys_as_dict = {
        'txHash': 'tx_hash',
        'prevHash': 'prev_block_hash',
        'transactionsHash': 'merkle_tree_root_hash',
        'timestamp': 'time_stamp',
        'hash': 'block_hash',
        'leader': 'peer_id',
        'nextLeader': 'next_leader'
    }
    if key in org_keys_as_dict and key not in org_data:
        return org_keys_as_dict[key]

    return key


def validate(template: dict, ord_data: dict, converted_data: dict, optional_keys: tuple = (), deleted_keys: tuple = (),
             additional_checking_func=None, check_optional: bool = True) -> bool:
    for key, value in template.items():
        if key == "CHANGE":
            continue
        if isinstance(value, list) and key in ord_data and isinstance(ord_data[key], list):
            for i, item in enumerate(ord_data[key]):
                if item is None:
                    continue
                if validate(value[0], item, converted_data[key][i], check_optional=False) is False:
                    return False
        if key in converted_data and not isinstance(converted_data[key], list) \
                and converted_data[key] != '' and key not in ("data", "failure"):
            if converted_data[key] != convert_value(ord_data[_get_tx_hash_key(key, ord_data)], value):
                return False
        if check_optional is True and key not in optional_keys and key not in converted_data:
            return False
        if key in deleted_keys:
            return False
        if additional_checking_func and additional_checking_func(key, converted_data) is False:
            return False
    return True
