import unittest
from hashlib import sha3_256
from unittest import TestCase

from iconsdk.libs import signer as signer1
from iconsdk.libs.serializer import serialize
from iconsdk.wallet.wallet import KeyWallet
from tests.example_config import PRIVATE_KEY_FOR_TEST
from tests.example_tx_requests import TEST_REQUEST_TRANSFER_ICX


@unittest.skip("no more install package Secp256k1")
class TestWalletCompatibilityWithSecp256k1(TestCase):
    """Test regarding to compatibility between secp256k1 and coincurve """
    def test_check_if_wallet_address_and_private_key_are_equal(self):
        from tests.wallet.backup_regarding_secp256k1.wallet_bk import KeyWallet as KeyWallet2

        wallet1 = KeyWallet.load(PRIVATE_KEY_FOR_TEST)
        wallet2 = KeyWallet2.load(PRIVATE_KEY_FOR_TEST)

        self.assertEqual(wallet1.get_address(), wallet2.get_address())
        self.assertEqual(wallet1.get_private_key(), wallet2.get_private_key())

    def test_check_if_wallet_signed_equally(self):
        from tests.wallet.backup_regarding_secp256k1 import signer_bk as signer2
        from tests.wallet.backup_regarding_secp256k1.wallet_bk import KeyWallet as KeyWallet2

        wallet1 = KeyWallet.load(PRIVATE_KEY_FOR_TEST)
        wallet2 = KeyWallet2.load(PRIVATE_KEY_FOR_TEST)

        msg = serialize(TEST_REQUEST_TRANSFER_ICX["params"])
        message_hash = sha3_256(msg).digest()
        sign1 = signer1.sign(message_hash, bytes.fromhex(wallet1.get_private_key()))
        sign2 = signer2.sign(message_hash, bytes.fromhex(wallet2.get_private_key()))
        self.assertEqual(sign1, sign2)
