import asyncio
import threading
from typing import TypeVar, Coroutine, Any

from qm.singleton import Singleton


class EventLoopThread(metaclass=Singleton):
    def __init__(self) -> None:
        self.loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self.loop.run_forever)
        self._thread.daemon = True
        self._thread.start()

    def stop(self) -> None:
        self.loop.stop()
        self._thread.join()


T = TypeVar("T")


def create_future(coroutine: Coroutine[Any, Any, T]) -> asyncio.Future:  # In 3.9 future is generic: asyncio.Future[T]
    return asyncio.run_coroutine_threadsafe(coroutine, loop=EventLoopThread().loop)


def run_async(coroutine: Coroutine[Any, Any, T]) -> T:
    return create_future(coroutine).result()
