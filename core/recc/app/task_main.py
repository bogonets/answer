# -*- coding: utf-8 -*-

from recc.argparse.config.task_config import TaskConfig
from recc.rpc.task_server import run_task_until_complete


def task_main(config: TaskConfig) -> int:
    return run_task_until_complete(config)
