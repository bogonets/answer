#!/usr/bin/env bash

RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit; pwd)

"$RECC_DIR/python" setup.py bdist_wheel

# Remove all '*.c' files.
# find "$RECC_DIR/recc" -name "*.c" | xargs rm
