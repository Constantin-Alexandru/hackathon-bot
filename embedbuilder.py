from __future__ import annotations
from discord import Embed


class EmbedBuilder:
    def __init__(self) -> None:
        self._embed = Embed()

    def colour(self, colour: str) -> EmbedBuilder:
        self._embed.colour = colour
        return self

    def title(self, title: str) -> EmbedBuilder:
        self._embed.title = title
        return self

    def description(self, description: str) -> EmbedBuilder:
        self._embed.description = description
        return self

    def tooltip(self, tooltip: str) -> EmbedBuilder:
        self._embed.description = f"[Info](https://google.com '{tooltip}')"

    def field(
        self, name: str, value: str, at: int | None = None, inline: bool = False
    ) -> EmbedBuilder:
        if at == None:
            self._embed.add_field(name=name, value=value, inline=inline)
        else:
            self._embed.insert_field_at(index=at, name=name, value=value, inline=inline)
        return self

    def footer(self, text: str, icon_url: str = "") -> EmbedBuilder:
        self._embed.set_footer(text=text, icon_url=icon_url)
        return self

    def author(self, name: str, icon_url: str = "") -> EmbedBuilder:
        self._embed.set_author(name=name, url="", icon_url=icon_url)
        return self

    def embed(self) -> Embed:
        return self._embed
