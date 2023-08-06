"""
DisWS (Discord WebSocket ver 0.0.2)

2023-2023

source code: https://github.com/Snaky1/disws
"""


from enum import Enum
from typing import Literal

from aiohttp import ClientResponse, ClientSession, ClientTimeout


class SessionStatus(Enum):
    GET = 1
    DELETE = 2
    POST = 3
    PATCH = 4
    PUT = 5


class BaseRequest:
    BASE_URL = "https://discord.com/"

    def __init__(self, session: ClientSession = None) -> None:
        self.session = session

    async def send_request(
        self, url: str, method: Literal["GET", "DELETE", "POST", "PATCH", "PUT"] = "GET",
        parameters: dict = None, headers: dict = None, files: dict = None
    ) -> ClientResponse:
        payload = {}
        if parameters is not None:
            t_url = url.replace(self.BASE_URL, "")

            data_json = ''

            if method in ['GET', 'DELETE']:
                if parameters:
                    strl = []
                    for key in sorted(parameters):
                        strl.append('{}={}'.format(key, parameters[key]))
                    data_json += '&'.join(strl)
                    t_url += f'?{data_json}'
            else:
                if parameters:
                    data_json = parameters
            try:
                payload: dict = json.dumps(data_json)  # type: ignore
            except (Exception, KeyError):
                print("exception...")
                payload: dict = data_json

            url = f'{self.BASE_URL}{t_url}'
        if headers is None:
            headers = {}
        if files is None:
            files = {}

        if method == SessionStatus.GET.name:
            return await self.session.get(url, headers=headers)
        elif method == SessionStatus.POST.name:
            return await self.session.post(url, data=payload, headers=headers, files=files)  # type: ignore
        elif method == SessionStatus.DELETE.name:
            return await self.session.delete(url, headers=headers)
        # TODO: complete this
        elif method == SessionStatus.PUT.name:
            ...
        elif method == SessionStatus.PATCH.name:
            ...

    async def force_exit(self):
        return await self.session.close()

    async def __aenter__(self):
        if self.session is None or self.session.closed:
            self.session = ClientSession(base_url=self.BASE_URL, timeout=ClientTimeout(10))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
