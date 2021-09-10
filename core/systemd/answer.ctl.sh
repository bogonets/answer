#!/usr/bin/env bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

SERVICE_NAME=answer
CONFIG_PATH="$CORE_DIR/config.yml"
LOGGING_PATH="$CORE_DIR/logging.yml"
STORAGE_DIR="$CORE_DIR/storage"

USAGE_MESSAGE="
systemctl for answer service.

  Usage: $0 [command] [command-args] ...

Available commands:
  -h, --help    Print this message.
  install       Install service file.
  uninstall     Uninstall service file.
  setup         Daemon reload, enable, start
  enable        Service enable
  disable       Service disable
  reload        Service reload
  status        Service status
  start         Service start
  stop          Service stop
  restart       Service restart
  log           Service journal
"

SERVICE_PREFIX=$HOME/.config/systemd/user
SERVICE_DESTINATION=$SERVICE_PREFIX/answer.service

SERVICE_CONTENT="
[Unit]
Description=ANSWER

[Service]
Environment=RECC_VERBOSE=2
Environment=RECC_DEVELOPER=true
ExecStart=/usr/bin/env \
    /home/zer0/.pyenv/versions/opy-zer0-3.8.9/bin/python \
    -m recc \
    --config \"$CONFIG_PATH\" \
    --log-config \"$LOGGING_PATH\" \
    core \
    --storage-root \"$STORAGE_DIR\"

[Install]
WantedBy=default.target
"

function install_service
{
    if [[ ! -d "$SERVICE_PREFIX" ]]; then
        mkdir -p "$SERVICE_PREFIX"
    fi

    if [[ -f "$service_destination" ]]; then
        echo "Exists $service_destination file."
        exit 1
    fi

    echo "$SERVICE_CONTENT" > "$SERVICE_DESTINATION"
    echo "Create service file: $SERVICE_DESTINATION"
}

function uninstall_service
{
    rm "$SERVICE_DESTINATION"
    echo "Remove service file: $SERVICE_DESTINATION"
}

COMMAND=$1
shift 1
if [[ -z $COMMAND ]]; then
    echo "Empty argument"
    exit 1
fi

case "$COMMAND" in
-h|--help)
    echo "$USAGE_MESSAGE"
    exit 0
    ;;
install)
    install_service
    ;;
uninstall)
    uninstall_service
    ;;
setup)
    systemctl --user daemon-reload
    systemctl --user enable $SERVICE_NAME
    systemctl --user start $SERVICE_NAME
    ;;
enable)
    systemctl --user enable $SERVICE_NAME "$@"
    ;;
disable)
    systemctl --user disable $SERVICE_NAME "$@"
    ;;
reload)
    systemctl --user reload $SERVICE_NAME "$@"
    ;;
status)
    systemctl --user status $SERVICE_NAME "$@"
    ;;
start)
    systemctl --user start $SERVICE_NAME "$@"
    ;;
stop)
    systemctl --user stop $SERVICE_NAME "$@"
    ;;
restart)
    systemctl --user restart $SERVICE_NAME "$@"
    ;;
log)
    journalctl --user -u $SERVICE_NAME "$@"
    ;;
*)
    if [[ -z $1 ]]; then
        echo "Empty argument"
    else
        echo "Unrecognized argument: $1"
    fi
    exit 1
    ;;
esac

