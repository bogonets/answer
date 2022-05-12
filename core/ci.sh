#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
ERROR_COUNT=0

trap "on_interrupt" SIGHUP SIGINT SIGTERM

function on_interrupt
{
    echo "[CI] Caught an interrupt !!"
    exit 1
}

function ci_runner
{
    local name=$1
    echo "[CI:${name}] running ..."

    "${CORE_DIR}/${name}.sh"

    local code=$?
    echo "[CI:${name}] done(${code})"
    if [[ $code -ne 0 ]]; then
        (( ERROR_COUNT++ ))
    fi
}

for cursor in isort black flake8 mypy sphinx pytest; do
    ci_runner $cursor
done

if [[ $ERROR_COUNT -eq 0 ]]; then
    echo "Everything was successful."
    exit 0
else
    echo "$ERROR_COUNT jobs failed."
    exit 1
fi
