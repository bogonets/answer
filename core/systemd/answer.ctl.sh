#!/usr/bin/env bash

if [[ $(id -u) -eq 0 ]]; then
    echo 'Please do not run as root.'
    exit 1
fi

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

SERVICE_NAME=answer
LOGGING_PATH="$CORE_DIR/logging.yml"
STORAGE_DIR="$CORE_DIR/storage"

OPY_EXECUTABLE=$(opy -c 'import sys; print(sys.executable)')
PYTHON_EXECUTABLE=$OPY_EXECUTABLE

SERVICE_PREFIX_FOR_USER=$HOME/.config/systemd/user
SERVICE_PREFIX_FOR_ROOT=/etc/systemd/system/

DEFAULT_OPT_FOR_USER="--user"
DEFAULT_OPT_FOR_ROOT=""

SERVICE_PREFIX=SERVICE_PREFIX_FOR_ROOT
SERVICE_DESTINATION=$SERVICE_PREFIX/answer.service
SERVICE_OPT=$DEFAULT_OPT_FOR_ROOT

CURRENT_USER=$USER
CURRENT_GROUP=$(id -Gn | awk '{print $1}')

USAGE_MESSAGE="
systemctl for answer service.

  Usage: $0 [command] [command-args] ...

Available commands:
  help          Print this message.
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

SERVICE_CONTENT="
[Unit]
Description=The ANSWER, No-code development platform

[Service]
Environment=RECC_VERBOSE=2
Environment=RECC_DEVELOPER=true
Environment=PYTHONPATH=\"$CORE_DIR\"
ExecStart=\"$PYTHON_EXECUTABLE\" -m recc core --storage-root \"$STORAGE_DIR\"
User=$CURRENT_USER
Group=$CURRENT_GROUP

[Install]
WantedBy=multi-user.target
"

function install_service
{
    if [[ ! -d "$SERVICE_PREFIX" ]]; then
        sudo mkdir -p "$SERVICE_PREFIX"
    fi

    if [[ -f "$service_destination" ]]; then
        echo "Exists $service_destination file."
        exit 1
    fi

    sudo echo "$SERVICE_CONTENT" > "$SERVICE_DESTINATION"
    echo "Create service file: $SERVICE_DESTINATION"
}

function uninstall_service
{
    if [[ -f "$SERVICE_DESTINATION" ]]; then
        sudo rm "$SERVICE_DESTINATION"
        echo "Remove service file: $SERVICE_DESTINATION"
    else
        echo "Not exists service file: $SERVICE_DESTINATION"
    fi
}

COMMAND=$1
shift 1
if [[ -z $COMMAND ]]; then
    echo "Empty argument"
    echo "$USAGE_MESSAGE"
    exit 1
fi

case "$COMMAND" in
help|--help|-h)
    echo "$USAGE_MESSAGE"
    exit 0
    ;;
install)
    install_service
    ;;
uninstall)
    uninstall_service
    ;;
up)
    install_service
    sudo systemctl $SERVICE_OPT daemon-reload
    sudo systemctl $SERVICE_OPT enable $SERVICE_NAME
    sudo systemctl $SERVICE_OPT start $SERVICE_NAME
    ;;
down)
    uninstall_service
    sudo systemctl $SERVICE_OPT stop $SERVICE_NAME
    sudo systemctl $SERVICE_OPT disable $SERVICE_NAME
    sudo systemctl $SERVICE_OPT daemon-reload
    ;;
enable)
    systemctl $SERVICE_OPT enable $SERVICE_NAME "$@"
    ;;
disable)
    systemctl $SERVICE_OPT disable $SERVICE_NAME "$@"
    ;;
reload)
    systemctl $SERVICE_OPT reload $SERVICE_NAME "$@"
    ;;
status)
    systemctl $SERVICE_OPT status $SERVICE_NAME "$@"
    ;;
start)
    systemctl $SERVICE_OPT start $SERVICE_NAME "$@"
    ;;
stop)
    systemctl $SERVICE_OPT stop $SERVICE_NAME "$@"
    ;;
restart)
    systemctl $SERVICE_OPT restart $SERVICE_NAME "$@"
    ;;
log)
    journalctl $SERVICE_OPT -u $SERVICE_NAME "$@"
    ;;
*)
    echo "Unrecognized argument: $1"
    echo "$USAGE_MESSAGE"
    exit 1
    ;;
esac
