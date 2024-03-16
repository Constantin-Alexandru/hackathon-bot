from typing import Dict, Callable
from lobby import Lobby
from embedfactory import EmbedFactory

callbacks: Dict[str, Callable] = {"start": start}


def start(lobby: Lobby) -> None:
    if len(lobby.users) < 4:
        EmbedFactory().error(
            f"Not enough users. Expected 4. Found {len(lobby.users)}",
            session_id=lobby.id,
        )
    else:
        raise NotImplemented()
