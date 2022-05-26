# -*- coding: utf-8 -*-
# Copyright 2022 ICON Foundation
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

from tests.api_send.test_send_super import TestSendSuper


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestBTP2(TestSendSuper):
    HEIGHT = 100
    ID = 1

    @staticmethod
    def convert_param(param: dict) -> dict:
        def _convert_key(k: str):
            if k.endswith("_id"):
                return k[:len(k)-3] + "ID"
            return k

        def _convert_value(v):
            if isinstance(v, int):
                return hex(v)
            return v

        result = {}
        for k, v in param.items():
            result[_convert_key(k)] = _convert_value(v)
        return result

    def run_test(self, _make_id, func: callable, method: str, params: dict):
        with requests_mock.Mocker() as m:
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': method,
            }
            response_json = {
                "jsonrpc": "2.0",
                "result": hex(0),
                "id": 1234
            }
            m.post(self.matcher, json=response_json)
            if params is not None:
                expected_request['params'] = self.convert_param(params)
                func(**params)
            else:
                func()
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)

    def test_btp_get_network_info(self, _make_id):
        func = self.icon_service.btp_get_network_info
        method = "btp_getNetworkInfo"
        params = {
            'height': self.HEIGHT,
            'id': self.ID
        }
        self.run_test(_make_id, func, method, params)

    def test_btp_get_network_type_info(self, _make_id):
        func = self.icon_service.btp_get_network_type_info
        method = "btp_getNetworkTypeInfo"
        params = {
            'height': self.HEIGHT,
            'id': self.ID,
        }
        self.run_test(_make_id, func, method, params)

    def test_btp_get_messages(self, _make_id):
        func = self.icon_service.btp_get_messages
        method = "btp_getMessages"
        params = {
            'height': self.HEIGHT,
            'network_id': self.ID,
        }
        self.run_test(_make_id, func, method, params)

    def test_btp_header(self, _make_id):
        func = self.icon_service.btp_get_header
        method = "btp_getHeader"
        params = {
            'height': self.HEIGHT,
            'network_id': self.ID,
        }
        self.run_test(_make_id, func, method, params)

    def test_btp_proof(self, _make_id):
        func = self.icon_service.btp_get_proof
        method = "btp_getProof"
        params = {
            'height': self.HEIGHT,
            'network_id': self.ID,
        }
        self.run_test(_make_id, func, method, params)

    def test_btp_source_information(self, _make_id):
        func = self.icon_service.btp_get_source_information
        method = "btp_getSourceInformation"
        params = None
        self.run_test(_make_id, func, method, params)


if __name__ == "__main__":
    main()
