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
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from tests.example_config import TEST_HTTP_ENDPOINT_URI_V3
from iconsdk.exception import DataTypeException, JSONRPCException
from iconsdk.utils.hexadecimal import remove_0x_prefix, add_cx_prefix
from iconsdk.utils.validation import is_transaction_result


class TestGetTransactionResult(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))
        result = cls.icon_service.get_block(1)
        cls.tx_hash = result["confirmed_transaction_list"][0]["txHash"]
        cls.tx_hash_invalid = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"

    def test_validate_transaction(self):
        result = self.icon_service.get_transaction_result(self.tx_hash)
        self.assertTrue(is_transaction_result(result))

    def test_get_transaction_result(self):
        # case 0: when tx_hash is valid
        result = self.icon_service.get_transaction_result(self.tx_hash)
        self.assertTrue(result)
        # case 1: when tx_hash is invalid - no prefixed
        self.assertRaises(DataTypeException, self.icon_service.get_transaction_result, remove_0x_prefix(self.tx_hash))
        # case 2: when tx_hash is invalid - wrong prefixed
        self.assertRaises(DataTypeException, self.icon_service.get_transaction_result,
                          add_cx_prefix(remove_0x_prefix(self.tx_hash)))
        # case 3: when tx_hash is invalid - too short
        self.assertRaises(DataTypeException, self.icon_service.get_transaction_result, self.tx_hash[:15])
        # case 4: when tx_hash is invalid - not exist
        self.assertRaises(JSONRPCException, self.icon_service.get_transaction_result, self.tx_hash_invalid)


if __name__ == "__main__":
    main()
