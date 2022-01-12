#!/usr/bin/env bash

USAGE_MESSAGE="
UnitTest manager.

  Usage: test.sh [options] args

Available options are:
  -h, --help        Print this message.
  -i {num}, --iterator={name}
                    Number of repetitions. (default: 1)
"

RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit; pwd)
ITERATOR=1

while [[ ! -z $1 ]]; do
    case $1 in
    -h|--help)
        echo "$USAGE_MESSAGE"
        return 0
        ;;
    -i|--iterator)
        ITERATOR=${2}
        shift 2
        ;;
    *)
        break
        ;;
    esac
done

for (( i=0; i<$ITERATOR; i++ )); do
    echo "Test iteration: $i/$ITERATOR"
    "$RECC_DIR/python" -m pytest "$@"
    code=$?
    if [[ $code -ne 0 ]]; then
        echo "Test error: $i/$ITERATOR"
        exit 1
    fi
done

