"""
DisWS (Discord WebSocket ver 0.0.3)

2023-2023

source code: https://github.com/Snaky1/disws
"""


from datetime import datetime
from enum import Enum, auto
from typing import Union


class WebSocketStatus:
    reconnect = 7
    resume = 6
    init = 2


def get_flag(public_flag: int) -> str:
    flags = [
        [1 << 0, "Staff Team"],
        [1 << 1, "Guild Partner"],
        [1 << 2, "HypeSquad Events Member"],
        [1 << 3, "Bug Hunter Level 1"],
        [1 << 5, "Dismissed Nitro promotion"],
        [1 << 6, "House Bravery Member"],
        [1 << 7, "House Brilliance Member"],
        [1 << 8, "House Balance Member"],
        [1 << 9, "Early Nitro Supporter"],
        [1 << 10, "Team User"],
        [1 << 14, "Bug Hunter Level 2"],
        [1 << 16, "Verified Bot"],
        [1 << 17, "Early Verified Bot Developer"],
        [1 << 18, "Moderator Programs Alumni"],
        [1 << 19, "Bot uses only http interactions"],
        [1 << 22, "Active Developer"]
    ]
    flags_all = list()
    for i in range(len(flags)):
        if (public_flag & flags[i][0]) == flags[i][0]:
            flags_all.append(flags[i][1])

    return ', '.join(flags_all)


def get_avatar_url(user_id: int, avatar: str) -> str:
    avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}." \
             f"{'gif' if str(avatar).startswith('a_') else 'png'}" if avatar else None
    return avatar


def get_banner_url(user_id: int, banner: str) -> str:
    banner = f"https://cdn.discordapp.com/banners/{user_id}/{banner}." \
             f"{'gif' if str(banner).startswith('a_') else 'png'}" if banner else None
    return banner


def get_member_create_date(
    user_id: Union[str, int],
    to_string: Union[datetime.strptime, str] = "%d.%m.%Y %H:%M:%S"
) -> Union[str, None]:
    if user_id == -1:
        return

    user_creation = (int(user_id) >> 22) + 1420070400000
    user_creation = datetime.fromtimestamp(user_creation / 1000.0)
    return user_creation.strftime(to_string)


def has_nitro(premium_type: Union[int, None]) -> str:
    return "No nitro" \
        if premium_type == 0 \
        else "Nitro Classic" \
        if premium_type == 1 \
        else "Nitro Boost" if premium_type == 2 else "Nitro Basic"


def from_timestamp_to_humanly(timestamp: int,
                              to_string: Union[datetime.strptime, str] = "%d.%m.%Y %H:%M:%S") -> str:
    return datetime.fromtimestamp(timestamp / 1000.0).strftime(to_string)


def from_iso_format_to_humanly(iso: str, to_string: Union[datetime.strptime, str] = "%d.%m.%Y %H:%M:%S"):
    try:
        date = datetime.fromisoformat(iso)
    except ValueError:
        return iso
    return date.strftime(to_string)


def gen_text(data: dict, status: Enum) -> str:
    text = f"Event: {data['t']}\n"
    data = data['d']

    # presence
    if status.name == EventStatus.PRESENCE_UPDATE.name:
        if 'username' in data['user']:
            avatar_url = "No avatar"
            flags = "No flags"
            if 'public_flags' in data['user']:
                flags = get_flag(data['user']['public_flags'])
            if 'avatar' in data['user'] and data['user']['avatar'] is not None:
                avatar_url = get_avatar_url(user_id=data['user']['id'], avatar=data['user']['avatar'])
            text += f"User:\nname#tag: {data['user']['username']}#" \
                    f"{data['user']['discriminator']}\nPublic flags: {flags}\nAvatar: {avatar_url}"
        text += f"\nID: {data['user']['id']}\nStatus: {data['status']}\n"

        if data['activities']:
            for i, activity in enumerate(data['activities']):
                created_at = from_timestamp_to_humanly(timestamp=activity['created_at'])
                text += f"\nActivity {i}:\n  Type: {activity['type']}\n  Name:" \
                        f" {activity['name']}\n  ID: {activity['id']}\n  Created at: {created_at}\n"
                if 'state' in activity:
                    text += f"  State: {activity['state']}\n"
                if 'details' in activity:
                    text += f"  Details: {activity['details']}\n"
                if 'assets' in activity:
                    if activity['assets']:
                        for small_text, small_image in activity['assets'].items():
                            text += f"  Small Text: {small_text}\n  Small image: {small_image}\n"

        if data['client_status']:
            for _type, status in data['client_status'].items():
                text += f"{_type}: {status}\n"

    return text


class EventStatus(Enum):
    PRESENCE_UPDATE = auto()
    """
    {'t': 'PRESENCE_UPDATE', 's': 60, 'op': 0, 'd': {'user': {'username': '!dуvуatka', 
    'public_flags': 256, 'id': '1070394736503951461', 'display_name': None, 'discriminator': '4308', 
    'avatar_decoration': None, 'avatar': '8a3060276b1a85dd41c283f5cced3d7c'}, 'status': 'offline', 
    'last_modified': 1678550830715, 'client_status': {}, 'activities': []}}
    """
    MESSAGE_CREATE = auto()
    """
    {'t': 'MESSAGE_CREATE', 's': 53, 'op': 0, 'd': {'type': 0, 'tts': False, 'timestamp': 
    '2023-03-11T16:06:58.071000+00:00', 'referenced_message': None, 'pinned': False, 'nonce': 
    '1084145450270851072', 'mentions': [], 'mention_roles': [], 'mention_everyone': False, 
    'member': {'roles': ['877586755488976997', '881826563719585802', '1003551968217796720', 
    '1048643438008074292', '1003551591045021788', '872748260207513630'], 'premium_since': None, 
    'pending': False, 'nick': 'Сяоми', 'mute': False, 'joined_at': '2022-11-28T18:37:03.011000+00:00', 
    'flags': 0, 'deaf': False, 'communication_disabled_until': None, 'avatar': None}, 'id': '1084145451437133944', 
    'flags': 0, 'embeds': [], 'edited_timestamp': None, 'content': 'норм', 'components': [], 'channel_id': 
    '872487083015548940', 'author': {'username': 'Neko Edges', 'public_flags': 256, 'id': '660489620596850731',
     'display_name': None, 'discriminator': '3232', 'avatar_decoration': None, 
     'avatar': '08ed1b5f7274a636a9c9af4ed56c89c0'}, 'attachments': [], 'guild_id': '872487082461888512'}}
Channel: 872487083015548940 | Neko Edges: норм
    """
    CHANNEL_CREATE = auto()
    """
    {'t': 'CHANNEL_CREATE', 's': 35, 'op': 0, 'd': {'version': 1678550785446, 'type': 0, 'topic': None, 
    'rate_limit_per_user': 0, 'position': 1, 'permission_overwrites': [], 'parent_id': '1081981509801619537', 
    'nsfw': False, 'name': 'sss', 'last_message_id': None, 'id': '1084145314572800181', 'hashes': {'version': 1, 
    'roles': {'hash': 'EpAPDQ'}, 'metadata': {'hash': 'XnnQPg'}, 'channels': {'hash': 'iBNOdA'}}, 'guild_id': 
    '1081981509357015112', 'guild_hashes': {'version': 1, 'roles': {'hash': 'EpAPDQ'}, 'metadata': {'hash': 'XnnQPg'}, 
    'channels': {'hash': 'iBNOdA'}}, 'flags': 0}}
    """
    GUILD_AUDIT_LOG_ENTRY_CREATE = auto()
    """
    {'t': 'GUILD_AUDIT_LOG_ENTRY_CREATE', 's': 36, 'op': 0, 'd': {'user_id': '999682446675161148', 'target_id': 
    '1084145314572800181', 'id': '1084145314572800182', 'changes': [{'new_value': 'sss', 'key': 'name'}, 
    {'new_value': 0, 'key': 'type'}, {'new_value': [], 'key': 'permission_overwrites'}, {'new_value': 
    False, 'key': 'nsfw'}, {'new_value': 0, 'key': 'rate_limit_per_user'}, {'new_value': 0, 'key': 'flags'}], 
    'action_type': 10, 'guild_id': '1081981509357015112'}}
    """
    CHANNEL_UPDATE = auto()
    """
    {'t': 'CHANNEL_UPDATE', 's': 43, 'op': 0, 'd': {'version': 1678550804042, 'user_limit': 0, 'type': 2, 
    'rtc_region': None, 'rate_limit_per_user': 0, 'position': 1, 'permission_overwrites': 
    [{'type': 1, 'id': '458276816071950337', 'deny': '0', 'allow': '1068048'}, {'type': 0, 'id': 
    '1005430567770271834', 'deny': '1049601', 'allow': '0'}, {'type': 0, 'id': '874538772761575465', 
    'deny': '2099200', 'allow': '0'}, {'type': 0, 'id': '872487082461888512', 'deny': '1050624', 'allow': '1024'}],
     'parent_id': '949005826549506159', 'nsfw': False, 'name': '📈 Discord: 904 📈', 'last_message_id': None, 'id':
      '902110430510587904', 'hashes': {'version': 1, 'roles': {'hash': 'oakYmg'}, 'metadata': {'hash': 'n/g7vg'}, 
      'channels': {'hash': 'eGOOdQ'}}, 'guild_id': '872487082461888512', 'guild_hashes': {'version': 1, 'roles':
       {'hash': 'oakYmg'}, 'metadata': {'hash': 'n/g7vg'}, 'channels': {'hash': 'eGOOdQ'}}, 'flags': 0, 
       'bitrate': 64000}}
    """
    MESSAGE_UPDATE = auto()
    """
    {'t': 'MESSAGE_UPDATE', 's': 69, 'op': 0, 'd': 
    {'type': 0, 'tts': False, 'timestamp': '2023-03-11T16:07:53.562000+00:00', 
    'pinned': False, 'mentions': [], 'mention_roles': [], 
    'mention_everyone': False, 'id': '1084145684183265290', 
    'flags': 0, 'embeds': [], 'edited_timestamp': '2023-03-11T16:07:57.676185+00:00', 'content': 'ss', 
    'components': [], 'channel_id': '1075066358255059077', 'author': {'username': 'yaku', 'public_flags': 64, 'id': 
    '999682446675161148', 'display_name': None, 'discriminator': '9535', 'avatar_decoration': None, 'avatar': 
    'a_2afdd67101de380215a7acb5de153a25'}, 'attachments': []}}
    """
    SESSIONS_REPLACE = auto()
    """
    {'t': 'SESSIONS_REPLACE', 's': 115, 'op': 0, 'd': [{'status': 'idle', 'session_id': 'all', 'client_info': 
    {'version': 0, 'os': 'unknown', 'client': 'unknown'}, 'activities': [{'type': 4, 'state': 
    'Danil Kulid: Тренер по Бравл Старс 31 мая 2020 года', 'name': 'Custom Status', 'id': 'custom', 
    'created_at': 1678541857008}, {'type': 2, 'timestamps': {'start': 1678550960692, 'end': 1678551174388}, 
    'sync_id': '6AbVJjzv7thIvmMCuhZrmK', 'state': 'Skrillex; Damian Marley', 'session_id': 
    '87a271bdd9cead47567d1c704f89b718', 'party': {'id': 'spotify:999682446675161148'}, 'name': 'Spotify', 
    'id': 'spotify:1', 'flags': 48, 'details': 'Make It Bun Dem', 'created_at': 1678550960951, 'assets': 
    {'large_text': 'Make It Bun Dem', 'large_image': 'spotify:ab67616d0000b273599d75148c77c356edd9ea6f'}}], 
    'active': True}, {'status': 'idle', 'session_id': '87a271bdd9cead47567d1c704f89b718', 'client_info': 
    {'version': 0, 'os': 'windows', 'client': 'desktop'}, 'activities': [{'type': 4, 'state': 'Danil Kulid: 
    Тренер по Бравл Старс 31 мая 2020 года', 'name': 'Custom Status', 'id': 'custom', 'created_at': 1678541857008}, 
    {'type': 2, 'timestamps': {'start': 1678550960692, 'end': 1678551174388}, 'sync_id': '6AbVJjzv7thIvmMCuhZrmK', 
    'state': 'Skrillex; Damian Marley', 'session_id': '87a271bdd9cead47567d1c704f89b718', 'party': {'id': 'spotify:
    999682446675161148'}, 'name': 'Spotify', 'id': 'spotify:1', 'flags': 48, 'details': 'Make It Bun Dem', 'crea
    ted_at': 1678550960951, 'assets': {'large_text': 'Make It Bun Dem', 'large_image': 'spotify:ab67616d0000b2735
    99d75148c77c356edd9ea6f'}}]}, {'status': 'idle', 'session_id': 'c264e8f9fbca8bbf0e1c2d591ea5b1c3', 'client_in
    fo': {'version': 0, 'os': 'other', 'client': 'web'}, 'activities': []}]}
    """
    MESSAGE_REACTION_ADD = auto()
    """
    {'t': 'MESSAGE_REACTION_ADD', 's': 130, 'op': 0, 'd': {'user_id': '660489620596850731', 'message_id': 
    '1083732757441695804', 'member': {'user': {'username': 'Neko Edges', 'public_flags': 256, 'id': '660489
    620596850731', 'display_name': None, 'discriminator': '3232', 'bot': False, 'avatar_decoration': None,
     'avatar': '08ed1b5f7274a636a9c9af4ed56c89c0'}, 'roles': ['877586755488976997', '881826563719585802', '
     1003551968217796720', '1048643438008074292', '1003551591045021788', '872748260207513630'], 'premium_sinc
     e': None, 'pending': False, 'nick': 'Сяоми', 'mute': False, 'joined_at': '2022-11-28T18:37:03.011000+00
     :00', 'flags': 0, 'deaf': False, 'communication_disabled_until': None, 'avatar': None}, 'emoji': {'name':
      '🥰', 'id': None}, 'channel_id': '1058743330441281566', 'burst': False, 'guild_id': '872487082461888512'}}
    """
    MESSAGE_REACTION_REMOVE = auto()
    """
    {'t': 'MESSAGE_REACTION_REMOVE', 's': 9, 'op': 0, 'd': {'user_id': '999682446675161148', 'message_id': 
    '1084149770144202762', 'emoji': {'name': '😎', 'id': None}, 'channel_id': '1075066358255059077', 'burst': False}}
    """
    MESSAGE_ACK = auto()
    """
    {'t': 'MESSAGE_ACK', 's': 286, 'op': 0, 'd': {'version': 28647, 'message_id': '1084147973753151579', 
    'channel_id': '1075066358255059077'}}
    """
    VOICE_STATE_UPDATE = auto()
    """
    {'t': 'VOICE_STATE_UPDATE', 's': 114, 'op': 0, 'd': {'member': {'user': {'username': 'yaku', 'public_flags': 64, 
    'id': '999682446675161148', 'display_name': None, 'discriminator': '9535', 'bot': False, 'avatar_decoration': None, 
    'avatar': 'a_2afdd67101de380215a7acb5de153a25'}, 'roles': ['1083068317352329277'], 'premium_since': '2023-03-10T0
    8:14:27.794000+00:00', 'pending': False, 'nick': None, 'mute': False, 'joined_at': '2023-03-10T08:12:07.711000+00
    :00', 'flags': 0, 'deaf': False, 'communication_disabled_until': None, 'avatar': None}, 'user_id': '9996824466751
    61148', 'suppress': True, 'session_id': '87a271bdd9cead47567d1c704f89b718', 'self_video': False, 'self_mute': Fal
    se, 'self_deaf': False, 'request_to_speak_timestamp': None, 'mute': False, 'guild_id': '1083064214664523878', 'de
    af': False, 'channel_id': '1083461794984644699' or None}}
    """
    CALL_CREATE = auto()
    """
    {'t': 'CALL_CREATE', 's': 155, 'op': 0, 'd': {'voice_states': [], 'ringing': [], 'region': 'bucharest', 
    'message_id': '1084151383323856967', 'embedded_activities': [], 'channel_id': '1075066358255059077'}}
    """
    CALL_UPDATE = auto()
    """
    {'t': 'CALL_UPDATE', 's': 157, 'op': 0, 'd': {'ringing': ['882679655088394260'], 'region': 'bucharest', 
    'message_id': '1084151383323856967', 'guild_id': None, 'channel_id': '1075066358255059077'}}
    """
    CALL_DELETE = auto()
    """
    {'t': 'CALL_DELETE', 's': 160, 'op': 0, 'd': {'channel_id': '1075066358255059077'}}
    """
    TYPING_START = auto()
    """{'t': 'TYPING_START', 's': 237, 'op': 0, 'd': {'user_id': '882679655088394260', 'timestamp': 1678552428, 
    'channel_id': '1075066358255059077'}}"""

# class BaseClient(
#     Application, Guild, Channel, Stage, User, Webhook,
#     Permissions, Intents
# ):
