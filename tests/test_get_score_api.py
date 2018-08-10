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
from IconService.exception import DataTypeException, AddressException, JSONRPCException
from IconService.utils.validation import is_block, is_score_apis


class TestGetScoreApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))
        # Because governance always has score apis, it is proper for the test.
        cls.governance_address = "cx0000000000000000000000000000000000000001"

    def test_get_score_api(self):
        # case 0: when getting score apis successfully
        result = self.icon_service.get_score_api(self.governance_address)
        self.assertTrue(result)
        # case 1: when address is wrong - wallet address
        self.assertRaises(AddressException, self.icon_service.get_score_api,
                          "hx882efc17c2f50e0d60142b9c0e746cbafb569d8c")
        # case 2: when address is wrong - too short
        self.assertRaises(AddressException, self.icon_service.get_score_api,
                          "cx882efc17c2f50e0d60142b9c0e746cbafb")
        # case 3: when the address is not score id
        self.assertRaises(JSONRPCException, self.icon_service.get_score_api,
                          "cxb0776ee37f5b45bfaea8cff1d8232fbb6122ec32")

    def test_validate_score_apis(self):
        result = self.icon_service.get_score_api(self.governance_address)
        self.assertTrue(result)
        self.assertTrue(is_score_apis(result))


if __name__ == "__main__":
    unittest.main()
