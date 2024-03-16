from commandtype import CommandType


class Command:
    def __init__(self, command: CommandType, user_id: int) -> None:
        self.command = command
        self.message_id = user_id


class JoinCommand(Command):
    def __init__(self, user_id: int, lobby_id: int) -> None:
        super().__init__(CommandType.JOIN, user_id)
        self.lobby_id = lobby_id
