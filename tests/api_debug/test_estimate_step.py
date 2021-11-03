import json
import re
from unittest.mock import patch

import requests_mock

from iconsdk.builder.transaction_builder import DeployTransactionBuilder, CallTransactionBuilder
from iconsdk.builder.transaction_builder import TransactionBuilder, MessageTransactionBuilder
from tests.api_send.test_send_super import TestSendSuper
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestEstimateStep(TestSendSuper):
    matcher = re.compile(re.escape(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3d/") + "?")

    def test_estimate_step_with_send_icx_transaction(self, _make_id):
        icx_transaction = TransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(self.setting["value"]) \
            .timestamp(self.setting["timestamp"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .version(self.version) \
            .build()

        with requests_mock.Mocker() as m:
            expected_step = 100_000
            expected_request = {
                'jsonrpc': '2.0',
                'method': 'debug_estimateStep',
                'id': 1234,
                'params': {
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to"],
                    'value': hex(self.setting["value"]),
                    'version': hex(self.version)
                }
            }

            response_json = {
                'jsonrpc': '2.0',
                'result': hex(expected_step),
                'id': 1234
            }

            m.post(self.matcher, json=response_json)
            result = self.icon_service.estimate_step(icx_transaction)
            actual_request = json.loads(m._adapter.last_request.text)

            self.assertEqual(expected_request, actual_request)
            self.assertEqual(expected_step, result)

    def test_estimate_step_with_message_transaction(self, _make_id):
        # Checks if making an instance of message transaction correctly
        message_transaction = MessageTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]) \
            .timestamp(self.setting["timestamp"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .data(self.setting["data"]).build()

        with requests_mock.Mocker() as m:
            expected_step = 102_400
            expected_request = {
                'jsonrpc': '2.0',
                'method': 'debug_estimateStep',
                'id': 1234,
                'params': {
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to"],
                    'version': hex(self.version),
                    'data': self.setting["data"],
                    'dataType': 'message'
                }
            }

            response_json = {
                'jsonrpc': '2.0',
                'result': hex(expected_step),
                'id': 1234
            }

            m.post(self.matcher, json=response_json)
            result = self.icon_service.estimate_step(message_transaction)
            actual_request = json.loads(m._adapter.last_request.text)

            self.assertEqual(expected_request, actual_request)
            self.assertEqual(expected_step, result)

    def test_estimate_step_with_deploy_transaction(self, _make_id):
        param = {"init_supply": 10000}
        deploy_transaction = DeployTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .timestamp(self.setting["timestamp"]) \
            .content_type(self.setting["content_type"]) \
            .content(self.setting["content_install"]) \
            .params(param) \
            .version(3) \
            .build()

        with requests_mock.Mocker() as m:
            expected_step = 1_042_767_600
            expected_request = {
                'jsonrpc': '2.0',
                'method': 'debug_estimateStep',
                'id': 1234,
                'params': {
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to_install"],
                    'version': hex(self.version),
                    'data': {
                        'contentType': self.setting["content_type"],
                        'content': f'0x{self.setting["content_install"].hex()}',
                        'params': {'init_supply': hex(param["init_supply"])}
                    },
                    'dataType': 'deploy'
                }
            }

            response_json = {
                'jsonrpc': '2.0',
                'result': hex(expected_step),
                'id': 1234
            }

            m.post(self.matcher, json=response_json)
            result = self.icon_service.estimate_step(deploy_transaction)
            actual_request = json.loads(m._adapter.last_request.text)

            self.assertEqual(expected_request, actual_request)
            self.assertEqual(expected_step, result)

    def test_estimate_step_with_call_transaction(self, _make_id):
        params = {"addr_to": self.setting["to"], "value": 1000000}
        call_transaction = CallTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to("cx4d6f646441a3f9c9b91019c9b98e3c342cceb114") \
            .nid(self.setting["nid"]) \
            .timestamp(self.setting["timestamp"]) \
            .nonce(self.setting["nonce"]) \
            .method("transfer") \
            .params(params) \
            .build()
        with requests_mock.Mocker() as m:
            expected_step = 155_160

            expected_request = {
                'jsonrpc': '2.0',
                'method': 'debug_estimateStep',
                'id': 1234,
                'params': {
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': "cx4d6f646441a3f9c9b91019c9b98e3c342cceb114",
                    'version': hex(self.version),
                    'dataType': 'call',
                    'data': {
                        'method': 'transfer',
                        'params': {
                            'addr_to': 'hx5bfdb090f43a808005ffc27c25b213145e80b7cd',
                            'value': '0xf4240'
                        }
                    }
                }
            }

            response_json = {
                'jsonrpc': '2.0',
                'result': hex(expected_step),
                'id': 1234
            }
            m.post(self.matcher, json=response_json)
            result = self.icon_service.estimate_step(call_transaction)
            actual_request = json.loads(m._adapter.last_request.text)

            self.assertEqual(expected_request, actual_request)
            self.assertEqual(expected_step, result)

