from typing import Any, Awaitable, Callable
import discord


class CallbackButton(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        label: str | None = None,
        disabled: bool = False,
        custom_id: str | None = None,
        url: str | None = None,
        emoji: str | discord.Emoji | discord.PartialEmoji | None = None,
        row: int | None = None,
        callback: Callable[
            [discord.Interaction[discord.Client]], Awaitable[None]
        ] = None
    ):
        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row,
        )
        self._callback = callback

    async def callback(self, interaction: discord.Interaction[discord.Client]) -> Any:
        if self._callback is not None:
            await self._callback(interaction)

        return await super().callback(interaction)
