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
import os
from time import sleep
from unittest import main

from iconsdk.builder.transaction_builder import DeployTransactionBuilder
from iconsdk.exception import DataTypeException, JSONRPCException
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.hexadecimal import remove_0x_prefix, add_cx_prefix, add_0x_prefix
from iconsdk.utils.validation import is_transaction_result
from tests.api_send.test_send_super import TestSendSuper


class TestGetTransactionResult(TestSendSuper):

    def test_validate_transaction(self):
        param = {"init_supply": 10000}
        deploy_transaction = DeployTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]) \
            .content(self.setting["content_install"]) \
            .params(param) \
            .version(3) \
            .build()

        # Test install SCORE : Sends transaction which makes the SCORE install correctly
        signed_transaction_dict = SignedTransaction(deploy_transaction, self.wallet)
        tx_hash = self.icon_service.send_transaction(signed_transaction_dict)

        sleep(2)
        result = self.icon_service.get_transaction_result(tx_hash)
        self.assertTrue(is_transaction_result(result))

        # case 1: when tx_hash is invalid - no prefixed
        self.assertRaises(DataTypeException, self.icon_service.get_transaction_result, remove_0x_prefix(tx_hash))
        # case 2: when tx_hash is invalid - wrong prefixed
        self.assertRaises(DataTypeException, self.icon_service.get_transaction_result,
                          add_cx_prefix(remove_0x_prefix(tx_hash)))
        # case 3: when tx_hash is invalid - too short
        self.assertRaises(DataTypeException, self.icon_service.get_transaction_result, tx_hash[:15])
        # case 4: when tx_hash is invalid - not exist
        tx_hash_invalid = add_0x_prefix(os.urandom(32).hex())
        self.assertRaises(JSONRPCException, self.icon_service.get_transaction_result, tx_hash_invalid)


if __name__ == "__main__":
    main()
