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
import warnings
from abc import ABCMeta, abstractmethod
from hashlib import sha3_256

from coincurve import PrivateKey
from eth_keyfile import create_keyfile_json, extract_key_from_keyfile
from multipledispatch import dispatch

from iconsdk import logger
from iconsdk.exception import KeyStoreException, DataTypeException
from iconsdk.libs.signer import sign
from iconsdk.utils import store_keystore_file_on_the_path
from iconsdk.utils.validation import is_keystore_file


class Wallet(metaclass=ABCMeta):
    """An interface `Wallet` has 2 abstract methods, `get_address()` and `sign(hash: str)`."""

    @abstractmethod
    def get_address(self) -> str:
        """Gets a wallet address of wallet which starts with 'hx'.

        :return address: A wallet address
        """
        raise NotImplementedError("Wallet must implement this method")

    @abstractmethod
    def sign(self, data: bytes) -> bytes:
        """Generates signature from input data which is transaction data

        :param data: data to be signed
        :return signature: signature made from input
        """
        raise NotImplementedError("Wallet implement this method")


class KeyWallet(Wallet):
    """KeyWallet class implements Wallet."""

    def __init__(self, private_key_object: PrivateKey):
        self.__private_key: bytes = private_key_object.secret
        self.public_key: bytes = private_key_object.public_key.format(compressed=False)

    @staticmethod
    def create() -> 'KeyWallet':
        """Generates an instance of Wallet without a specific private key.

        :return: An instance of Wallet class.
        """
        private_key_object = PrivateKey()
        wallet = KeyWallet(private_key_object)
        logger.info(f"Created Wallet. Address: {wallet.get_address()}")
        return wallet

    @staticmethod
    @dispatch(bytes)
    def load(private_key: bytes) -> 'KeyWallet':
        """Loads a wallet from a private key and generates an instance of Wallet.

        :param private_key: private key in bytes
        :return: An instance of Wallet class.
        """
        try:
            private_key_object = PrivateKey(private_key)
            wallet = KeyWallet(private_key_object)
            logger.info(f"Loaded Wallet by the private key. Address: {wallet.get_address()}")
            return wallet
        except TypeError:
            logger.exception(
                f"Raised DataTypeException while loading wallet by private key because the private key is invalid.")
            raise DataTypeException("Private key is invalid.")

    @staticmethod
    @dispatch(str, str)
    def load(file_path: str, password: str) -> 'KeyWallet':
        """Loads a wallet from a keystore file with your password and generates an instance of Wallet.

        :param file_path: File path of the keystore file. type(str)
        :param password:
            Password for the keystore file.
            It must include alphabet character, number, and special character.
        :return: An instance of Wallet class.
        """
        try:
            with open(file_path, 'rb') as file:
                private_key: bytes = extract_key_from_keyfile(file, bytes(password, 'utf-8'))
                private_key_object = PrivateKey(private_key)
                wallet = KeyWallet(private_key_object)
                logger.info(
                    f"Loaded Wallet by the keystore file. Address: {wallet.get_address()}, File path: {file_path}")
                return wallet
        except FileNotFoundError:
            logger.exception(
                f"Raised KeyStoreException while loading the wallet by the keystore file because the file is not found.")
            raise KeyStoreException("File is not found.")
        except ValueError:
            logger.exception(
                f"Raised KeyStoreException while loading the wallet by the keystore file because the password is wrong.")
            raise KeyStoreException("Password is wrong.")
        except Exception as e:
            logger.exception(
                f"Raised KeyStoreException while loading the wallet by the keystore file. Error message: {e}")
            raise KeyStoreException(f'keystore file error.{e}')

    def store(self, file_path: str, password: str):
        """Stores data of an instance of a derived wallet class on the file path with your password.

        :param file_path: File path of the keystore file. type(str)
        :param password:
            Password for the keystore file. Password must include alphabet character, number, and special character.
            type(str)
        """
        try:
            key_store_contents = create_keyfile_json(
                self.__private_key,
                bytes(password, 'utf-8'),
                iterations=16384,
                kdf="scrypt"
            )
            key_store_contents['address'] = self.get_address()
            key_store_contents['coinType'] = 'icx'

            # validate the  contents of a keystore file.
            if is_keystore_file(key_store_contents):
                json_string_keystore_data = json.dumps(key_store_contents)
                store_keystore_file_on_the_path(file_path, json_string_keystore_data)
                logger.info(f"Stored Wallet. Address: {self.get_address()}, File path: {file_path}")
        except FileExistsError:
            logger.exception(
                f"Raised KeyStoreException while storing the wallet because the file already exists. "
                f"File path: {file_path}")
            raise KeyStoreException("File already exists.")
        except PermissionError:
            logger.exception(
                f"Raised KeyStoreException while storing the wallet because permission is not enough"
                f"File path: {file_path}")
            raise KeyStoreException("Not enough permission.")
        except FileNotFoundError:
            logger.exception(
                f"Raised KeyStoreException while storing the wallet because the file is not found."
                f"File path: {file_path}")
            raise KeyStoreException("File not found.")
        except IsADirectoryError:
            logger.exception(
                f"Raised KeyStoreException while storing the wallet because the directory is invalid."
                f"File path: {file_path}")
            raise KeyStoreException("Directory is invalid.")

    def get_private_key(self) -> str:
        """Returns the private key of the wallet.

        :return a private_key in hexadecimal.
        """
        return self.__private_key.hex()

    def get_address(self) -> str:
        """Returns an EOA address.

        :return address: An EOA address
        """
        return f'hx{sha3_256(self.public_key[1:]).digest()[-20:].hex()}'

    def sign(self, data: bytes) -> bytes:
        """Generates signature from input data which is transaction data

        :param data: data to be signed
        :return signature: signature made from input
        """
        return sign(data, self.__private_key)


def get_public_key(private_key_object: PrivateKey):
    warnings.warn("get_public_key is deprecated, use KeyWallet.public_key", DeprecationWarning)
    return private_key_object.public_key.format(compressed=False)
