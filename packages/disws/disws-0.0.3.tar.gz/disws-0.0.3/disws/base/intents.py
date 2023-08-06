"""
DisWS (Discord WebSocket ver 0.0.3)

2023-2023

source code: https://github.com/Snaky1/disws
"""

# class Intents(object):
#     # https://discord.com/developers/docs/topics/gateway#gateway-intents
#     _intents = [
#         'GUILDS', 'GUILD_MEMBERS', 'GUILD_BANS', 'GUILD_EMOJIS_AND_STICKERS', 'GUILD_INTEGRATIONS', 'GUILD_WEBHOOKS',
#         'GUILD_INVITES', 'GUILD_VOICE_STATES', 'GUILD_PRESENCES', 'GUILD_MESSAGES', 'GUILD_MESSAGE_REACTIONS',
#         'GUILD_MESSAGE_TYPING', 'DIRECT_MESSAGES', 'DIRECT_MESSAGE_REACTIONS', 'GUILD_SCHEDULED_EVENTS',
#         'GUILD_SCHEDULED_EVENTS'
#     ]
#
#     @classmethod
#     def get_intents_list(cls) -> [str]:
#         return cls._intents
#
#     def get_intent(self, intent_name: str = '') -> int:
#         for i, role in enumerate(self._intents):
#             if role == intent_name:
#                 return 1 << i
#         raise ValueError(f'Intent {intent_name} not found!')
#
#     def get_intents(self, intents_list: [str]) -> int:
#         return sum([self.get_intent(intent) for intent in intents_list])
