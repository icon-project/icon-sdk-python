import unittest
from IconService.wallet.wallet import KeyWallet, get_public_key
from IconService.utils.validation import validate_address


class TestWalletCreate(unittest.TestCase):

    def test_wallet_create_successfully(self):
        """Case both of each wallets are created successfully without a private key."""
        wallet1 = KeyWallet.create()
        wallet2 = KeyWallet.create()
        self.assertTrue(wallet1.get_address() != wallet2.get_address())
        self.assertTrue(validate_address(wallet1.get_address()))
        self.assertTrue(validate_address(wallet2.get_address()))

