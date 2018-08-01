import unittest
import os

from IconService.wallet.wallet import KeyWallet
from IconService.exception import KeyStoreException


class TestWalletLoadFromKeystoreFile(unittest.TestCase):

    TEST_KEYSTORE_FILE_DIR = os.path.abspath("keystore_file/test_keystore.txt")
    TEST_KEYSTORE_FILE_PASSWORD = "Adas21312**"
    TEST_DIR = os.path.abspath("keystore_file")

    def test_wallet_load_from_keystore_file(self):
        """A wallet loads from a keystore file correctly."""

        # Loads a wallet.
        wallet = KeyWallet.load(self.TEST_KEYSTORE_FILE_DIR, self.TEST_KEYSTORE_FILE_PASSWORD)

        # Checks a wallet's address is correct.
        self.assertEqual(wallet.get_address(), "hxfd7e4560ba363f5aabd32caac7317feeee70ea57")

    def test_wallet_load_from_invalid_directory(self):
        """Case when loading a wallet from a invalid directory not existing."""
        keystore_file_path = os.path.join(self.TEST_DIR, "unknown_folder", "test_keystore.txt")

        try:
            wallet = KeyWallet.load(keystore_file_path, self.TEST_KEYSTORE_FILE_PASSWORD)
        except FileNotFoundError:
            self.assertTrue(True)

    def test_wallet_load_with_invalid_password(self):
        """Case When loading a wallet with a invalid password."""
        password = "1234wrongpassword"
        self.assertRaises(KeyStoreException, KeyWallet.load, self.TEST_KEYSTORE_FILE_DIR, password)




