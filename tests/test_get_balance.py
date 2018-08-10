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

import unittest
from IconService.Icon_service import IconService
from IconService.providers.http_provider import HTTPProvider
from tests.example_config import TEST_HTTP_ENDPOINT_URI_V3
from IconService.exception import DataTypeException, AddressException


class TestGetBalance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))
        result = cls.icon_service.get_block("latest")
        cls.from_ = result["confirmed_transaction_list"][0]["from"]
        cls.to_ = result["confirmed_transaction_list"][0]["to"]

    def test_get_balance_from_wallet(self):
        # case 0: get balance from wallet or score successfully.
        result = self.icon_service.get_balance(self.from_)
        self.assertTrue(isinstance(result, int))
        result = self.icon_service.get_balance(self.to_)
        self.assertTrue(isinstance(result, int))

        # case 1: when a param is wrong.
        self.assertRaises(AddressException, self.icon_service.get_balance, self.to_[2:])
        self.assertRaises(AddressException, self.icon_service.get_balance, self.from_[2:])
        self.assertRaises(AddressException, self.icon_service.get_balance, "123")
        self.assertRaises(DataTypeException, self.icon_service.get_balance, 123)
        # when the address's length is short
        self.assertRaises(AddressException, self.icon_service.get_balance, "cx882efc17c2f50e0d60142b9c0e746cbafb569d")


if __name__ == "__main__":
    unittest.main()
