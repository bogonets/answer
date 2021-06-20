# -*- coding: utf-8 -*-

from recc.argparse.config.core_config import CoreConfig
from recc.http.http_app import HttpAppCallback, HttpApp
from recc.core.context import Context


def core_main(
    config: CoreConfig,
    http_callback: HttpAppCallback = None,
) -> int:
    application = HttpApp(
        context=Context(config),
        callback=http_callback,
    )
    application.run_until_complete()
    return 0
