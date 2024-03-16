import random
import string

def random_string(option_string: str = string.ascii_letters, length: int = 10) -> str:
    return random.choices(option_string, k=length)


if __name__ == "__main__":
    for i in range(10):
        print(create_session_id())
