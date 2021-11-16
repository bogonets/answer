#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

STORAGE_DIR=$CORE_DIR/storage
DAEMON_DIR=$STORAGE_DIR/daemon
PLUGIN_DIR=$STORAGE_DIR/plugin

for i in $(find "$DAEMON_DIR" -mindepth 1 -maxdepth 1 -type d); do
    PYTHONPATH="$i:$PYTHONPATH"
done
for i in $(find "$PLUGIN_DIR" -mindepth 1 -maxdepth 1 -type d); do
    PYTHONPATH="$i:$PYTHONPATH"
done

PYTHONPATH="$PYTHONPATH" "$RECC_DIR/python" -m pytest \
     -v \
     --cov \
     --cov-report=term-missing \
     --cov-report=html \
     --cov-config="${CORE_DIR}/pytest.ini" \
     "$@"
