# -*- coding: utf-8 -*-

from recc.argparse.config.daemon_config import DaemonConfig
from recc.daemon.daemon_servicer import run_daemon_until_complete


def daemon_main(config: DaemonConfig) -> int:
    return run_daemon_until_complete(config)
