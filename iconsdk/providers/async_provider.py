from abc import ABCMeta, abstractmethod

from .provider import MonitorSpec
from typing import Any, Dict, Optional


class AsyncMonitor(metaclass=ABCMeta):
    @abstractmethod
    async def read(self, timeout: Optional[float] = None) -> any:
        """
        Read the notification

        :param timeout: Timeout to wait for the message in fraction of seconds
        :except MonitorTimeoutException: if it passes the timeout
        """
        pass

    @abstractmethod
    async def close(self):
        """
        Close the monitor

        It releases related resources.
        """
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class AsyncProvider(metaclass=ABCMeta):
    """The provider defines how the IconService connects to RPC server."""

    @abstractmethod
    async def make_request(self, method: str, params: Optional[Dict[str, Any]] = None, full_response: bool = False):
        raise NotImplementedError("Providers must implement this method")

    @abstractmethod
    async def make_monitor(self, spec: MonitorSpec, keep_alive: Optional[float] = None) -> AsyncMonitor:
        """
        Make monitor for the spec
        :param spec: Monitoring spec
        :param keep_alive: Keep-alive message interval in fraction of seconds
        """
        raise NotImplementedError()

    @abstractmethod
    async def close(self):
        """
        Close the provider
        """
        raise NotImplementedError()