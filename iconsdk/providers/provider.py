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

from abc import ABCMeta, abstractmethod
from typing import Optional, Dict, Any


class MonitorSpec(metaclass=ABCMeta):
    @abstractmethod
    def get_request(self) -> any:
        """
        Request object to send to the websocket
        """
        raise NotImplementedError("MonitorSpec must implement this method")

    @abstractmethod
    def get_path(self) -> str:
        """
        Extra path fragment for the websocket
        """
        raise NotImplementedError("MonitorSpec must implement this method")


class MonitorTimeoutException(Exception):
    pass


class Monitor(metaclass=ABCMeta):
    @abstractmethod
    def close(self):
        """
        Close the monitor

        It releases related resources.
        """
        pass

    @abstractmethod
    def read(self, timeout: Optional[float] = None) -> any:
        """
        Read the notification

        :param timeout: Timeout to wait for the message in fraction of seconds
        :except MonitorTimeoutException: if it passes the timeout
        """
        pass


class Provider(metaclass=ABCMeta):
    """The provider defines how the IconService connects to RPC server."""

    @abstractmethod
    def make_request(self, method: str, params: Optional[Dict[str, Any]] = None, full_response: bool = False):
        raise NotImplementedError("Providers must implement this method")

    @abstractmethod
    def make_monitor(self, spec: MonitorSpec, keep_alive: Optional[float] = None) -> Monitor:
        """
        Make monitor for the spec
        :param spec: Monitoring spec
        :param keep_alive: Keep-alive message interval in fraction of seconds
        """
        raise NotImplementedError()

