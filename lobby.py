from dataclasses import dataclass
from utils import create_session_id


@dataclass
class Lobby:
    id: str
    users: list[int]


def create_lobby(user_id: int) -> Lobby:
    return Lobby(create_session_id(), [user_id])
