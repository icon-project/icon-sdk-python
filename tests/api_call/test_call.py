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
import json
from unittest import main
from unittest.mock import patch

import requests_mock

from iconsdk.builder.call_builder import CallBuilder
from tests.api_send.test_send_super import TestSendSuper


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestCall(TestSendSuper):

    def test_call(self, _make_id):

        # with from
        test_call = CallBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .method("getStepCosts") \
            .params({}) \
            .build()

        with requests_mock.Mocker() as m:
            expected_request = {
                "jsonrpc": "2.0",
                "method": "icx_call",
                "id": 1234,
                "params": {
                    "to": self.setting["to"],
                    "dataType": "call",
                    "data": {
                        "method": "getStepCosts"
                    },
                    "from": self.setting["from"]
                }
            }

            m.post(self.matcher, json=response_json)
            result = self.icon_service.call(test_call)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
            self.assertTrue(result)

    def test_call_without_params(self, _make_id):
        test_call = CallBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .method("getStepCosts") \
            .build()

        with requests_mock.Mocker() as m:
            expected_request = {
                "jsonrpc": "2.0",
                "method": "icx_call",
                "id": 1234,
                "params": {
                    "to": self.setting["to"],
                    "dataType": "call",
                    "data": {
                        "method": "getStepCosts"
                    },
                    "from": self.setting["from"]
                }
            }
            m.post(self.matcher, json=response_json)
            result = self.icon_service.call(test_call)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
            self.assertTrue(result)

    def test_call_without_from(self, _make_id):
        test_call = CallBuilder() \
            .to(self.setting["to"]) \
            .method("getStepCosts") \
            .build()

        with requests_mock.Mocker() as m:
            expected_request = {
                "jsonrpc": "2.0",
                "method": "icx_call",
                "id": 1234,
                "params": {
                    "to": self.setting["to"],
                    "dataType": "call",
                    "data": {
                        "method": "getStepCosts"
                    },
                }
            }
            m.post(self.matcher, json=response_json)
            result = self.icon_service.call(test_call)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
            self.assertTrue(result)


response_json = {
    "jsonrpc": "2.0",
    "result": {
        "default": "0x186a0",
        "contractCall": "0x61a8",
        "contractCreate": "0x3b9aca00",
        "contractUpdate": "0x5f5e1000",
        "contractDestruct": "-0x11170",
        "contractSet": "0x7530",
        "get": "0x0",
        "set": "0x140",
        "replace": "0x50",
        "delete": "-0xf0",
        "input": "0xc8",
        "eventLog": "0x64",
        "apiCall": "0x2710"
    },
    "id": 1234
}


if __name__ == "__main__":
    main()
