#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)

SIGNATURE=aaa
LOCAL_STORAGE="$HOME/answer"

"$ROOT_DIR/python" "$ROOT_DIR/main.py" -vv -d \
    core \
    --signature "$SIGNATURE" \
    --local-storage "$LOCAL_STORAGE" \
    "$@"
