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

from os import path
from functools import wraps
from logging import StreamHandler, Formatter
from time import time
from iconsdk.utils.hexadecimal import add_0x_prefix


def store_keystore_file_on_the_path(file_path, json_string):
    """Stores a created keystore string data which is JSON format on the file path.

    :param file_path: The path where the file will be saved. type(str)
    :param json_string: Contents of the keystore.
    """
    if path.isfile(file_path):
        raise FileExistsError

    with open(file_path, 'wt') as f:
        f.write(json_string)


def apply_to_return_value(callback):
    def outer(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            return callback(fn(*args, **kwargs))

        return inner
    return outer


to_dict = apply_to_return_value(dict)


def set_logger(logger, level):
    handler = StreamHandler()
    formatter = Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)


def get_timestamp():
    """Get epoch time"""
    return add_0x_prefix(hex(int(time() * 10 ** 6)))


