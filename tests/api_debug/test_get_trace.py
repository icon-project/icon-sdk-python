# -*- coding: utf-8 -*-
# Copyright 2021 ICON Foundation
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
import json
from unittest import main
from unittest.mock import patch

import requests_mock

from iconsdk.exception import DataTypeException
from tests.api_send.test_send_super import TestSendSuper


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestGetTrace(TestSendSuper):
    TX_HASH = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"

    def test_get_trace(self, _make_id):
        with requests_mock.Mocker() as m:
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'debug_getTrace',
                'params': {
                    'txHash': TestGetTrace.TX_HASH
                }
            }
            response_json = {
                "jsonrpc": "2.0",
                "result": {"logs": [], "status": "0x1"},
                "id": 1234
            }
            m.post(self.matcher, json=response_json)
            self.icon_service.get_trace(TestGetTrace.TX_HASH)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)

    def test_get_trace_invalid(self, _make_id):
        tx_hash = TestGetTrace.TX_HASH
        self.assertRaises(DataTypeException, self.icon_service.get_trace, tx_hash[2:])
        self.assertRaises(DataTypeException, self.icon_service.get_trace, "123")
        self.assertRaises(DataTypeException, self.icon_service.get_trace, 123)
        self.assertRaises(DataTypeException, self.icon_service.get_trace, tx_hash[:len(tx_hash)-1])


if __name__ == "__main__":
    main()
