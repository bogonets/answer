#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

STORAGE_DIR="$CORE_DIR/storage"
SIGNATURE_KEY=aaa

"$RECC_DIR/python" "$CORE_DIR/main.py" -vv -d \
    core \
    --signature "$SIGNATURE_KEY" \
    --storage-root "$STORAGE_DIR" \
    "$@"
