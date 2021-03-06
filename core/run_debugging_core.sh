#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit; pwd)

LOCAL_STORAGE_DIR="$CORE_DIR/storage"
SIGNATURE_KEY=aaa

"$RECC_DIR/python" "$CORE_DIR/main.py" -vv -d \
    core \
    --signature "$SIGNATURE_KEY" \
    --local-storage "$LOCAL_STORAGE_DIR" \
    "$@"
