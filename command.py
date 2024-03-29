from commandtype import CommandType


class Command:
    def __init__(self, command: CommandType, message_id: int, *args: list) -> None:
        self.command = command
        self.message_id = message_id
        self.args = args


def create_command(
    command: CommandType, message_id: int, *args: list | None
) -> Command:
    return Command(command=command, message_id=message_id, args=args)
