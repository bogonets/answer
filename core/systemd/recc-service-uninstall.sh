#!/usr/bin/env bash

SERVICE_NAME=recc.service
SERVICE_PREFIX=/etc/systemd/system
SERVICE_PATH=$SERVICE_PREFIX/$SERVICE_NAME

if [[ ! -f "$SERVICE_PATH" ]]; then
    echo "Not exists service file: $SERVICE_PATH"
    exit 1
fi

rm "$SERVICE_PATH"
echo "Remove service file: $SERVICE_PATH"

