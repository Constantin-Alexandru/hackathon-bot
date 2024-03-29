from __future__ import annotations
from discord.ui import View, Button
from discord import ButtonStyle


class ViewBuilder:
    def __init__(self) -> ViewBuilder:
        self.view = View()
        return self

    def add_buton(
        self, label: str, style: ButtonStyle, disabled: bool, custom_id: str
    ) -> ViewBuilder:
        button = Button(
            label=label, style=style, disabled=disabled, custom_id=custom_id
        )
        self.view.add_item(button)
        return self
