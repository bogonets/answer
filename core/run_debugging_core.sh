#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

"$RECC_DIR/python" "$CORE_DIR/main.py" -v -d core -k aaa

