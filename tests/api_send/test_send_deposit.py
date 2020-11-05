import json

import requests_mock

from iconsdk.builder.transaction_builder import DepositTransactionBuilder, DepositTransaction
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_T_HASH
from tests.api_send.test_send_super import TestSendSuper
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


class TestSendDeposit(TestSendSuper):
    def test_add_deposit(self):
        action: str = "add"
        deposit_transaction_of_add_0: DepositTransaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(self.setting["value"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .action(action) \
            .timestamp(self.setting["timestamp"]) \
            .build()
        # Checks if sending transaction correctly
        signed_transaction = SignedTransaction(deposit_transaction_of_add_0, self.wallet)

        with requests_mock.Mocker() as m:
            tx_hash: str = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
            expected_result: dict = {
                "jsonrpc": "2.0",
                "result": tx_hash,
                "id": 1234
            }
            expected_request_body: dict = {
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
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", json=expected_result)
            result = self.icon_service.send_transaction(signed_transaction)
            self.assertTrue(is_T_HASH(result))
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)

    def test_withdraw_deposit(self):
        action: str = "withdraw"
        deposit_transaction_of_withdraw_0: DepositTransaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .id(self.setting["id"]) \
            .action("withdraw") \
            .timestamp(self.setting["timestamp"]) \
            .build()
        # Checks if sending transaction correctly
        signed_transaction = SignedTransaction(deposit_transaction_of_withdraw_0, self.wallet)

        with requests_mock.Mocker() as m:
            tx_hash: str = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
            expected_result: dict = {
                "jsonrpc": "2.0",
                "result": tx_hash,
                "id": 1234
            }
            expected_request_body: dict = {
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
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", json=expected_result)
            result = self.icon_service.send_transaction(signed_transaction)
            self.assertTrue(is_T_HASH(result))
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)
