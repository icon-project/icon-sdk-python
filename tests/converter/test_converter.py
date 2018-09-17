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

from unittest import TestCase, main
from tests.converter.example_blocks import block_v2_1, block_v2_2, block_v2_3, block_v3_1, block_v3_2, block_genesis
from tests.converter.example_transactions import transaction_v2_1, transaction_v2_2, transaction_v3_1, transaction_v3_2, transaction_v3_3
from tests.converter.example_tx_results import tx_result_v2_1, tx_result_v2_2, tx_result_v3_1, tx_result_v3_2, tx_result_v3_3
from iconsdk.converter import convert_block, convert_transaction, convert_transaction_result
from iconsdk.utils.hexadecimal import is_0x_prefixed
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from tests.example_config import TEST_HTTP_ENDPOINT_URI_V3
from logging import getLogger
from iconsdk.utils import set_logger
import pprint


class TestConverter(TestCase):

    blocks = [block_v2_1, block_v2_2, block_v2_3, block_v3_1, block_v3_2, block_genesis]
    transactions = [transaction_v2_1, transaction_v2_2, transaction_v3_1, transaction_v3_2, transaction_v3_3]
    tx_results = [tx_result_v2_1, tx_result_v2_2, tx_result_v3_1, tx_result_v3_2, tx_result_v3_3]

    def test_converter_blocks(self):
        """
        Test with different sample blocks which are made from JSON RPC API V2 or V3
        and with the genesis block.
        """
        for block in self.blocks:
            convert_block(block)
            self.assertTrue(validate_block(block))

    def test_converter_transactions(self):
        """
        Test with different sample transactions which made from JSON RPC API V2 or V3.
        """
        for transaction in self.transactions:
            convert_transaction(transaction)
            self.assertTrue(validate_transaction(transaction))

    def test_converter_tx_results(self):
        """
        Test with different sample transaction results which made from JSON RPC API V2 or V3.
        """
        for tx_result in self.tx_results:
            convert_transaction_result(tx_result)
            print(tx_result)
            self.assertTrue(validate_transaction_result(tx_result))

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
        logger = getLogger("TEST CONVERTER")

        # No need to use logging, remove the line.
        set_logger(logger, 'DEBUG')

        logger.debug("TEST CONVERTER START")

        icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))

        # Scenario 1: Get the last block data and validate the block data.
        last_block_height = icon_service.get_block("latest")["height"]

        for height in range(0, last_block_height if last_block_height < 500 else 500):
            # Scenario 2: Get all of the transaction data on that block and validate the transaction data.
            block = icon_service.get_block(height)
            # pprint.pprint(block)
            self.assertTrue(validate_block(block))

            # Except for the genesis block
            if height > 0:
                for transaction_in_block in block["confirmed_transaction_list"]:
                    # Scenario 3: Get all of the transaction result data on that transaction
                    # and validate the transaction result data.
                    transaction_result = icon_service.get_transaction_result(transaction_in_block["txHash"])
                    # logger.debug(transaction_result)
                    # pprint.pprint(transaction_result)
                    self.assertTrue(validate_transaction_result(transaction_result))
                    # Scenario 4: Repeatedly, get the other blocks from the last to the first
                    # and validate all of three kinds of the data.
                    transaction = icon_service.get_transaction(transaction_in_block["txHash"])
                    # logger.debug(transaction)
                    # pprint.pprint(transaction)
                    self.assertTrue(validate_transaction(transaction))


def validate_common_data_on_transaction(transaction):
    """Validate the common data on transaction has right returning format."""
    int_fields = ["value", "fee", "nid", "stepLimit", "timestamp", "nonce", "version"]

    for int_field in int_fields:
        if int_field in transaction and not isinstance(transaction[int_field], int):
            return False

    if "method" in transaction:
        return False

    if "version" not in transaction:
        return False

    if "dataType" in transaction and transaction["dataType"] in ("deploy", "message"):
        if transaction["dataType"] == "deploy" and not isinstance(transaction["data"]["content"], bytes):
            return False
        if transaction["dataType"] == "message" and not isinstance(transaction["data"], str):
            return False

    return True


def validate_block(data: dict):
    """Validate the block data has right returning format."""
    if data["height"] == 0:
        return True

    if "tx_hash" in data:
        return False

    for transaction in data["confirmed_transaction_list"]:
        validate_common_data_on_transaction(transaction)
        if "txHash" not in transaction and not is_0x_prefixed(transaction["txHash"]):
            return False

    return True


def validate_transaction(transaction: dict):
    """Validate the transaction data has right returning format."""
    int_fields = ["txIndex", "blockHeight"]

    for int_field in int_fields:
        if int_field in transaction and not isinstance(transaction[int_field], int):
            return False

    return True and validate_common_data_on_transaction(transaction)


def validate_transaction_result(data: dict):
    """Validate the transaction result data has right returning format."""
    int_fields = ["status", "blockHeight", "txIndex", "stepUsed", "stepPrice", "cumulativeStepUsed"]

    for int_field in int_fields:
        if int_field in data and not isinstance(data[int_field], int):
            return False

    if "logsBloom" in data and not isinstance(data["logsBloom"], bytes):
        return False

    return True


if __name__ == "__main__":
    main()


