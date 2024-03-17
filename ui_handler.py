from __future__ import annotations
from asyncio import Future, AbstractEventLoop
from typing import Awaitable

from discord import Embed
from discord.ui import View


class UiHandler:
    _event_loop: AbstractEventLoop
    _futures: dict[int, Future[str]]
    _send_message: callable[[int, Embed, View], Awaitable[None]]

    def __init__(
        self,
        event_loop: AbstractEventLoop,
        _send_message: callable[[int, Embed, View], Awaitable[None]],
    ) -> None:
        self._event_loop = event_loop
        self._futures = {}
        self._send_message = _send_message

    async def send_user_prompt(
        self, user_id: int, discord_embed: Embed, buttons: View
    ) -> str:
        fut = self._event_loop.create_future()
        self._futures[user_id] = fut

        await self._send_message(user_id, discord_embed, buttons)

        return await fut

    def set_user_response(self, user_id: int, value: str) -> None:
        self._futures[user_id].set_result(value)
