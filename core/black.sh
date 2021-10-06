#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

"$RECC_DIR/python" -m black \
    --check \
    --diff \
    --color \
    --exclude '/(recc\/proto)/' \
    recc/ \
    storage/plugin/ \
    test/
