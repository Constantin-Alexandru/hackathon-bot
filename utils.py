import random
import string


def random_string(
    option_string: str = string.ascii_uppercase + string.digits, length: int = 5
) -> str:
    return "".join(random.choices(option_string, k=length))


if __name__ == "__main__":
    for i in range(10):
        print(random_string())
