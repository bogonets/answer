#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit; pwd)

STORAGE_DIR="$CORE_DIR/storage"
DAEMON_ADDRESS=0.0.0.0:19999

DAEMON_PLUGIN_NAME=$1

if [[ -z $DAEMON_PLUGIN_NAME ]]; then
    echo "Empty daemon plugin name."
    exit 1
fi

"$RECC_DIR/python" "$CORE_DIR/main.py" -vv -d \
    daemon \
    --daemon-address "$DAEMON_ADDRESS" \
    --daemon-module "$DAEMON_PLUGIN_NAME"
