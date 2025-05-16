from ..exception import URLException

import re
from urllib.parse import urlparse, urlunparse

URL_PATH_FORMAT = r'/api/v(?P<version>\d+)d?(/(?P<channel>[^/]+))?'

class URLMap:
    def __init__(self, base_url=None, version=None, channel=None):
        # If base_url has full path to specific channel, then we utilize it.
        uri = urlparse(base_url)

        if version is None:
            mo: re.Match = re.compile(URL_PATH_FORMAT).match(uri.path)
            if not mo:
                raise URLException(f'Invalid URL: {base_url}')
            version, channel = mo.group('version', 'channel')
        elif uri.path != '':
            raise URLException('Path is not allowed')

        self.serverUri = f'{uri.scheme}://{uri.netloc}'

        def _add_channel_path(url: str):
            if channel:
                return f"{url}/{channel}"
            return url

        self.rpc = {
            "icx": _add_channel_path(f"{self.serverUri}/api/v{version}"),
            "btp": _add_channel_path(f"{self.serverUri}/api/v{version}"),
            "debug": _add_channel_path(f"{self.serverUri}/api/v{version}d"),
        }

        def _make_ws_url(url: str, name: str) -> str:
            url = urlparse(url)
            if url.scheme == 'http':
                scheme = 'ws'
            elif url.scheme == 'https':
                scheme = 'wss'
            else:
                raise URLException('unknown scheme')
            return urlunparse((scheme, url.netloc, f'{url.path}/{name}', '', '', ''))

        if channel:
            self.ws = {
                'block': _make_ws_url(self.rpc['icx'], 'block'),
                'event': _make_ws_url(self.rpc['icx'], 'event'),
                'btp': _make_ws_url(self.rpc['btp'], 'btp'),
            }
        else:
            self.ws = None

    def for_rpc(self, name):
        return self.rpc[name]

    def for_ws(self, name):
        if not self.ws:
            raise Exception("Websocket is not available (missing channel)")
        return self.ws[name]