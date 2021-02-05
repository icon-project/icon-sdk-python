import requests_mock
import json

from unittest.mock import patch
from iconsdk.builder.transaction_builder import DepositTransactionBuilder, DepositTransaction
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_T_HASH
from tests.api_send.test_send_super import TestSendSuper
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestSendDeposit(TestSendSuper):

    def test_add_deposit(self, _make_id):
        # transaction instance for add action
        action = "add"
        deposit_transaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(self.setting["value"]) \
            .timestamp(self.setting["timestamp"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .action("add") \
            .build()
        signed_transaction = SignedTransaction(deposit_transaction, self.wallet)

        with requests_mock.Mocker() as m:
            tx_hash = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_sendTransaction',
                'params': {
                    'data': {
                        'action': action
                    },
                    'dataType': 'deposit',
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'signature': signed_transaction.signed_transaction_dict["signature"],
                    'stepLimit': hex(self.setting["step_limit"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to"],
                    'value': hex(self.setting["value"]),
                    'version': hex(3)
                }
            }

            response_json = {
                "jsonrpc": "2.0",
                "result": tx_hash,
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json)
            result = self.icon_service.send_transaction(signed_transaction)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
            self.assertTrue(result)

        # Checks if sending transaction correctly
        # signed_transaction_dict = SignedTransaction(deposit_transaction_of_add_0, self.wallet)
        # result = self.icon_service.send_transaction(signed_transaction_dict)
        # self.assertTrue(is_T_HASH(result))

    def test_withdraw_deposit(self, _make_id):
        # transaction instance for withdraw action
        action = 'withdraw'
        withdraw_transaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]) \
            .timestamp(self.setting["timestamp"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .id(self.setting["id"]) \
            .action(action) \
            .build()
        signed_transaction = SignedTransaction(withdraw_transaction, self.wallet)

        with requests_mock.Mocker() as m:
            tx_hash = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_sendTransaction',
                'params': {
                    'data': {
                        'action': action,
                        'id': self.setting["id"],
                    },
                    'dataType': 'deposit',
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'signature': signed_transaction.signed_transaction_dict["signature"],
                    'stepLimit': hex(self.setting["step_limit"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to"],
                    'version': hex(3)
                }
            }

            response_json = {
                "jsonrpc": "2.0",
                "result": tx_hash,
                "id": 1234
            }
            # Checks if sending transaction correctly
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json)
            result = self.icon_service.send_transaction(signed_transaction)
            self.assertTrue(is_T_HASH(result))
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
