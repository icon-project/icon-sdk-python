# -*- coding: utf-8 -*-
# Copyright 2017-2018 theloop Inc.
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

import hashlib
import json
from abc import ABCMeta, abstractmethod
from secp256k1 import PrivateKey
from IconService.utils.validation import is_password_of_keystore_file, is_keystore_file
from IconService.exception import KeyStoreException
from eth_keyfile import load_keyfile, decode_keyfile_json, create_keyfile_json
from multipledispatch import dispatch
from IconService.utils import store_keystore_file_on_the_path
from IconService.libs.signer import sign, sign_b64encode


class Wallet(metaclass=ABCMeta):
    """An interface `Wallet` has 2 abstract methods, `get_address()` and `sign_message(hash: str)`."""

    @abstractmethod
    def get_address(self) -> str:
        """Gets a wallet address of wallet which starts with 'hx'.

        :return address:
        """
        raise NotImplementedError("Wallet must implement this method")

    @abstractmethod
    def sign_message(self, message_hash: bytes) -> str:
        """Makes a plain transaction message signature.

        :param message_hash: type(bytes)
        :return signature: type(str)
        """
        raise NotImplementedError("Wallet implement this method")


class KeyWallet(Wallet):
    """KeyWallet class implements Wallet."""

    def __init__(self, private_key_object):
        self.__bytes_private_key = private_key_object.private_key
        self.bytes_public_key = get_public_key(private_key_object)
        self.address = get_address(self.bytes_public_key)

    # @property
    # def public_key(self) -> bytes:
    #     return self._private_key_object.pubkey.serialize(compressed=False)
    #
    # @property
    # def address(self) -> bytes:
    #     return hashlib.sha3_256(self.public_key[1:]).digest()[-20:]

    @staticmethod
    def create():
        """Creates an instance of Wallet without a specific private key.

        :return: An instance of Wallet class.
        """
        private_key_object = PrivateKey()
        wallet = KeyWallet(private_key_object)
        return wallet

    @staticmethod
    @dispatch(str)
    def load(hex_private_key: str):
        """Creates an instance of Wallet with a specific private key.

        :param hex_private_key: in hexadecimal. type(str)
        :return: An instance of Wallet class.
        """
        private_key_object = PrivateKey(bytes.fromhex(hex_private_key))
        wallet = KeyWallet(private_key_object)
        return wallet

    @staticmethod
    @dispatch(str, str)
    def load(file_path, password):
        """Loads data in the keystore file on the file path with your password.

        :param file_path: type(str)
        :param password: a password including alphabet characters, numbers and special characters. stype(str)
        :return: An instance of Wallet class.
        """
        if not is_password_of_keystore_file(password):
            raise KeyStoreException('Invalid password.')

        keystore = load_keyfile(file_path)
        if is_keystore_file(keystore):
            bytes_private_key = decode_keyfile_json(keystore, bytes(password, 'utf-8'))
            private_key_object = PrivateKey(bytes_private_key)
            wallet = KeyWallet(private_key_object)
            return wallet

    def store(self, file_path, password):
        """Stores data of an instance of a derived wallet class on the file path with your password.

        :param file_path: type(str)
        :param password: type(str)
        :return: An instance of Wallet class.
        """

        if not is_password_of_keystore_file(password):
            raise KeyStoreException('Invalid password.')

        try:
            key_store_contents = create_keyfile_json(self.__bytes_private_key, bytes(password, 'utf-8'), iterations=262144)
            key_store_contents['address'] = self.get_address()
            key_store_contents['coinType'] = 'icx'

            # validate the  contents of a keystore file.
            if is_keystore_file(key_store_contents):
                json_string_keystore_data = json.dumps(key_store_contents)
                store_keystore_file_on_the_path(file_path, json_string_keystore_data)
        except FileExistsError:
            raise KeyStoreException("File already exists.")
        except PermissionError:
            raise KeyStoreException("Not enough permission.")
        except FileNotFoundError:
            raise KeyStoreException("File not found.")
        except IsADirectoryError:
            raise KeyStoreException("Directory is invalid.")

    def get_private_key(self) -> str:
        """Gets a private key of an instance of a derived wallet class.

        :return a private_key in hexadecimal.
        """
        return self.__bytes_private_key.hex()

    def get_address(self) -> str:
        """Gets a wallet address of wallet which starts with 'hx'.

        :return address:
        """
        return self.address

    def sign_message(self, message_hash: bytes) -> bytes:
        """Makes a plain transaction message signature.

        :param message_hash:
        :return signature: type(bytes)
        """
        return (sign_b64encode(sign(message_hash, self.__bytes_private_key))).decode()


def get_public_key(private_key_object):
    return private_key_object.pubkey.serialize(compressed=False)


def get_address(bytes_public_key):
    return f'hx{hashlib.sha3_256(bytes_public_key[1:]).digest()[-20:].hex()}'
