"""
DisWS (Discord WebSocket ver 0.0.3)

2023-2023

source code: https://github.com/Snaky1/disws
"""


import json
from typing import Any, Coroutine, Union

from aiohttp import ClientError, ClientResponse, ClientSession, http_exceptions
from multidict import CIMultiDict

from disws.base.user import DiscordUser
from disws.utils.info_types import Member, Message, MessageCache


class BaseClient(DiscordUser):
    BASE_URL = 'https://discord.com/api/v9'
    TIMEOUT = 10
    headers = {
        'content-type': 'application/json',
        'user-agent': 'python-discord-client'
    }

    def __init__(self, token: str, api_version: int = None) -> None:
        # super().__init__(token)
        super().__init__()
        self._token = token
        if api_version is not None:
            self.BASE_URL = f'https://discord.com/api/v{api_version}'

        self.session = ClientSession()
        self.headers['Authorization'] = self._token

        self._callbacks = {
            'on_event': [self.on_event],
            'on_guild_member_update': [self.on_guild_member_update],
            'on_message_create': [self.on_message_create],
            'on_message_delete': [self.on_message_delete]
        }
        self.message_cache = MessageCache()

    @staticmethod
    async def _check_response(response: ClientResponse) -> dict:
        if f'{response.status}'[0] == '2':
            try:
                data = await response.json()
            except ValueError:
                raise Exception(response.content)
            else:
                return data
        else:
            raise Exception(f'{response.status}: {await response.text()}')

    async def _request(
        self, method: str,
        params: dict = dict,
        uri: str = '', headers: dict = dict,
        **kwargs
    ) -> dict:
        data_json = ''
        response = None

        if method in ['GET', 'DELETE']:
            if params:
                strl = []
                for key in sorted(params):
                    strl.append('{}={}'.format(key, params[key]))
                data_json += '&'.join(strl)
                uri += f'?{data_json}'
        else:
            if params:
                data_json = params

        try:
            payload = json.dumps(data_json)
        except (BaseException, Exception):
            payload = data_json

        url = f'{self.BASE_URL}{uri}'
        try:
            async with ClientSession(headers=self.headers) as session:
                if method == 'GET':
                    response = await session.request(method=method, url=url, headers=headers, timeout=self.TIMEOUT,
                                                     **kwargs)
                elif method == 'DELETE':
                    response = await session.request(method=method, url=url, headers=headers, timeout=self.TIMEOUT,
                                                     **kwargs)
                elif method == 'POST':
                    response = await session.request(method=method, url=url, data=payload, headers=headers,
                                                     timeout=self.TIMEOUT, **kwargs)
                elif method == 'PATCH':
                    response = await session.request(method=method, url=url, data=payload, headers=headers,
                                                     timeout=self.TIMEOUT, **kwargs)
                elif method == 'PUT':
                    response = await session.request(method=method, url=url, data=payload, headers=headers,
                                                     timeout=self.TIMEOUT, **kwargs)
        except (ClientError, http_exceptions.HttpProcessingError):
            pass
        except (BaseException, Exception):
            # logger.exception('Non-aiohttp exception occured:  %s', getattr(e, '__dict__', {}))
            raise
        else:
            if response is not None:
                return await self._check_response(response)
            else:
                print('!')

    def _send_file_attachment(
        self, method: str,
        uri: str,
        file_names: [str],
        payload=None
    ) -> Coroutine[Any, Any, dict]:
        if payload is None:
            payload = {}

        self.session.headers.update(CIMultiDict({'content-type': None}))
        headers = {'content-disposition': 'form-data; name="payload_json"'}
        payload: dict = {'payload_json': json.dumps(payload)}
        prepared_files: dict = {}
        for i, filename in enumerate(file_names):
            file_type = filename.split('.')[-1]
            media_type = None
            if file_type in ['jpg', 'png', 'jpeg', 'gif']:
                media_type = 'image'
                if file_type == 'svg':
                    file_type = 'svg+xml'

            prepared_files[f'files[{i}]'] = (
                filename, open(filename, 'rb'), f'{media_type}/{file_type}', {
                    'Content-Disposition': f'form-data; name="files[{i}]"; filename="{filename}"'
                })

        for key in prepared_files:
            payload[key] = prepared_files[key]

        response = self._request(method, params=payload, files=prepared_files, headers=headers, uri=uri)
        self.session.headers.update(CIMultiDict({'content-type': 'application/json'}))
        return response

    async def on(self, event_name: str, callback):
        if event_name not in self._callbacks:
            self._callbacks[event_name] = [callback]
        else:
            self._callbacks[event_name].append(callback)

    async def trigger(self, event_name: str, event_object):
        if event_name in self._callbacks:
            for callback in self._callbacks[event_name]:
                await callback(event_object)

    async def on_event(self, event) -> None:
        pass

    async def on_guild_member_update(self, event) -> 'Member':
        return event

    async def on_message_create(self, event) -> 'Message':
        return event

    @staticmethod
    async def on_message_delete(self, event: Union['Message', dict]) -> Union['Message', dict]:
        return event
