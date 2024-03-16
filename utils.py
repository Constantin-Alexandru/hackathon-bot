import random

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def create_session_id(length: int = 5) -> str:
    return "".join(
        [characters[random.randint(0, len(characters) - 1)] for i in range(length)]
    )


if __name__ == "__main__":
    for i in range(10):
        print(create_session_id())
