import time
from typing import TypeVar, Callable


T = TypeVar("T")


def run_until_with_timeout(
    on_iteration_callback: Callable[[], bool],
    on_complete_callback: Callable[[], T] = lambda: None,
    timeout: float = float("infinity"),
    loop_interval: float = 0.1,
    timeout_message: str = "Timeout Exceeded",
) -> T:
    """

    :param on_iteration_callback: A callback that returns bool that is called every loop iteration.
     If True is returned, the loop is complete and on_complete_callback is called.

    :param on_complete_callback: A callback that is called when the loop is completed.
    This function returns the return value of on_complete_callback

    :param timeout: The timeout in seconds for on_iteration_callback to return True,
    on Zero the loop is executed once.

    :param loop_interval: The interval (in seconds) between each loop execution.

    :param timeout_message: The message of the TimeoutError exception.
    raise TimeoutError: When the timeout is exceeded
    """
    if timeout < 0:
        raise ValueError("timeout cannot be smaller than 0")

    start = time.time()
    end = start + timeout

    while True:
        if on_iteration_callback():
            return on_complete_callback()

        time.sleep(loop_interval)

        if time.time() >= end:
            raise TimeoutError(timeout_message)
