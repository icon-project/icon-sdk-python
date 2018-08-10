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
from IconService.exception import DataTypeException
from IconService.utils.validation import is_block


class TestGetLastBlock(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))

    def test_get_block_by_height(self):
        # case 0: when param is `latest`
        result = self.icon_service.get_block("latest")
        self.assertTrue(result)

        # case 2: when param is wrong
        self.assertRaises(DataTypeException, self.icon_service.get_block, "latest1")
        self.assertRaises(DataTypeException, self.icon_service.get_block, "late")

    def test_validate_block(self):
        result = self.icon_service.get_block("latest")
        self.assertTrue(is_block(result))


if __name__ == "__main__":
    unittest.main()
