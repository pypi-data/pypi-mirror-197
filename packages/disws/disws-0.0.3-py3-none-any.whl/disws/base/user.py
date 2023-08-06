"""
DisWS (Discord WebSocket ver 0.0.3)

2023-2023

source code: https://github.com/Snaky1/disws
"""


from disws.base.api_base import BaseRequest
from disws.utils.info_types import User


class DiscordUser(object):
    def __init__(self):
        super().__init__()
        self.request = BaseRequest()

    async def get_me(self) -> User:
        async with self.request:
            json = await self.request.send_request(
                "/api/v10/users/@me", method="GET", headers=self.headers
            )
            if json.status == 200:
                r_json = await json.json()

        return User.to_user(r_json)

    # TODO: complete this
    # async def get_user(self, user_id: int) -> dict:
    #     async with self.request:
    #         json = await self.request.send_request(f"/api/v10/users/{user_id}", method="GET", headers=self.headers)
