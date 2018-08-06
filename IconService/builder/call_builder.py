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


class Call:
    """
    Class `Call` for calling a SCORE API.
    Once an instance generated, it is read-only."""
    def __init__(self, from_, to, method, params):
        self.__from  = from_
        self.__to = to
        self.__method = method
        self.__params = params

    @property
    def from_(self):
        return self.__from

    @property
    def to(self):
        return self.__to

    @property
    def method(self):
        return self.__method

    @property
    def params(self):
        return self.__params


class CallBuilder:
    """
    Builder for a `Call` object.
    Once setting it, a value of any property can't be changed forever.
    """
    def from_(self, from_):
        self.from_ = from_
        return self

    def to(self, to):
        self.to = to
        return self

    def method(self, method):
        self.method = method
        return self

    def params(self, params):
        self.params = params
        return self

    def build(self):
        return Call(self.from_, self.to, self.method, self.params)


