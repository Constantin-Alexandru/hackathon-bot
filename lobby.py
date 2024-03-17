from dataclasses import dataclass
from typing import Awaitable, Optional

from discord import Embed
from discord.ui import View
from game import Game
from ui_handler import UiHandler


@dataclass
class Lobby:
    id: str
    host_id: tuple[int, int]
    users: dict[int, int]
    ui_handler: Optional[UiHandler]

    def start_game(self, ui_handler: UiHandler):
        self.ui_handler = ui_handler


def create_lobby(lobby_id: str, host_id: int, message_id: int) -> Lobby:
    return Lobby(id=lobby_id, host_id={host_id: message_id}, users=[], ui_handler=None)
