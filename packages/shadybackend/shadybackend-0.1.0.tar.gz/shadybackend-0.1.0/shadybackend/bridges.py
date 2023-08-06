"""
A central module to look up the available backends.
"""

from dataclasses import dataclass
from typing import Callable, Dict
import discord
from typing import Any, Dict
from shadybackend.request_tools import Request
from json import loads
import logging as log

BRIDGES: Dict[str, Any] = dict()


class DiscordBridge():
    """
    This is just the example code from:
    https://discordpy.readthedocs.io/en/stable/quickstart.html
    """

    name = "discord"

    def build_bridge(self, g: Dict[str, Any]) -> None:
        intents = discord.Intents.default()
        intents.message_content = True

        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            log.info(f'Started Discord Bridge {client.user}')

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            try:
                rjson = loads(message.content)
                tmp = Request(rjson["api_call"], rjson["data"])
                log.info(f"Received hook data: {tmp}")
                g["Q"].appendleft(tmp)
            except Exception as e:
                err = e
                log.error(f"Failed to pass message to API: {e}")
        client.run(g["discord_token"])


BRIDGES["discord"] = DiscordBridge
