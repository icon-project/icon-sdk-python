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
from hashlib import sha3_256
from abc import ABCMeta, abstractmethod
from secp256k1 import PrivateKey
from iconsdk.utils.validation import is_password_of_keystore_file, is_keystore_file
from iconsdk.exception import KeyStoreException, DataTypeException
from eth_keyfile import load_keyfile, decode_keyfile_json, create_keyfile_json
from multipledispatch import dispatch
from iconsdk.utils import store_keystore_file_on_the_path
from iconsdk.libs.signer import sign


class Wallet(metaclass=ABCMeta):
    """An interface `Wallet` has 2 abstract methods, `get_address()` and `sign_message(hash: str)`."""

    @abstractmethod
    def get_address(self) -> str:
        """Gets a wallet address of wallet which starts with 'hx'.

        :return address: A wallet address
        """
        raise NotImplementedError("Wallet must implement this method")

    @abstractmethod
    def sign(self, data: bytes) -> str:
        """Generates signature from input data which is transaction data

        :param data: data to be signed
        :return signature: signature made from input
        """
        raise NotImplementedError("Wallet implement this method")


class KeyWallet(Wallet):
    """KeyWallet class implements Wallet."""

    def __init__(self, private_key_object):
        self.__bytes_private_key = private_key_object.private_key
        self.bytes_public_key = get_public_key(private_key_object)
        self.address = get_address(self.bytes_public_key)

    @staticmethod
    def create():
        """Generates an instance of Wallet without a specific private key.

        :return: An instance of Wallet class.
        """
        private_key_object = PrivateKey()
        wallet = KeyWallet(private_key_object)
        return wallet

    @staticmethod
    @dispatch(bytes)
    def load(private_key: bytes):
        """Loads a wallet from a private key and generates an instance of Wallet.

        :param private_key: private key in bytes
        :return: An instance of Wallet class.
        """
        try:
            private_key_object = PrivateKey(private_key)
            wallet = KeyWallet(private_key_object)
            return wallet
        except TypeError:
            raise DataTypeException("Private key is invalid.")

    @staticmethod
    @dispatch(str, str)
    def load(file_path, password):
        """Loads a wallet from a key store file with your password and generates an instance of Wallet.

        :param file_path: File path of the key store file. type(str)
        :param password:
            Password for the key store file.
            It must include alphabet character, number, and special character.
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

        :param file_path: File path of the key store file. type(str)
        :param password:
            Password for the key store file. Password must include alphabet character, number, and special character.
            type(str)
        """

        if not is_password_of_keystore_file(password):
            raise KeyStoreException('Invalid password.')

        try:
            key_store_contents = create_keyfile_json(
                self.__bytes_private_key,
                bytes(password, 'utf-8'),
                iterations=16384
            )
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
        """Returns the private key of the wallet.

        :return a private_key in hexadecimal.
        """
        return self.__bytes_private_key.hex()

    def get_address(self) -> str:
        """Returns an EOA address.

        :return address: An EOA address
        """
        return self.address

    def sign(self, data: bytes) -> bytes:
        """Generates signature from input data which is transaction data

        :param data: data to be signed
        :return signature: signature made from input
        """
        return sign(data, self.__bytes_private_key)


def get_public_key(private_key_object):
    return private_key_object.pubkey.serialize(compressed=False)


def get_address(bytes_public_key):
    return f'hx{sha3_256(bytes_public_key[1:]).digest()[-20:].hex()}'
