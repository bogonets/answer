# -*- coding: utf-8 -*-

import asyncio
from recc.util.python_version import PY_37


def all_tasks(loop: asyncio.AbstractEventLoop):
    if PY_37:
        return getattr(asyncio, "all_tasks")(loop)
    else:
        return {t for t in list(asyncio.Task.all_tasks(loop)) if not t.done()}


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
