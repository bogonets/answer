# -*- coding: utf-8 -*-

from recc.argparse.config.ctrl_config import CtrlConfig


def ctrl_main(config: CtrlConfig) -> int:
    print(f"ctrl_main: {config.unrecognized_arguments}")
    return 0
