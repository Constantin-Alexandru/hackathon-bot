from __future__ import annotations
from discord import Embed


class EmbedBuilder:
    def __init__(self) -> EmbedBuilder:
        self.embed = Embed()
        return self

    def colour(self, colour: str) -> EmbedBuilder:
        self.embed.colour = colour
        return self

    def title(self, title: str) -> EmbedBuilder:
        self.embed.title = title
        return self

    def description(self, description: str) -> EmbedBuilder:
        self.embed.description = description
        return self

    def field(
        self, name: str, value: str, at: int | None = None, inline: bool = False
    ) -> EmbedBuilder:
        if at == None:
            self.embed.add_field(name, value, inline)
        else:
            self.embed.insert_field_at(at, name, value, inline)
        return self

    def footer(self, text: str, icon_url: str) -> EmbedBuilder:
        self.embed.set_footer(text, icon_url)
        return self

    def author(self, name: str, icon_url: str) -> EmbedBuilder:
        self.embed.set_author(name, "", icon_url)
        return self

    def embed(self) -> Embed:
        return self.embed
