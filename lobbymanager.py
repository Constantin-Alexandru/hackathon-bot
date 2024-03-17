from typing import Awaitable, Callable

from discord import Embed
from discord.ui import View
from lobby import create_lobby, Lobby
from command import Command, CreateCommand, JoinCommand, StartCommand, GameCommand
from embedfactory import EmbedFactory
from utils import random_string
from viewfactory import ViewFactory


class LobbyManager:
    lobbies: list[Lobby] = []
    _send_message: Callable[[int, Embed, View, int], Awaitable[None]]

    @staticmethod
    def set_send_message(
        send_message: Callable[[int, Embed, View, int], Awaitable[None]]
    ) -> None:
        LobbyManager._send_message = send_message

    @staticmethod
    def __get_lobby(session_id) -> Lobby | None:
        for lobby in LobbyManager.lobbies:
            if lobby.id == session_id:
                return lobby

        return None

    @staticmethod
    async def create(command: CreateCommand) -> bool:
        lobby_id = random_string()
        embed = EmbedFactory.waitForStart(lobby_id, 1)
        view = ViewFactory.empty()

        message_id = await LobbyManager._send_message(command.user_id, embed, view)

        if message_id == -1:
            return False

        lobby = create_lobby(lobby_id, command.user_id, message_id)

        LobbyManager.lobbies.append(lobby)
        return True

    @staticmethod
    async def join(command: JoinCommand) -> bool:
        lobby: Lobby | None = LobbyManager.__get_lobby(command.lobby_id)

        if not lobby:
            return False

        if lobby.host_id[0] == command.user_id:
            return False

        view = ViewFactory.empty()

        embed = EmbedFactory.waitForStart(command.lobby_id, len(lobby.users) + 2)

        message_id = await LobbyManager._send_message(command.user_id, embed, view)

        if message_id == -1:
            return False

        lobby.users[command.user_id] = message_id

        for user_id, msg_id in lobby.users.items():
            await LobbyManager._send_message(user_id, embed, view, msg_id)

        if len(lobby.users) > 2:
            view = ViewFactory.start(lobby.id)
            print("REACHED")

        await LobbyManager._send_message(
            lobby.host_id[0], embed, view, lobby.host_id[1]
        )

        return True

    @staticmethod
    async def start(command: StartCommand):
        lobby: Lobby | None = LobbyManager.__get_lobby(command.lobby_id)

        if not lobby:
            return False

        lobby.start_game(command.event_loop, command._send_message)

    @staticmethod
    async def process_command(command: Command) -> None:
        match command:
            case CreateCommand():
                await LobbyManager.create(command)
            case JoinCommand():
                await LobbyManager.join(command)
            case StartCommand():
                await LobbyManager.start(command)
            case GameCommand():
                await LobbyManager.lobbies[command.lobby_id].ui_handler
