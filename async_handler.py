import asyncio
from typing import Awaitable
from asyncio import Future, Lock
from __future__ import annotations

class AsyncHandler:
    awaiting_lock: Lock = Lock()
    awaiting: dict[int, Awaitable[str]] = {}

    def __init__(self, send: callable[[int, str], None]):
        self.send = send

    async def on_message(self, msg: str, uid: int) -> None:
        fut: Future
        async with self.awaiting_lock.acquire():
            fut = self.awaiting.pop(uid)

        if (fut != None):
            fut.set_result(msg)
        else:
            self.send("you cannot send a message at this time")

    async def await_msg(self, uid: int) -> Awaitable[str]:
        fut: Future = Future()
        
        async with self.awaiting_lock.acquire():
            self.awaiting[uid] = fut
        
        return fut
