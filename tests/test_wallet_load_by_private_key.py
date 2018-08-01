import unittest

from IconService.wallet.wallet import KeyWallet
from secp256k1 import PrivateKey
from IconService.utils.validation import validate_address


class TestWalletLoadByPrivateKey(unittest.TestCase):

    def test_wallet_load_by_private_key(self):
        """A wallet loads by a private key correctly."""

        # Creates a wallet.
        private_key_object = PrivateKey()
        hex_private_key = private_key_object.private_key.hex()
        wallet1 = KeyWallet.load(hex_private_key)

        # Checks a private key as same.
        self.assertEqual(hex_private_key, wallet1.get_private_key())

        # Checks a wallet's address is correct.
        self.assertTrue(validate_address(wallet1.get_address()))

        # Creates the other wallet.
        private_key_object2 = PrivateKey()
        hex_private_key2 = private_key_object2.private_key.hex()
        wallet2 = KeyWallet.load(hex_private_key2)

        # Checks a private key as same.
        self.assertEqual(hex_private_key2, wallet2.get_private_key())

        # Checks a wallet's address is correct.
        self.assertTrue(validate_address(wallet2.get_address()))

        self.assertNotEqual(hex_private_key2, hex_private_key)

    def test_wallet_load_by_invalid_private_key(self):
        """A wallet loads by a wrong private key. It will fail."""

        try:
            # Given, When
            wallet = KeyWallet.load("71fc378d3a3fb92b57474af156f9d277c9b60a923a1db75575b1cc")

        # Then
        except TypeError:
            self.assertTrue(True)
