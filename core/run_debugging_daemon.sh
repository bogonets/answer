#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

STORAGE_DIR="$CORE_DIR/storage"
DAEMON_ADDRESS=0.0.0.0:19999

DAEMON_PLUGIN_NAME=$1

if [[ -z $DAEMON_PLUGIN_NAME ]]; then
    echo "Empty daemon plugin name."
    exit 1
fi

DAEMON_PLUGIN_DIR="$STORAGE_DIR/daemon/$DAEMON_PLUGIN_NAME"
DAEMON_PLUGIN_SCRIPT_PATH="$DAEMON_PLUGIN_DIR/$DAEMON_PLUGIN_NAME.py"
DAEMON_VENV_DIR="$DAEMON_PLUGIN_DIR/.venv"
DAEMON_SITE_PACKAGES_DIR="$DAEMON_VENV_DIR/lib/python3.8/site-packages"

if [[ ! -f "$DAEMON_PLUGIN_SCRIPT_PATH" ]]; then
    echo "Not exists plugin file: $DAEMON_PLUGIN_SCRIPT_PATH"
    exit 1
fi

"$RECC_DIR/python" "$CORE_DIR/main.py" -vv -d \
    daemon \
    --daemon-address "$DAEMON_ADDRESS" \
    --daemon-file "$DAEMON_PLUGIN_SCRIPT_PATH" \
    --daemon-packages-dir "$DAEMON_SITE_PACKAGES_DIR"
