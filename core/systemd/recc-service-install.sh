#!/usr/bin/env bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)

SERVICE_SOURCE=$SCRIPT_DIR/recc.service
SERVICE_PREFIX=/etc/systemd/system

SERVICE_NAME=recc.service
SERVICE_DESTINATION=$SERVICE_PREFIX/$SERVICE_NAME

if [[ ! -d "$SERVICE_PREFIX" ]]; then
    mkdir -p "$SERVICE_PREFIX"
    echo "Create directory: $SERVICE_PREFIX"
fi

if [[ -f "$SERVICE_DESTINATION" ]]; then
    echo "Exists $SERVICE_DESTINATION file."
    exit 1
fi

cp -v "$SERVICE_SOURCE" "$SERVICE_DESTINATION"

