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
from threading import Timer
from functools import wraps
from time import sleep
from logging import Logger


class RepeatedTimer(object):
    def __init__(self, interval, func, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.result = None
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.result = self.func(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def get(self):
        return self.result


def retry(exception_to_check: Exception or tuple, tries: int =10, delay: int =1, back_off: int=2, logger: Logger=None):
    """
    Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param exception_to_check: The exception to check. May be a tuple of exceptions to check
    :param tries: Number of times to try (not retry) before giving up
    :param delay: Initial delay between retries in seconds
    :param back_off: Back_off multiplier e.g. Value of 2 will double the delay each retry
    :param logger: Logger to use. If None, print
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exception_to_check as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    sleep(mdelay)
                    mtries -= 1
                    mdelay *= back_off
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry


