from asyncio import AbstractEventLoop
from typing import Awaitable, Callable

from discord import Embed
from discord.ui import View
from commandtype import CommandType


class Command:
    def __init__(self, command: CommandType, user_id: int) -> None:
        self.command = command
        self.user_id = user_id


class CreateCommand(Command):
    def __init__(self, user_id: int) -> None:
        super().__init__(CommandType.CREATE, user_id)


class JoinCommand(Command):
    def __init__(self, user_id: int, lobby_id: int) -> None:
        super().__init__(CommandType.JOIN, user_id)
        self.lobby_id = lobby_id


class StartCommand(Command):
    def __init__(
        self,
        user_id: int,
        lobby_id: int,
        event_loop: AbstractEventLoop,
        _send_message: Callable[[int, int, Embed, View], Awaitable[None]],
    ) -> None:
        super().__init__(CommandType.START, user_id)
        self.lobby_id = lobby_id
        self.event_loop = event_loop
        self._send_message = _send_message


class GameCommand(Command):
    def __init__(self, user_id: int, lobby_id: str, value: str) -> None:
        super().__init__(CommandType.GAME, user_id)
        self.lobby_id = lobby_id
        self.value = value
