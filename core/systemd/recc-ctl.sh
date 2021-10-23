#!/usr/bin/env bash

SERVICE_NAME=recc.service
SERVICE_OPT=

USAGE_MESSAGE="
systemctl for answer service.

  Usage: $0 [command] [command-args] ...

Available commands:
  help          Print this message.
  reload        Daemon reload
  up            Daemon reload, enable, start
  down          Daemon stop, disable, reload
  enable        Service enable
  disable       Service disable
  reload        Service reload
  status        Service status
  start         Service start
  stop          Service stop
  restart       Service restart
  log           Service journal
"

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
reload)
    systemctl $SERVICE_OPT daemon-reload
up)
    systemctl $SERVICE_OPT daemon-reload
    systemctl $SERVICE_OPT enable $SERVICE_NAME
    systemctl $SERVICE_OPT start $SERVICE_NAME
    ;;
down)
    systemctl $SERVICE_OPT stop $SERVICE_NAME
    systemctl $SERVICE_OPT disable $SERVICE_NAME
    systemctl $SERVICE_OPT daemon-reload
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

