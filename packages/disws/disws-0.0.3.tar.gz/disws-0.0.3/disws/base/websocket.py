"""
DisWS (Discord WebSocket ver 0.0.3)

2023-2023

source code: https://github.com/Snaky1/disws
"""


import asyncio
import json
import time
from traceback import format_exc
from typing import Union

import websockets

# from base.intents import Intents
from disws.base.client import BaseClient
from disws.utils.info_types import Member, Message
from disws.utils.logger import log
from disws.utils.utils import WebSocketStatus


# from utils.converters import gen_guild_member_update_object


class WebSocketAPI(BaseClient):
    last_ping_time: int = 0
    heartbeat_interval = 41250 / 1000
    sequence: Union[int, None] = None

    # def __init__(self, token: str, intents: list = Intents.get_intents_list(), api_num: int = 10):
    def __init__(self, token: str, api_num: int = 10):
        super().__init__(token)
        self._api_url = f"wss://gateway.discord.gg/?v={api_num}&encoding=json"
        self.token = token
        self._conn = None
        # self.intents = Intents()
        # self._intents = self.intents.get_intents(intents)
        self.ws: websockets = None
        self.wait = True

    def _get_ping_timeout(self) -> float:
        return self.heartbeat_interval

    def _gen_payload(self, op_code):
        return {
            'op': op_code,
            'd': {
                'token': self.token,
                'properties': {
                    '$os': "linux",
                    '$browser': 'disco',
                    '$device': 'pc'
                },
                'compress': True
            }
        }

    def run(self) -> None:
        log.info("Running Discord Client...")
        self._conn = asyncio.ensure_future(self.connect())

    async def _connect(self) -> None:
        log.info("Connecting to WebSocket...")
        await self.send_message(self._gen_payload(WebSocketStatus.init))

    async def _close(self) -> None:
        log.info("Closing...")
        await self.ws.close()

    async def _reconnect(self, wait: bool = True) -> None:
        log.info("Reconnecting...")
        await self._close()
        self.wait = wait
        self.run()

    async def _send_ping(self):
        start = int(time.time())
        await self.send_message({
            'op': 1,
            'd': self.sequence
        })
        self.last_ping_time = int(time.time())
        log.info(f"WS ping: {self.last_ping_time - start}")

    async def connect(self) -> None:
        try:
            print("try...")
            async with websockets.connect(self._api_url) as session:
                self.ws = session
                await self._connect()
                log.warning("Connected")

                try:
                    while self.wait:
                        if not self.last_ping_time or int(time.time()) - self.last_ping_time > self._get_ping_timeout():
                            await self._send_ping()
                        try:
                            evt = await asyncio.wait_for(self.ws.recv(), timeout=self._get_ping_timeout())
                        except asyncio.TimeoutError:
                            await self._send_ping()
                        except asyncio.CancelledError:
                            await self.ws.ping()
                        else:
                            try:
                                evt_obj = json.loads(evt)
                                if evt_obj['op'] != 11 and 's' in evt_obj and evt_obj['s']:
                                    self.sequence = evt_obj['s']
                                    if evt_obj['op'] == 10:
                                        self.heartbeat_interval = int(evt_obj['d']['heartbeat_interval']) / 1000
                            except ValueError:
                                pass
                            else:
                                if evt_obj['t'] == "GUILD_MEMBER_UPDATE":
                                    result = Member.to_member(evt_obj['d'])
                                    await self.trigger('on_guild_member_update', result)
                                if evt_obj['t'] == "MESSAGE_CREATE":
                                    result = Message.to_message(evt_obj['d'])
                                    self.message_cache.add_message(evt_obj['d']['id'], result)
                                    await self.trigger("on_message_create", result)
                                if evt_obj['t'] == "MESSAGE_DELETE":
                                    result = self.message_cache.mark_message_as_deleted(
                                        evt_obj['d']['id'], convert_to_json=False
                                    )
                                    await self.trigger("on_message_delete", result)
                                else:
                                    await self.trigger('on_event', evt_obj)

                except websockets.ConnectionClosed as e:
                    log.fatal(f"Error: {e} {format_exc()}")
                    await self._reconnect(wait=True)
                except (BaseException, Exception) as e:
                    log.fatal(f"Error: {e} {format_exc()}")
                    await self._reconnect(wait=True)
        except (Exception, BaseException) as e:
            log.fatal(f"Error: {e} {format_exc()}")
            await asyncio.sleep(2)
            await self._reconnect(wait=True)

    async def send_message(self, message: dict) -> None:
        await self.ws.send(json.dumps(message))
