# -*- coding: utf-8 -*-

import os
import sys

SOURCE_PATH = os.path.abspath(__file__)
SOURCE_DIR = os.path.dirname(SOURCE_PATH)

# Ensure we're in the proper directory whether or not we're being used by pip.
os.chdir(SOURCE_DIR)
sys.path.append(SOURCE_DIR)

from recc.app.entrypoint import main  # noqa


if __name__ == "__main__":
    exit(main())
