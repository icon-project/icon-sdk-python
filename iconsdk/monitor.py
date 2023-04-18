#  Copyright 2023 ICON Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from __future__ import annotations

from typing import List, Dict, Any

from iconsdk.providers.provider import MonitorSpec
from iconsdk.utils.typing.conversion import object_to_str


class EventFilter:
    def __init__(self, event: str, addr: str, indexed: int, *args):
        self.__event = event
        self.__addr = addr
        self.__indexed = list(args[0:indexed])
        self.__data = list(args[indexed:])

    def apply_to(self, obj: Dict[str, Any]):
        obj.update({
            "event": self.__event,
            "indexed": self.__indexed,
            "data": self.__data,
        })
        if self.__addr is not None:
            obj.update({
                "addr": self.__addr
            })

    def as_dict(self) -> Dict[str, Any]:
        obj = {}
        self.apply_to(obj)
        return obj


class EventMonitorSpec(MonitorSpec):
    def __init__(self, height: int | None,
                 filters: EventFilter | List[EventFilter],
                 logs: bool = False,
                 progress_interval: int = 0):
        self.__height = height
        self.__logs = logs
        if type(filters) is EventFilter:
            self.__filters = list([filters])
        else:
            self.__filters = filters
        self.__progress_interval = progress_interval

    def get_path(self) -> str:
        return 'event'

    def get_request(self) -> any:
        params = {}
        if self.__height is not None:
            params["height"] = self.__height
        if self.__logs:
            params["logs"] = True
        if self.__progress_interval > 0:
            params["progressInterval"] = self.__progress_interval
        if len(self.__filters) == 1:
            self.__filters[0].apply_to(params)
        else:
            params["filters"] = list(map(lambda a: a.as_dict(), self.__filters))
        return object_to_str(params)


class BlockMonitorSpec(MonitorSpec):
    def __init__(self, height: int | None,
                 filters: EventFilter|List[EventFilter]|None = None,
                 logs: bool = False):
        """
        Block monitoring spec

        :param height: Block height to start monitoring
        :param filters: One event filter or list of event filters
        :param logs: Whether the notification includes logs or not
        """
        self.__height = height
        self.__logs = logs
        if type(filters) is EventFilter:
            self.__filters = list([filters])
        else:
            self.__filters = filters

    def get_path(self) -> str:
        return 'block'

    def get_request(self) -> Dict[str, Any]:
        params = {}
        if self.__height is not None:
            params["height"] = self.__height
        if self.__logs:
            params["logs"] = True
        if len(self.__filters) == 1:
            self.__filters[0].apply_to(params)
        else:
            params["eventFilters"] = list(map(lambda a: a.as_dict(), self.__filters))
        return object_to_str(params)


class BTPMonitorSpec(MonitorSpec):
    def __init__(self, height: int | None,
                 network_id: int,
                 proof_flag: bool = False,
                 progress_interval: int = 0):
        """
        BTP Block event monitoring specification.
        https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#block

        :param height: Height of the block to start monitoring
        :param network_id: Network ID of the BTP Network
        :param proof_flag: Whether it includes proof data or not
        :param progress_interval: Progress interval to notify progress
        """
        self.__height = height
        self.__network_id = network_id
        self.__proof_flag = proof_flag
        self.__progress_interval = progress_interval

    def get_path(self) -> str:
        return 'btp'

    def get_request(self) -> Dict[str, Any]:
        params = {
            "networkID": self.__network_id,
        }
        if self.__height is not None:
            params["height"] = self.__height
        if self.__proof_flag:
            params['proofFlag'] = True
        if self.__progress_interval > 0:
            params["progressInterval"] = self.__progress_interval
        return object_to_str(params)
