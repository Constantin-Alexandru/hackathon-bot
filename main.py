from bot import create_client
from config import config


def main():
    client = create_client()
    client.run(config["BOT_KEY"])


if __name__ == "__main__":
    main()
