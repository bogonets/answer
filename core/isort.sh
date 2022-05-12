#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit; pwd)

function print_error
{
    # shellcheck disable=SC2145
    echo -e "\033[31m$@\033[0m" 1>&2
}

function print_message
{
    # shellcheck disable=SC2145
    echo -e "\033[32m$@\033[0m"
}

trap 'cancel_black' INT

function cancel_black
{
    print_error "An interrupt signal was detected."
    exit 1
}

print_message "Run isort ..."

"$RECC_DIR/python" -m isort \
    --settings-path "$CORE_DIR/isort.cfg" \
    --check \
    --diff \
    --color \
    "$CORE_DIR/recc" \
    "$CORE_DIR/test" \
    "$CORE_DIR/tester"
