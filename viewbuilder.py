from __future__ import annotations
from typing import Awaitable, Callable
import discord
from discord.ui import View, Button
from discord import ButtonStyle, Interaction

from callbackbutton import CallbackButton


class ViewBuilder:
    def __init__(self) -> None:
        self._view = View()

    def add_buton(
        self,
        label: str,
        custom_id: str,
        callback: Callable[[discord.Interaction[discord.Client]], Awaitable[None]],
        style: ButtonStyle = ButtonStyle.primary,
        disabled: bool = False,
    ) -> ViewBuilder:
        button = CallbackButton(
            label=label,
            style=style,
            disabled=disabled,
            custom_id=custom_id,
            callback=callback,
        )
        self._view.add_item(button)
        return self

    def view(self) -> View:
        return self._view
