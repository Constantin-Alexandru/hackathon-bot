from lobby import create_lobby, Lobby
from command import Command
from commandtype import CommandType


class LobbyManager:
    lobbies: list[Lobby] = []

    @staticmethod
    def __getLobby(session_id) -> Lobby | None:
        for lobby in LobbyManager.lobbies:
            if lobby.id == session_id:
                return lobby

        return None

    @staticmethod
    def create(message_id: int) -> bool:
        lobby = create_lobby(message_id)
        LobbyManager.lobbies.append(lobby)
        return True

    @staticmethod
    def join(message_id, session_id) -> bool:
        return True

    @staticmethod
    def start(session_id) -> bool:
        lobby: Lobby | None = LobbyManager.__getLobby(session_id)

        if not lobby:
            return False

        return True

    @staticmethod
    def leave(message_id, session_id) -> None:
        return True

    @staticmethod
    def process_command(command: Command) -> None:
        match command.command:
            case CommandType.COMMAND_CREATE:
                LobbyManager.create(command.message_id)
            case CommandType.COMMAND_JOIN:
                LobbyManager.join(command.message_id, command.args[0])
            case CommandType.COMMAND_START:
                LobbyManager.start(command.args[0])
