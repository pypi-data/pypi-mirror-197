"""
DisWS (Discord WebSocket ver 0.0.3)

2023-2023

source code: https://github.com/Snaky1/disws
"""


from datetime import datetime
from typing import Union

from disws.utils.utils import (from_iso_format_to_humanly, get_avatar_url, get_banner_url, get_flag,
                               get_member_create_date, has_nitro)


class MessageCache:
    messages: dict[int, dict] = {}

    def __init__(self) -> None:
        pass

    def add_message(self, message_id: Union[int, str], message: Union[dict, 'Message']) -> dict:
        self.messages[message_id] = message
        return self.messages[message_id]

    def get_message(self, message_id: int) -> dict:
        return self.messages[message_id] if message_id in self.messages else None

    def mark_message_as_deleted(
        self, message_id: int, convert_to_json: bool = False
    ) -> Union[dict, 'Message', None]:
        result: Union[dict, 'Message', None] = self.messages.pop(message_id, None)
        if convert_to_json:
            result = result.to_json()
        return result

    def mark_message_as_edited(self, message_id: int) -> dict:
        self.messages[message_id]['edited_at'] = datetime.now()
        return self.messages[message_id]


class Member:
    id: Union[str, int, None]
    username: str
    discriminator: Union[str, int]
    full_name: str
    guild_nick: Union[str, None]
    bot: bool
    created_at: Union[datetime, str, None]
    public_flags_int: int
    public_flags_full: str
    avatar_url: Union[str, None]
    user_guild_avatar: Union[str, None]
    banner_url: Union[str, None]
    banner_color: Union[str, hex, None]
    has_nitro: bool
    premium_type: Union[str, None]
    premium_guild_since: Union[datetime, str, None]
    joined_at: Union[datetime, str, None]
    is_pending_friend: bool
    roles: Union[list, str, None]

    def __init__(
        self, u_id: Union[str, int, None], username: str,
        discriminator: Union[str, int],
        full_name: str,
        guild_nick: Union[str, None],
        bot: bool,
        created_at: Union[datetime, str, None],
        public_flags_int: int,
        public_flags_full: str,
        avatar_url: Union[str, None],
        user_guild_avatar: Union[str, None],
        banner_url: Union[str, None],
        banner_color: Union[str, hex, None],
        nitro: bool,
        premium_type: Union[str, None],
        premium_guild_since: Union[datetime, str, None],
        joined_at: Union[datetime, str, None],
        is_pending_friend: bool = False,
        roles: Union[list, str, None] = None
    ) -> None:
        self.id = u_id
        self.username = username
        self.discriminator = discriminator
        self.full_name = full_name
        self.guild_nick = guild_nick
        self.bot = bot
        self.created_at = created_at
        self.public_flags_int = public_flags_int
        self.public_flags_full = public_flags_full
        self.avatar_url = avatar_url
        self.user_guild_avatar = user_guild_avatar
        self.banner_url = banner_url
        self.banner_color = banner_color
        self.has_nitro = nitro
        self.premium_type = premium_type
        self.premium_guild_since = premium_guild_since
        self.joined_at = joined_at
        self.is_pending_friend = is_pending_friend
        self.roles = roles

    def __repr__(self) -> str:
        return f"<user={self.full_name!r}, id={self.id}, public_flags={self.public_flags_int}>"

    def __str__(self) -> str:
        return self.full_name

    def to_json(self) -> dict:
        print(self.created_at)
        return {
            'id': self.id,
            'username': self.username,
            'discriminator': self.discriminator,
            'full_name': self.full_name,
            'nick': self.guild_nick if self.guild_nick is not None else None,
            'bot': self.bot,
            'created_at': from_iso_format_to_humanly(self.created_at),
            'public_flags_int': self.public_flags_int,
            'public_flags_full': self.public_flags_full,
            'avatar_url': self.avatar_url,
            'user_guild_avatar': self.user_guild_avatar if self.user_guild_avatar is not None else None,
            'banner_url': self.banner_url,
            'banner_color': self.banner_color,
            'has_nitro': self.has_nitro,
            'premium_type': self.premium_type,
            'joined_at': from_iso_format_to_humanly(self.joined_at) if self.joined_at is not None else None,
            'is_pending_friend': self.is_pending_friend,
            'roles': self.roles if self.roles is not None else None
        }

    @staticmethod
    def to_member(data: dict) -> 'Member':
        """Converts dictionary with user data to User class"""
        joined_at = None
        if 'guild_id' in data:
            if 'member' in data and data['member']['joined_at'] is not None:
                joined_at = from_iso_format_to_humanly(data['member']['joined_at'])
            elif 'joined_at' in data and data['joined_at'] is not None:
                joined_at = from_iso_format_to_humanly(data['joined_at'])
        public_flags_converted = get_flag(
            data['user']['public_flags']
            if 'user' in data and 'public_flags' in data['user']
            else data['public_flags']) if 'public_flags' in data else "No flags"
        print(data)
        created_at = None
        if 'user' in data or 'author' in data:
            created_at = get_member_create_date(
                data['user']['id']
                if 'user' in data else data['author']['id'] if 'author' in data else -1
            )
        nitro_type = None
        if 'premium_type' in data:
            if 'user' in data:
                nitro_type = has_nitro(premium_type=data['user']['premium_type'])
            else:
                nitro_type = has_nitro(premium_type=data['premium_type'])

        avatar = None

        if 'user' in data and 'avatar' in data['user']:
            if data['user']['avatar'] is not None and data['user']['avatar'].startswith(
                    "https://cdn.discordapp.com/avatars/"):
                avatar = data['user']['avatar']
            else:
                avatar = get_avatar_url(
                    data['user']['id'] if 'user' in data else data['id'],
                    data['user']['avatar'] if 'user' in data else data['avatar']
                )

        elif 'author' in data and 'avatar' in data['author']:
            if data['author']['avatar'] is not None \
                    and data['author']['avatar'].startswith("https://cdn.discordapp.com/avatars/"):
                avatar = data['author']['avatar']
            else:
                avatar = get_avatar_url(
                    data['user']['id'] if 'user' in data else data['id'],
                    data['user']['avatar'] if 'user' in data else data['avatar']
                )

        banner = None
        if 'user' in data:
            if 'banner' in data['user']:
                banner = get_banner_url(data['user']['id'], data['user']['banner'])
            else:
                pass
        elif 'banner' in data:
            banner = get_banner_url(data['id'], data['banner'])

        print(data)
        return Member(
            u_id=data['user']['id'] if 'user' in data else data['id'] if 'id' in data else None,
            username=data['user']['username']
            if 'user' in data else data['username'] if 'username' in data else data['nick'] if 'nick' in data else None,
            discriminator=data['user']['discriminator']
            if 'user' in data else data['discriminator'] if 'discriminator' in data else None,
            full_name=f"{data['user']['username']}#{data['user']['discriminator']}"
            if 'user' in data else f"{data['username']}#{data['discriminator']}"
            if 'username' in data and 'discriminator' in data else None,
            guild_nick=data['nick'] if 'nick' in data else None,
            bot=data['author']['bot']
            if 'author' in data and 'bot' in data
            else data['user']['bot']
            if 'user' in data and 'bot' in data else False,
            created_at=created_at,
            public_flags_int=data['user']['public_flags']
            if 'user' in data else data['public_flags'] if 'public_flags' in data else 0,
            public_flags_full=public_flags_converted,
            avatar_url=avatar,
            user_guild_avatar=data['avatar'],
            banner_url=banner,
            banner_color=data['banner_color'] if 'banner_color' in data else None,
            nitro=data['premium_type'] != 0 if 'premium_type' in data else False,
            premium_type=nitro_type,
            premium_guild_since=data['premium_since'] if 'premium_since' in data else None,
            joined_at=joined_at,
            roles=data['roles'] if 'roles' in data and data['roles'] is not None else None
        )


class User:
    id: str
    username: str
    email: Union[str, None]
    bio: str
    locale: Union[str, None]
    nsfw_allowed: bool
    mfa: bool
    phone: Union[str, None]
    discriminator: Union[str, int]
    full_name: str
    created_at: Union[datetime, str, None]
    public_flags_int: int
    public_flags_full: str
    avatar_url: Union[str, None]
    banner_url: Union[str, None]
    banner_color: Union[str, hex, None]
    has_nitro: bool
    premium_type: Union[str, None]

    def __init__(
        self, u_id: str, username: str,
        email: Union[str, None],
        bio: str,
        locale: Union[str, None],
        nsfw_allowed: bool,
        mfa: bool,
        phone: Union[str, None],
        discriminator: Union[str, int],
        full_name: str,
        created_at: Union[datetime, str, None],
        public_flags_int: int,
        public_flags_full: str,
        avatar_url: Union[str, None],
        banner_url: Union[str, None],
        banner_color: Union[str, hex, None],
        nitro: bool,
        premium_type: Union[str, None],
    ) -> None:
        self.id = u_id
        self.username = username
        self.email = email
        self.bio = bio
        self.locale = locale
        self.nsfw_allowed = nsfw_allowed
        self.mfa = mfa
        self.phone = phone
        self.discriminator = discriminator
        self.full_name = full_name
        self.created_at = created_at
        self.public_flags_int = public_flags_int
        self.public_flags_full = public_flags_full
        self.avatar_url = avatar_url
        self.banner_url = banner_url
        self.banner_color = banner_color
        self.has_nitro = nitro
        self.premium_type = premium_type

    def __repr__(self):
        return f"<user={self.full_name!r}, id={self.id}, public_flags={self.public_flags_int}>"

    # def __str__(self) -> str:
    #     return self.full_name

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'bio': self.bio,
            'locale': self.locale,
            'nsfw_allowed': self.nsfw_allowed,
            'mfa': self.mfa,
            'phone': self.phone,
            'discriminator': self.discriminator,
            'full_name': self.full_name,
            'created_at': self.created_at,
            'public_flags_int': self.public_flags_int,
            'public_flags_full': self.public_flags_full,
            'avatar_url': self.avatar_url,
            'banner_url': self.banner_url,
            'banner_color': self.banner_color,
            'has_nitro': self.has_nitro,
            'premium_type': self.premium_type
        }

    @staticmethod
    def to_user(data: dict) -> 'User':
        """Converts dictionary with user data to User class"""
        public_flags_converted = get_flag(data['public_flags'])
        created_at = get_member_create_date(data['id'])
        nitro_type = has_nitro(premium_type=data['premium_type'])
        avatar = get_avatar_url(data['id'], data['avatar'])
        banner = get_banner_url(data['id'], data['banner'])

        return User(
            u_id=data['id'],
            username=data['username'],
            email=data['email'],
            bio=data['bio'],
            locale=data['locale'],
            nsfw_allowed=data['nsfw_allowed'],
            mfa=data['mfa_enabled'],
            phone=data['phone'],
            discriminator=data['discriminator'],
            full_name=f"{data['username']}#{data['discriminator']}",
            created_at=created_at,
            public_flags_int=data['public_flags'],
            public_flags_full=public_flags_converted,
            avatar_url=avatar,
            banner_url=banner,
            banner_color=data['banner_color'],
            nitro=data['premium_type'] != 0,
            premium_type=nitro_type
        )


class Message:
    id: str
    timestamp: Union[datetime.timestamp, str]
    pinned: bool
    tts: bool
    referenced_message: Union[..., None]
    mentions: list[Union[Member, None]]
    mention_roles: list
    mention_everyone: bool
    member: Member
    embeds: list
    edited_timestamp: Union[datetime.timestamp, str, None]
    content: str
    components: list
    attachments: list
    channel_id: Union[str, int]
    author: Member
    guild_id: Union[str, int]

    def __init__(
        self, msg_id: str, timestamp: Union[datetime.timestamp, str],
        pinned: bool, tts: bool, referenced_message: Union[..., None],
        mentions: list, mention_roles: list, mention_everyone: bool,
        member: Member, embeds: list, edited_timestamp: Union[datetime.timestamp, str, None],
        content: str, components: list, attachments: list, channel_id: Union[str, int],
        author: Member, guild_id: Union[str, int]
    ):
        self.id = msg_id
        self.timestamp = timestamp
        self.pinned = pinned
        self.tts = tts
        self.referenced_message = referenced_message
        self.mentions = mentions
        self.mention_roles = mention_roles
        self.mention_everyone = mention_everyone
        self.member = member
        self.embeds = embeds
        self.edited_timestamp = edited_timestamp
        self.content = content
        self.components = components
        self.attachments = attachments
        self.channel_id = channel_id
        self.author = author
        self.guild_id = guild_id

    def __repr__(self):
        return f"<message={self.content!r}, id={self.id}>, attachments={len(self.attachments)}"

    def to_json(self) -> dict:
        # if data is not None:
        #
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'pinned': self.pinned,
            'tts': self.tts,
            'referenced_message': self.referenced_message,
            'mentions': self.mentions,
            'mention_roles': self.mention_roles,
            'mention_everyone': self.mention_everyone,
            'member': self.member.to_json() if self.member is not None else None,
            'embeds': self.embeds,
            'edited_timestamp': self.edited_timestamp,
            'content': self.content if self.content is not None else '',
            'components': self.components,
            'attachments': self.attachments,
            'channel_id': self.channel_id,
            'author': self.author.to_json(),
            'guild_id': self.guild_id
        }

    @staticmethod
    def to_message(data: dict) -> 'Message':
        """Converts dictionary with message data to Message class"""
        mentions = []
        for mention in data['mentions']:
            mentions.append(Member.to_member(mention))

        return Message(
            msg_id=data['id'],
            timestamp=from_iso_format_to_humanly(data['timestamp']),
            pinned=data['pinned'],
            tts=data['tts'],
            referenced_message=data['referenced_message'] if 'referenced_message' in data else None,
            mentions=mentions,
            mention_roles=data['mention_roles'] if 'mention_roles' in data else None,
            mention_everyone=data['mention_everyone'] if 'mention_everyone' in data else False,
            member=Member.to_member(data['member']) if 'member' in data and data['member'] is not None else None,
            embeds=data['embeds'] if 'embeds' in data else None,
            edited_timestamp=from_iso_format_to_humanly(data['edited_timestamp'])
            if data['edited_timestamp'] is not None else None,
            content=data['content'],
            components=data['components'] if 'components' in data else None,
            attachments=data['attachments'] if 'attachments' in data else None,
            channel_id=data['channel_id'] if 'channel_id' in data else None,
            author=Member.to_member(data['author']),
            guild_id=data['guild_id'] if 'guild_id' in data else None,
        )


class DeletedMessage:
    id: str
    timestamp: Union[datetime.timestamp, str]
    channel_id: Union[str, int]
    guild_id: Union[str, int]

    def __init__(self, msg_id: str, timestamp: Union[datetime.timestamp, str], channel_id: Union[str, int],
                 guild_id: Union[str, int], cache: MessageCache):
        self.id = msg_id
        self.timestamp = timestamp
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.messages: MessageCache = cache

    def __repr__(self):
        return f"id={self.id}>"

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'channel_id': self.channel_id,
            'guild_id': self.guild_id
        }

    def to_deleted_message(self, data: dict) -> 'DeletedMessage':
        cache_message = self.messages.get_message(data['id'])
        print(cache_message)
        return DeletedMessage(
            msg_id=data['id'],
            timestamp=from_iso_format_to_humanly(data['timestamp']),
            channel_id=data['channel_id'],
            guild_id=data['guild_id']
        )
