"""
DisWS (Discord WebSocket ver 0.0.3)

2023-2023

source code: https://github.com/Snaky1/disws
"""


from .info_types import Member
from .utils import from_iso_format_to_humanly, get_avatar_url, get_flag, get_member_create_date


def gen_guild_member_update_object(data: dict) -> Member:
    username = data['user']['username']
    public_flags = data['user']['public_flags']
    public_flags_converted = get_flag(public_flags)
    discriminator = data['user']['discriminator']
    user_id = data['user']['id']
    avatar = get_avatar_url(user_id, data['user']['avatar'])
    roles = data['roles']
    premium_since = data['premium_since']
    joined_at = from_iso_format_to_humanly(data['joined_at'])
    is_pending_friend = data['is_pending']
    guild_user_avatar = get_avatar_url(user_id, data['avatar']) if data[
        'avatar'] else None
    return Member(
        u_id=user_id,
        username=username,
        discriminator=discriminator,
        full_name=f"{username}#{discriminator}",
        guild_nick=None,
        bot=False,
        created_at=get_member_create_date(user_id),
        public_flags_int=public_flags,
        public_flags_full=public_flags_converted,
        user_guild_avatar=guild_user_avatar,
        is_pending_friend=is_pending_friend,
        joined_at=joined_at,
        roles=roles,
        avatar_url=avatar,
        premium_type=data['premium_type'],
        nitro=data['premium_type'] != 0,
        premium_guild_since=premium_since,
        banner_color=None,
        banner_url=None
    )
