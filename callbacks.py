from lobby import Lobby
from embedfactory import EmbedFactory


def start(lobby: Lobby) -> None:
    pass


callbacks: dict[str, callable] = {"start": start}
