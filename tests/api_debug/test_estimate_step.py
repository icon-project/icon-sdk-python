import json

import requests_mock

from iconsdk.builder.transaction_builder import DeployTransactionBuilder
from iconsdk.builder.transaction_builder import TransactionBuilder, MessageTransactionBuilder
from tests.api_send.test_send_super import TestSendSuper
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


class TestEstimateStep(TestSendSuper):
    def test_estimate_step_with_send_icx_transaction(self):
        expected_step: int = 100_000
        icx_transaction = TransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(self.setting["value"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .version(3) \
            .timestamp(self.setting["timestamp"]) \
            .build()

        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'debug_estimateStep',
                'params': {
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'stepLimit': hex(self.setting["step_limit"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to"],
                    'value': hex(self.setting["value"]),
                    'version': hex(3)
                }
            }
            ret_json: dict = {
                "jsonrpc": "2.0",
                "result": hex(expected_step),
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/debug/v3", json=ret_json)
            result = self.icon_service.estimate_step(icx_transaction)
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)

        self.assertEqual(expected_step, result)

    def test_estimate_step_with_message_transaction(self):
        expected_step: int = 102_400
        message_transaction = MessageTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .data(self.setting["data"]) \
            .timestamp(self.setting["timestamp"]) \
            .build()

        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'debug_estimateStep',
                'params': {
                    'data': self.setting["data"],
                    'dataType': 'message',
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'stepLimit': hex(self.setting["step_limit"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to"],
                    'version': '0x3'
                }
            }
            ret_json: dict = {
                "jsonrpc": "2.0",
                "result": hex(expected_step),
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/debug/v3", json=ret_json)
            result = self.icon_service.estimate_step(message_transaction)
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)
        self.assertEqual(expected_step, result)

    def test_estimate_step_with_deploy_transaction(self):
        param = {"init_supply": 10_000}
        expected_step: int = 1_042_767_600
        deploy_transaction = DeployTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]) \
            .content(self.setting["content_install"]) \
            .params(param) \
            .version(3) \
            .timestamp(self.setting["timestamp"]) \
            .build()

        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'debug_estimateStep',
                'params': {
                    'data': {
                        'content': f"0x{self.setting['content_install'].hex()}",
                        'contentType': self.setting["content_type"],
                        'params': {
                            'init_supply': hex(param["init_supply"])
                        }
                    },
                    'dataType': 'deploy',
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'stepLimit': hex(self.setting["step_limit"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to_install"],
                    'version': '0x3'
                }
            }
            ret_json: dict = {
                "jsonrpc": "2.0",
                "result": hex(expected_step),
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/debug/v3", json=ret_json)
            result = self.icon_service.estimate_step(deploy_transaction)
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)
        self.assertEqual(expected_step, result)
