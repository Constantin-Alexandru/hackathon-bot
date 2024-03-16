from __future__ import annotations
import random
import string
from typing import Optional
from async_handler import AsyncHandler
from lobby import Lobby
from utils import random_string


class LobbyHandler:
    __closed_lobbys: dict[str, Lobby]
    __open_lobbys: dict[str, tuple[bool, Lobby]]
    __async_handler: AsyncHandler

    def __init__(self):
        self.__closed_lobbys = {}
        self.__open_lobbys = {}        
        self.__async_handler = AsyncHandler()

    def on_message(self, msg: str, uid: int):
        self.__async_handler.on_message(msg, uid)

    def make_lobby(self, host_uid: int, public: bool = True) -> Optional[str]:
        lobby_id: str = random_string(string.ascii_uppercase + string.digits, 5)
        self.__open_lobbys[lobby_id] = (public, Lobby(host_uid))

    def join_lobby_random(self, player_uid: int) -> None:
        for public, lobby in self.__open_lobbys.items():
            if public:
                lobby.add_player(player_uid)
                return
        
        self.make_lobby(player_uid, True)

    def join_lobby_with_code(self, player_uid: int, lobby_code: str) -> None:
        lobby: Lobby = self.__open_private_lobbys.get(lobby_code)
        if lobby != None:
            lobby.add_player(player_uid)

    def close_lobby(self, host_uid: int) -> None:
        for _, lobby in self.__open_lobbys:
            if lobby.get_host_uid() == host_uid:
                return lobby.close_lobby()
    
    def delete_lobby(self, lobby_id: str) -> None:
        for key in self.__closed_lobbys.keys():
            if key == lobby_id:
                self.__closed_lobbys.pop(key)
                return
            
        for key in self.__open_lobbys.keys():
            if key == lobby_id:
                self.__open_lobbys.pop(key)
                return
            
        raise Exception("Cannot find lobby to close")