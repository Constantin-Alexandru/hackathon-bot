from bot import client, send_message
from config import config


def main():
    client.run(config["BOT_KEY"])


if __name__ == "__main__":
    main()
