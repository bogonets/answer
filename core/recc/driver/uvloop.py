# -*- coding: utf-8 -*-

import asyncio
import warnings


def install_uvloop_driver() -> bool:
    """
    Install uvloop driver.

    .. warning::
        It should not be applied to be installed automatically.
        If you find a driver error, you should use the Python default settings.
    """

    try:
        import uvloop

        # Setup uvloop policy, so that every
        # asyncio.get_event_loop() will create an instance
        # of uvloop event loop.
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        warnings.warn("Not found uvloop module")
        return False
    except BaseException as e:
        warnings.warn(f"uvloop installation failed: {e}")
        return False
    else:
        return True
