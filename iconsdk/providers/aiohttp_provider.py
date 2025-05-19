# -*- coding: utf-8 -*-
# Copyright 2024 ICON Foundation
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

import asyncio
import json
from json import JSONDecodeError
from time import monotonic
from typing import Any, Dict, Optional

import aiohttp
from ..exception import JSONRPCException, HTTPError

from .async_provider import AsyncMonitor, AsyncProvider

from .provider import (MonitorSpec,
                       MonitorTimeoutException)
from .url_map import URLMap


class AIOHTTPProvider(AsyncProvider):
    """
    Async Provider implementation using the aiohttp library for HTTP requests.
    Connects to a standard ICON JSON-RPC endpoint.
    """

    def __init__(self, full_path_url: str,
                 request_kwargs: Optional[Dict[str, Any]] = None,
                 ):
        """
        Initializes AIOHTTPProvider.

        :param full_path_url: The URL of the ICON node's JSON-RPC endpoint (e.g., "https://ctz.solidwallet.io/api/v3/icon_dex").
                              It should include channel name if you want to use socket.
        :param session: An optional existing aiohttp ClientSession. If None, a new session is created.
                        Using an external session is recommended for better resource management.
        :param request_kwargs: Optional dictionary of keyword arguments to pass to aiohttp session requests
                               (e.g., {'timeout': 10}).
        """
        self._url = URLMap(full_path_url)
        self._request_kwargs = request_kwargs or {}
        if 'headers' not in self._request_kwargs:
            self._request_kwargs['headers'] = {'Content-Type': 'application/json'}
        self._request_id = 0  # Simple counter for JSON-RPC request IDs


    async def make_request(self, method: str, params: Optional[Dict[str, Any]] = None, full_response: bool = False) -> Any:
        """
        Makes an asynchronous JSON-RPC request to the ICON node.

        :param method: The JSON-RPC method name (e.g., 'icx_getLastBlock').
        :param params: A dictionary of parameters for the JSON-RPC method.
        :param full_response: If True, returns the entire JSON-RPC response object.
                              If False (default), returns only the 'result' field.
        :return: The JSON-RPC response 'result' or the full response dictionary.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request/response.
        :raise JsonRpcError: If the JSON-RPC response contains an error object.
        :raise ValueError: If the response is not valid JSON or missing expected fields.
        """
        self._request_id += 1

        payload: dict = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self._request_id,
        }
        if params is not None:
            payload["params"] = params

        request_url = self._url.for_rpc(method.split('_')[0])
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.post(request_url, json=payload, **self._request_kwargs)
                # Raise exception for non-2xx HTTP status codes
                resp_json = await response.json()
                if full_response:
                    return resp_json

                if response.ok:
                    return resp_json['result']
                raise JSONRPCException(
                    resp_json['error']['message'],
                    resp_json['error']['code'],
                    resp_json['error'].get("data", None),
                )
        except JSONDecodeError:
            raw_response = await response.text()
            raise HTTPError(raw_response, response.status)

    async def make_monitor(self, spec: MonitorSpec, keep_alive: Optional[float] = None) -> AsyncMonitor:
        """
        Creates a monitor for receiving real-time events via WebSocket (Not Implemented).

        :param spec: Monitoring specification defining the events to subscribe to.
        :param keep_alive: Keep-alive message interval in seconds.
        :return: A Monitor object for reading events.
        :raise NotImplementedError: This provider does not currently support monitoring.
        """
        ws_url = self._url.for_ws(spec.get_path())
        params = spec.get_request()
        monitor = AIOWebSocketMonitor(aiohttp.ClientSession(), ws_url, params, keep_alive=keep_alive)
        await monitor._connect()
        return monitor

class AIOWebSocketMonitor(AsyncMonitor):
    def __init__(self, session: aiohttp.ClientSession, url: str, params: dict, keep_alive: Optional[float] = None):
        self.__session = session
        self.__url = url
        self.__params = params
        self.__keep_alive = keep_alive or 30
        self.__ws = None

    async def __aenter__(self):
        if self.__ws is None:
            raise Exception("WebSocket is not connected")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return self

    async def _connect(self):
        if self.__ws is not None:
            raise Exception("WebSocket is already connected")
        self.__ws = await self.__session.ws_connect(self.__url)
        await self.__ws.send_json(self.__params)
        result = await self.__read_json(None)
        if 'code' not in result:
            raise Exception(f'invalid response={json.dumps(result)}')
        if result['code'] != 0:
            raise Exception(f'fail to monitor err={result["message"]}')

    async def close(self):
        if self.__ws:
            ws = self.__ws
            self.__ws = None
            await ws.close()

    async def __read_json(self, timeout: Optional[float] = None) -> any:
        now = monotonic()
        limit = None
        if timeout is not None:
            limit = now + timeout

        while True:
            try:
                if limit is not None:
                    timeout_left = min(limit - now, self.__keep_alive)
                else:
                    timeout_left = self.__keep_alive
                msg = await self.__ws.receive_json(timeout=timeout_left)
                return msg
            except asyncio.TimeoutError as e:
                now = monotonic()
                if limit is None or now < limit:
                    await self.__ws.send_json({"keepalive": "0x1"})
                    continue
                else:
                    raise MonitorTimeoutException()
            except Exception as e:
                raise e

    async def read(self, timeout: Optional[float] = None) -> any:
        return await self.__read_json(timeout=timeout)
