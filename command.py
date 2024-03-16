from commandtype import CommandType


class Command:
    def __init__(self, command: CommandType, user_id: int, *args: list) -> None:
        self.command = command
        self.user_id = user_id
        self.args = args


def create_command(command: CommandType, user_id: int, *args: list | None) -> Command:
    return Command(command=command, user_id=user_id, args=args)
