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

from unittest import TestCase, main
from IconService.Icon_service import IconService
from IconService.providers.http_provider import HTTPProvider
from tests.example_config import TEST_HTTP_ENDPOINT_URI_V3
from IconService.utils.hexadecimal import add_0x_prefix, remove_0x_prefix
from IconService.exception import DataTypeException, JSONRPCException
from IconService.utils.validation import is_block


class TestGetBlockByHash(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))
        result = cls.icon_service.get_block("latest")
        cls.valid_hash = add_0x_prefix(result["block_hash"])

    def test_get_block_by_hash(self):
        # case 0: when hash value of latest block is valid
        result = self.icon_service.get_block(self.valid_hash)
        self.assertTrue(result)

        # case 1: when hash value of the previous of latest block is valid
        if result["prev_block_hash"]:
            valid_hash_prev = add_0x_prefix(result["prev_block_hash"])
            result = self.icon_service.get_block(valid_hash_prev)
            self.assertTrue(result)

        # case 2: when hash value is invalid not prefixed with `0x`
        invalid_hash = remove_0x_prefix(self.valid_hash)
        self.assertRaises(DataTypeException, self.icon_service.get_block, invalid_hash)

        # case 2: when block hash is wrong
        invalid_hash = "0x033f8d96045eb8301fd17cf078c28ae58a3ba329f6ada5cf128ee56dc2af26f7"
        self.assertRaises(JSONRPCException, self.icon_service.get_block, invalid_hash)

    def test_validate_block(self):
        result = self.icon_service.get_block(self.valid_hash)
        self.assertTrue(is_block(result))


if __name__ == "__main__":
    main()
