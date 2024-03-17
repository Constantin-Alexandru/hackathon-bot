from dataclasses import dataclass
from game import Game


@dataclass
class Lobby:
    id: str
    host_id: tuple[int, int]
    users: dict[int, int]
    game: Game | None


def create_lobby(lobby_id: str, host_id: int, message_id: int) -> Lobby:
    return Lobby(id=lobby_id, host_id={host_id: message_id}, users=[], game=None)
