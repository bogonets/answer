# -*- coding: utf-8 -*-

import asyncio
import sys


def all_tasks(loop: asyncio.AbstractEventLoop):
    if sys.version_info >= (3, 7):
        return getattr(asyncio, "all_tasks")(loop)  # nocov
    else:
        tasks = asyncio.Task.all_tasks(loop)  # type: ignore[attr-defined]
        return {t for t in list(tasks) if not t.done()}


def cancel_tasks(loop: asyncio.AbstractEventLoop, *tasks) -> None:
    if not tasks:
        return

    for task in tasks:
        task.cancel()

    loop.run_until_complete(asyncio.gather(*tasks, loop=loop, return_exceptions=True))

    for task in tasks:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler(
                {
                    "message": "Unhandled exception during asyncio.run() shutdown",
                    "exception": task.exception(),
                    "task": task,
                }
            )
