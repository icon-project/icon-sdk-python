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

from hashlib import sha3_256
from unittest import TestCase, main
from IconService.signed_transaction import SignedTransaction
from IconService.builder.transaction_builder import IcxTransactionBuilder, MessageTransactionBuilder, \
    CallTransactionBuilder, DeployTransactionBuilder
from IconService.utils.hexadecimal import add_0x_prefix
from IconService.utils.validation import is_icx_transaction, is_call_transaction, is_message_transaction, \
    is_deploy_transaction, is_T_HASH
from IconService.wallet.wallet import KeyWallet
from IconService.Icon_service import IconService
from IconService.providers.http_provider import HTTPProvider
from tests.example_config import TEST_HTTP_ENDPOINT_URI_V3, TEST_PRIVATE_KEY


class TestSignedTransaction(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.from_ = "hx4873b94352c8c1f3b2f09aaeccea31ce9e90bd31"
        # If SCORE's address is as follows, it means install SCORE
        cls.to_0 = "cx0000000000000000000000000000000000000000"
        cls.to = "hx5bfdb090f43a808005ffc27c25b213145e80b7cd"
        cls.value = "0xde0b6b3a7640000"
        cls.step_limit = "0x12345"
        cls.nid = "0x3"
        cls.nonce = "0x2"
        cls.content_type = "application/zip"
        cls.content = "test".encode()
        cls.msg_data = add_0x_prefix(sha3_256("test".encode()).hexdigest())
        cls.params = {
            "name": "ABCToken",
            "symbol": "abc",
            "decimals": "0x12"
        }
        cls.method = "transfer"
        cls.data = "test"

    def test_to_dict(self):
        # Transfer
        icx_transaction = IcxTransactionBuilder().from_(self.from_).to(self.to).value(self.value)\
            .step_limit(self.step_limit).nid(self.nid).nonce(self.nonce).build()
        tx_dict = SignedTransaction.to_dict(icx_transaction)
        self.assertTrue(is_icx_transaction(tx_dict))

        # Update SCORE
        deploy_transaction = DeployTransactionBuilder().from_(self.from_).to(self.to).step_limit(self.step_limit)\
            .nid(self.nid).content_type(self.content_type).content(self.content)\
            .params(self.params).build()
        tx_dict = SignedTransaction.to_dict(deploy_transaction)
        self.assertTrue(is_deploy_transaction(tx_dict))

        # Install SCORE
        deploy_transaction = DeployTransactionBuilder().from_(self.from_).to(self.to_0).step_limit(self.step_limit) \
            .nid(self.nid).nonce(self.nonce).content_type(self.content_type).content(self.content) \
            .params(self.params).build()
        tx_dict = SignedTransaction.to_dict(deploy_transaction)
        self.assertTrue(is_deploy_transaction(tx_dict))

        # SCORE method call
        call_transaction = CallTransactionBuilder().from_(self.from_).to(self.to).step_limit(self.step_limit)\
            .nid(self.nid).nonce(self.nonce).method(self.method).params(self.params).build()
        tx_dict = SignedTransaction.to_dict(call_transaction)
        self.assertTrue(is_call_transaction(tx_dict))

        # Message send
        msg_transaction = MessageTransactionBuilder().from_(self.from_).to(self.to).step_limit(self.step_limit)\
            .nid(self.nid).nonce(self.nonce).data(self.data).build()
        tx_dict = SignedTransaction.to_dict(msg_transaction)
        self.assertTrue(is_message_transaction(tx_dict))

    def test_signed_transaction_transfer(self):
        wallet = KeyWallet.load(TEST_PRIVATE_KEY)
        icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))
        icx_transaction = IcxTransactionBuilder().from_(wallet.get_address()).to(self.to).value(self.value) \
            .step_limit(self.step_limit).nid(self.nid).nonce(self.nonce).build()
        signed_transaction_dict = SignedTransaction(icx_transaction, wallet)
        result = icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))


if __name__ == "__main__":
    main()


