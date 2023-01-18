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

import os
from functools import wraps
from logging import Formatter, StreamHandler
from time import time
from typing import Union

from iconsdk import logger

# https://docs.python.org/3/glossary.html#term-path-like-object
PathLikeObject = Union[str, bytes, os.PathLike]


def store_keystore_file_on_the_path(file_path: PathLikeObject, json_string: str):
    """Stores a created keystore string data which is JSON format on the file path.

    :param file_path: The path where the file will be saved. type(str)
    :param json_string: Contents of the keystore.
    """
    if os.path.isfile(file_path):
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


def set_logger(level, handler=StreamHandler(),
               format: str = '%(asctime)s %(name)-12s %(levelname)-5s '
                             '%(filename)-12s %(lineno)-4s %(funcName)-12s %(message)s') -> None:
    """ Set logger by setting level and handler

    :param level: the logging level of this logger. The level must be an int or a str.
    :param handler: the specified handler to be added to this logger
    :param format: the specified format strings which initialize the formatter with.
    :return: None
    """
    formatter = Formatter(format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)


def get_timestamp() -> str:
    """Returns the timestamp in microseconds since the epoch"""
    return hex(int(time() * 10 ** 6))
