from random import choice

import discord

from luna.interface import Adapter
from luna.utils import escape_content
from luna.verb import Verb

__all__ = (
    "SnowflakeAdapter",
    "MemberAdapter",
    "ChannelAdapter",
    "GuildAdapter",
)


class SnowflakeAdapter(Adapter):
    __slots__ = ("object", "_attributes", "_methods")

    def __init__(self, snowflake: discord.abc.Snowflake) -> None:
        self._underlying = snowflake
        created_at = getattr(
            snowflake, "created_at", None
        ) or discord.utils.snowflake_time(snowflake.id)
        self._attributes = {
            "id": snowflake.id,
            "created_at": created_at,
            "timestamp": int(created_at.timestamp()),
            "name": getattr(snowflake, "name", str(snowflake)),
        }
        self._methods = {}
        self.update_attributes()
        self.update_methods()

    def __repr__(self) -> str:
        return f"<{type(self).__qualname__} object={self._underlying!r}>"

    def update_attributes(self) -> None:
        pass

    def update_methods(self) -> None:
        pass

    def get_value(self, verb: Verb) -> str:
        should_escape = False

        if verb.parameter is None:
            return_value = str(self._underlying)
        else:
            try:
                value = self._attributes[verb.parameter]
            except KeyError:
                if method := self._methods.get(verb.parameter):
                    value = method()
                else:
                    return ""

            if isinstance(value, tuple):
                value, should_escape = value

            return_value = str(value)

        return escape_content(return_value) if should_escape else return_value


class MemberAdapter(SnowflakeAdapter):
    _underlying: discord.Member

    def update_attributes(self) -> None:
        avatar_url = self._underlying.display_avatar.url
        joined_at = getattr(self._underlying, "joined_at", self._underlying.created_at)
        additional_attributes = {
            "color": self._underlying.color,
            "colour": self._underlying.color,
            "nick": self._underlying.display_name,
            "avatar": (avatar_url, False),
            "discriminator": self._underlying.discriminator,
            "joined_at": joined_at,
            "joinstamp": int(joined_at.timestamp()),
            "mention": self._underlying.mention,
            "bot": self._underlying.bot,
            "top_role": getattr(self._underlying, "top_role", ""),
        }
        if roleids := getattr(self._underlying, "_roles", None):
            additional_attributes["roleids"] = " ".join(str(r) for r in roleids)
        self._attributes.update(additional_attributes)


class ChannelAdapter(SnowflakeAdapter):
    _underlying: discord.abc.GuildChannel

    def update_attributes(self) -> None:
        if isinstance(self._underlying, discord.TextChannel):
            additional_attributes = {
                "nsfw": self._underlying.nsfw,
                "mention": self._underlying.mention,
                "topic": self._underlying.topic or "",
            }

        else:
            additional_attributes = {
                "nsfw": getattr(self._underlying, "nsfw", False),
                "mention": self._underlying.mention,
            }

        self._attributes.update(additional_attributes)


class GuildAdapter(SnowflakeAdapter):
    _underlying: discord.Guild

    def update_attributes(self) -> None:
        guild = self._underlying
        bots = 0
        humans = 0
        for m in guild.members:
            if m.bot:
                bots += 1
            else:
                humans += 1
        member_count = guild.member_count
        icon_url = getattr(guild.icon, "url", "")
        additional_attributes = {
            "icon": (icon_url, False),
            "member_count": member_count,
            "members": member_count,
            "bots": bots,
            "humans": humans,
            "description": guild.description or "No description.",
        }
        self._attributes.update(additional_attributes)

    def update_methods(self) -> None:
        additional_methods = {"random": self.random_member}
        self._methods.update(additional_methods)

    def random_member(self) -> discord.Member:
        return choice(self._underlying.members)
