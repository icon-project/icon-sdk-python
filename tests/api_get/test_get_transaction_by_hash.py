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

from time import sleep
from unittest import main

from iconsdk.builder.transaction_builder import TransactionBuilder
from iconsdk.exception import JSONRPCException, DataTypeException
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.hexadecimal import remove_0x_prefix, add_cx_prefix
from iconsdk.utils.validation import is_transaction
from tests.api_send.test_send_super import TestSendSuper


class TestGetTransactionByHash(TestSendSuper):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # When having an optional property, nonce
        icx_transaction = TransactionBuilder() \
            .from_(cls.setting["from"]) \
            .to(cls.setting["to"]) \
            .value(cls.setting["value"]) \
            .step_limit(cls.setting["step_limit"]) \
            .nid(3) \
            .nonce(cls.setting["nonce"]) \
            .version(3) \
            .build()

        signed_transaction_dict = SignedTransaction(icx_transaction, cls.wallet)
        tx_result = cls.icon_service.send_transaction(signed_transaction_dict)
        sleep(2)
        cls.tx_hash = tx_result
        cls.tx_hash_invalid = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"

    def test_get_transaction_by_hash(self):
        # case 0: when tx_hash is valid
        result = self.icon_service.get_transaction(self.tx_hash)
        self.assertTrue(result)
        # case 1: when tx_hash is invalid - no prefixed
        self.assertRaises(DataTypeException, self.icon_service.get_transaction, remove_0x_prefix(self.tx_hash))
        # case 2: when tx_hash is invalid - wrong prefixed
        self.assertRaises(DataTypeException, self.icon_service.get_transaction,
                          add_cx_prefix(remove_0x_prefix(self.tx_hash)))
        # case 3: when tx_hash is invalid - too short
        self.assertRaises(DataTypeException, self.icon_service.get_transaction, self.tx_hash[:15])
        # case 4: when tx_hash is invalid - not exist
        self.assertRaises(JSONRPCException, self.icon_service.get_transaction, self.tx_hash_invalid)

    def test_validate_transaction(self):
        result = self.icon_service.get_transaction(self.tx_hash)
        self.assertTrue(is_transaction(result))


if __name__ == "__main__":
    main()
