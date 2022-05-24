#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit; pwd)

USAGE="
Usage: $0 [options]

Available options are:
  -h, --help       Print this message.
  -f, --fix        Edit files in place.
  -i, --in-place   Same '--fix' flag.
  --               Stop handling options.
"

FIX_FLAG=0

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

function print_usage
{
    echo "$USAGE"
}

while [[ -n $1 ]]; do
    case $1 in
    -h|--help)
        print_usage
        exit 0
        ;;
    -f|--fix|-i|--in-place)
        FIX_FLAG=1
        shift
        ;;
    --)
        shift
        break
        ;;
    *)
        print_error "Unknown option: $1"
        exit 1
        ;;
    esac
done

ISORT_CHECK_ARGS=()
if [[ $FIX_FLAG -eq 0 ]]; then
    ISORT_CHECK_ARGS[0]="--check"
    ISORT_CHECK_ARGS[1]="--diff"
    ISORT_CHECK_ARGS[2]="--color"
fi

print_message "Run isort ..."

"$RECC_DIR/python" -m isort \
    --settings-path "$CORE_DIR/isort.cfg" \
    ${ISORT_CHECK_ARGS[*]} \
    "$CORE_DIR/recc" \
    "$CORE_DIR/test" \
    "$CORE_DIR/tester"