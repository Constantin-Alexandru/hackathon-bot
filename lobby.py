from asyncio import AbstractEventLoop
from dataclasses import dataclass
from typing import Awaitable, Optional

from discord import Embed
from discord.ui import View
from ui_handler import UiHandler
from game import Game


@dataclass
class Lobby:
    id: str
    host_id: tuple[int, int]
    users: dict[int, int]
    ui_handler: Optional[UiHandler]
    game: Game

    def __get_msg_id(self, user_id: int) -> int:
        if self.host_id[0] == user_id:
            return self.host_id[1]

    def start_game(
        self,
        event_loop: AbstractEventLoop,
        _send_mesage: callable[[str, str, Embed, View], Awaitable[None]],
    ):
        self.ui_handler = UiHandler(
            event_loop,
            lambda user_id, embed, view: _send_mesage(
                user_id, self.__get_msg_id(user_id), embed, view
            ),
        )

        players = self.users
        players[self.host_id[0]] = self.host_id[1]

        self.game = Game(players, self.ui_handler)


def create_lobby(lobby_id: str, host_id: int, message_id: int) -> Lobby:
    return Lobby(id=lobby_id, host_id={host_id: message_id}, users=[], ui_handler=None)
