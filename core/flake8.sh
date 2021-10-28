#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

"$RECC_DIR/python" -m flake8 \
    --config="${CORE_DIR}/flake8.ini" \
    recc/ \
    storage/plugin/ \
    storage/daemon/ \
    test/
