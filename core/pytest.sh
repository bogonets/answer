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

print_message "Run core pytest ..."
"$RECC_DIR/python" -m pytest \
     -v \
     --cov \
     --cov-report=term-missing \
     --cov-report=html \
     --cov-config="${CORE_DIR}/pytest.ini" \
     "$CORE_DIR/test/" \
     "$@"

function run_pytest
{
    local find_dir=$1
    local dirs=()

    mapfile -t dirs < <(find "$find_dir" -mindepth 1 -maxdepth 1 -type d)

    local file
    for i in ${dirs[*]}; do
        file=$i/pytest.sh
        if [[ -x "$file" ]]; then
            print_message "Run '$file' ..."
            PYTHONPATH="$i:$PYTHONPATH" bash "$file"
        fi
    done
}

STORAGE_DIR=$CORE_DIR/storage

if [[ $SKIP_STORAGE -eq 0 ]]; then
    run_pytest "$STORAGE_DIR/daemon"
    run_pytest "$STORAGE_DIR/plugin"
fi
