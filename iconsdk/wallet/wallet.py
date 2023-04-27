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

from __future__ import annotations

import json
import warnings
from abc import ABCMeta, abstractmethod
from hashlib import sha3_256
from typing import Dict, Union, Any

from coincurve import PrivateKey, PublicKey
from eth_keyfile import create_keyfile_json, extract_key_from_keyfile, decode_keyfile_json
from multimethod import multimethod

from iconsdk import logger
from iconsdk.exception import DataTypeException, KeyStoreException
from iconsdk.libs.signer import sign
from iconsdk.utils import PathLikeObject, store_keystore_file_on_the_path
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
        self._private_key_object: PrivateKey = private_key_object

    @property
    def private_key(self) -> bytes:
        return self._private_key_object.secret

    @property
    def public_key(self) -> bytes:
        return self._private_key_object.public_key.format(compressed=False)

    @staticmethod
    def create() -> 'KeyWallet':
        """Generates an instance of Wallet without a specific private key.

        :return: An instance of Wallet class.
        """
        private_key_object = PrivateKey()
        wallet = KeyWallet(private_key_object)
        logger.info(f"Created Wallet. Address: {wallet.get_address()}")
        return wallet

    @multimethod
    def load(private_key: bytes) -> KeyWallet:
        """Loads a wallet from a private key and generates an instance of Wallet.

        :param private_key: private key in bytes
        :return: An instance of Wallet class.
        """
        try:
            wallet = KeyWallet(PrivateKey(private_key))
            logger.info(f"Loaded Wallet by the private key. Address: {wallet.get_address()}")
            return wallet
        except TypeError:
            raise DataTypeException("Private key is invalid.")

    @staticmethod
    @multimethod
    def load(file_path: PathLikeObject, password: str) -> KeyWallet:
        """Loads a wallet from a keystore file with your password and generates an instance of Wallet.

        :param file_path: File path of the keystore file. type(str | bytes | PathLike)
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
        except FileNotFoundError as e:
            raise KeyStoreException(f'File not found: {e}')
        except ValueError as e:
            raise KeyStoreException(f'Wrong password: {e}')
        except Exception as e:
            raise KeyStoreException(f'Keystore error: {e}')

    def store(self, file_path: PathLikeObject, password: str):
        """Stores data of an instance of a derived wallet class on the file path with your password.

        :param file_path: File path of the keystore file. type(str | bytes | PathLike)
        :param password:
            Password for the keystore file. Password must include alphabet character, number, and special character.
            type(str)
        """
        try:
            key_store_contents = self.to_dict(password)
            # validate the  contents of a keystore file.
            if is_keystore_file(key_store_contents):
                json_string_keystore_data = json.dumps(key_store_contents)
                store_keystore_file_on_the_path(file_path, json_string_keystore_data)
                logger.info(f"Stored Wallet. Address: {self.get_address()}, File path: {file_path}")
        except FileExistsError:
            raise KeyStoreException("File already exists.")
        except PermissionError:
            raise KeyStoreException("Not enough permission.")
        except FileNotFoundError:
            raise KeyStoreException("File not found.")
        except IsADirectoryError:
            raise KeyStoreException("Directory is invalid.")

    def to_dict(self, password: str) -> Dict[str, Any]:
        ret: Dict[str, Any] = create_keyfile_json(
            self.private_key,
            bytes(password, 'utf-8'),
            iterations=16384,
            kdf="scrypt"
        )
        ret['address'] = self.get_address()
        ret['coinType'] = 'icx'
        return ret

    @classmethod
    def from_dict(cls, jso: Dict[str, Any], password: str) -> KeyWallet:
        private_key: bytes = decode_keyfile_json(jso, password)
        return KeyWallet.load(private_key)

    def get_private_key(self, hexadecimal: bool = True) -> Union[str, bytes]:
        """Returns the private key of the wallet.
        """
        pri_key: bytes = self._private_key_object.secret
        return pri_key.hex() if hexadecimal else pri_key

    def get_public_key(self, compressed: bool = True, hexadecimal: bool = True) -> Union[str, bytes]:
        pub_key: bytes = self._private_key_object.public_key.format(compressed)
        return pub_key.hex() if hexadecimal else pub_key

    def get_address(self) -> str:
        """Returns an EOA address.

        :return address: An EOA address
        """
        return public_key_to_address(self._private_key_object.public_key.format(compressed=False))

    def sign(self, data: bytes) -> bytes:
        """Generates signature from input data which is transaction data

        :param data: data to be signed
        :return signature: signature made from input
        """
        return sign(data, self.private_key)

    def __eq__(self, other: KeyWallet) -> bool:
        return self.private_key == other.private_key

    def __ne__(self, other: KeyWallet) -> bool:
        return not self.__eq__(other)

    def __deepcopy__(self, memodict={}) -> KeyWallet:
        return KeyWallet.load(self.private_key)

    def __hash__(self):
        return hash(self._private_key_object.secret)


def public_key_to_address(public_key: bytes) -> str:
    if not (len(public_key) == 65 and public_key[0] == 4):
        pub_key = PublicKey(public_key)
        public_key: bytes = pub_key.format(compressed=False)
    return f'hx{sha3_256(public_key[1:]).digest()[-20:].hex()}'


def convert_public_key_format(public_key: bytes, compressed: bool) -> bytes:
    pub_key = PublicKey(public_key)
    return pub_key.format(compressed)


def get_public_key(private_key_object: PrivateKey):
    warnings.warn("get_public_key is deprecated, use KeyWallet.public_key", DeprecationWarning)
    return private_key_object.public_key.format(compressed=False)
