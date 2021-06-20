#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

"$RECC_DIR/python" setup.py bdist_wheel

# Remove all '*.c' files.
find "$RECC_DIR/recc" -name "*.c" | xargs rm
