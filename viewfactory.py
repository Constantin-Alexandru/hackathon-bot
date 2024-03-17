from typing import Awaitable, Callable

import discord
from viewbuilder import ViewBuilder
from discord.ui import View


class ViewFactory:

    def empty() -> View:
        return ViewBuilder().view()

    def start(
        lobby_id: str,
        callback: Callable[[discord.Interaction[discord.Client]], Awaitable[None]],
    ) -> View:
        return ViewBuilder().add_buton("Start", f"start_{lobby_id}", callback).view()
