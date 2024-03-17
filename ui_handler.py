from __future__ import annotations
from asyncio import Future, AbstractEventLoop
from typing import Awaitable

from discord import Embed
from discord.ui import View


class UiHandler:
    _event_loop: AbstractEventLoop
    _futures: dict[tuple[str], Future[str]]
    _send_message: callable[[str, Embed, View], Awaitable[None]]

    def __init__(self, event_loop: AbstractEventLoop) -> None:
        self._event_loop = event_loop
        self._futures = {}

    async def send_user_prompt(
        self, user_id: str, message_id: str, discord_embed: Embed, buttons: View
    ) -> str:
        fut = self._event_loop.create_future()
        self._futures[(user_id, message_id)] = fut

        await self._send_message(user_id, discord_embed, buttons)

        return await fut

    def set_user_response(self, user_id: str, message_id: str, value: str) -> None:
        self._futures[(user_id, message_id)].set_result(value)