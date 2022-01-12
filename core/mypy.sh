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

if [[ ${#@} -ge 1 ]]; then
    SKIP_STORAGE=1
    if [[ "$1" == "-" ]]; then
        shift
    fi
else
    SKIP_STORAGE=0
fi

print_message "Run core mypy ..."
"$RECC_DIR/python" -m mypy \
    --config-file="${CORE_DIR}/mypy.ini" \
    "$CORE_DIR/recc/" \
    "$CORE_DIR/test/" \
    "$CORE_DIR/tester/" \
    "$@"

function run_mypy
{
    local find_dir=$1
    local dirs=()

    mapfile -t dirs < <(find "$find_dir" -mindepth 1 -maxdepth 1 -type d)

    local file
    for i in ${dirs[*]}; do
        file=$i/mypy.sh
        if [[ -x "$file" ]]; then
            print_message "Run '$file' ..."
            bash "$file"
        fi
    done
}

STORAGE_DIR=$CORE_DIR/storage

if [[ $SKIP_STORAGE -eq 0 ]]; then
    run_mypy "$STORAGE_DIR/daemon"
    run_mypy "$STORAGE_DIR/plugin"
fi
