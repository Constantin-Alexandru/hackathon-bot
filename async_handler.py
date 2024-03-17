from __future__ import annotations
import asyncio
import time
from typing import Awaitable
from asyncio import Future, Lock, Task


class AsyncHandler:
    __awaiting_lock: Lock
    __awaiting: dict[int, tuple[Awaitable[str], float]]
    __task: Task

    def __init__(self):
        self.__awaiting_lock = Lock()
        self.__awaiting = {}
        self.__task = asyncio.ensure_future(self.check_timeout)

    def __del__(self):
        self.__task.cancel()

    async def on_message(self, msg: str, uid: int) -> None:
        fut: Future
        async with self.__awaiting_lock.acquire():
            (_, fut) = self.__awaiting.pop(uid)
        fut.set_result(msg)

    async def await_msg(self, uid: int, timeout_s: int) -> Awaitable[str]:
        fut: Future = Future()

        async with self.__awaiting_lock.acquire():
            self.__awaiting[uid] = (fut, time.time() + timeout_s)

        return fut

    async def check_timeout(self) -> None:
        while True:
            time_now_s: float = time.time()
            async with self.__awaiting_lock.acquire():
                for tup in self.__awaiting:
                    timeout_s, fut = tup
                    if timeout_s < time_now_s:
                        self.__awaiting.pop(tup)
                        fut.set_exception(Exception("timed out waiting for response"))
            asyncio.sleep(1)
