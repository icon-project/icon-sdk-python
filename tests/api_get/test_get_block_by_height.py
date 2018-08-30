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
from iconsdk.utils.validation import is_block


class TestGetBlockByHeight(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))
        result = cls.icon_service.get_block("latest")
        cls.height_of_latest_block = result["height"]

    def test_get_block_by_height(self):
        # case 0: when height is 0
        result = self.icon_service.get_block(0)
        self.assertTrue(result)

        # case 1: when a block of that height does not exist
        self.assertRaises(JSONRPCException, self.icon_service.get_block, self.height_of_latest_block+1)

        # case 2: when height is wrong
        self.assertRaises(DataTypeException, self.icon_service.get_block, "1")
        self.assertRaises(DataTypeException, self.icon_service.get_block, "0x123")
        self.assertRaises(DataTypeException, self.icon_service.get_block, -2)

    def test_validate_block(self):
        result = self.icon_service.get_block(0)
        self.assertTrue(is_block(result))


if __name__ == "__main__":
    main()
