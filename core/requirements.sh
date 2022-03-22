#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit; pwd)
STORAGE_DIR=$CORE_DIR/storage
PIP_CACHE_DIR=$STORAGE_DIR/pip.download

USAGE="
Usage: $0 [options]

Available options are:
  -h, --help       Print this message.
  -d, --download   First 'pip download', then 'pip install'
  -i, --install    Only 'pip install'
  -u, --upgrade    Upgrade the 'requirement.main.txt' file of the package.
  -v, --verbose    Be more verbose/talkative during the operation.
  --               Stop handling options.
"

DOWNLOAD_FLAG=0
INSTALL_FLAG=0
UPGRADE_FLAG=0
VERBOSE_FLAG=0

trap 'cancel_installation' INT

function cancel_installation
{
    local msg="An interrupt signal was detected."
    echo -e "\033[31m$msg\033[0m" 1>&2
    exit 1
}

function print_verbose
{
    if [[ $VERBOSE_FLAG -eq 1 ]]; then
        echo "$@"
    fi
}

function print_message
{
    # shellcheck disable=SC2145
    echo -e "\033[32m$@\033[0m"
}

function print_error
{
    # shellcheck disable=SC2145
    echo -e "\033[31m$@\033[0m" 1>&2
}

function check_dir_or_create
{
    local dir=$1
    if [[ -d "$dir" ]]; then
        print_verbose "Exists directory: $dir"
    else
        print_verbose "Create directory: $dir"
        mkdir -p "$dir"
    fi
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
    -d|--download)
        DOWNLOAD_FLAG=1
        shift
        ;;
    -i|--install)
        INSTALL_FLAG=1
        shift
        ;;
    -u|--upgrade)
        UPGRADE_FLAG=1
        shift
        ;;
    -v|--verbose)
        VERBOSE_FLAG=1
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

function download_and_install
{
    print_message "Run download_and_install"

    check_dir_or_create "$PIP_CACHE_DIR"

    "$RECC_DIR/python" -m pip download --dest "$PIP_CACHE_DIR" pip
    "$RECC_DIR/python" -m pip install --no-index --find-links "$PIP_CACHE_DIR" pip

    for f in "$CORE_DIR"/requirements.*.txt; do
        print_verbose "Current requirements file: '$f'"
        "$RECC_DIR/python" -m pip download --dest "$PIP_CACHE_DIR" -r "$f"
        "$RECC_DIR/python" -m pip install --no-index --find-links "$PIP_CACHE_DIR" -r "$f"
    done
}

function install
{
    print_message "Run install"

    "$RECC_DIR/python" -m pip install pip
    for f in "$CORE_DIR"/requirements.*.txt; do
        print_verbose "Current requirements file: '$f'"
        "$RECC_DIR/python" -m pip install -r "$f"
    done
}

function upgrade
{
    print_message "Upgrade the 'requirement.main.txt' file of the package."

    cp -f \
        "$CORE_DIR/requirements.main.txt" \
        "$CORE_DIR/recc/package/requirements.main.txt"
}

if [[ $DOWNLOAD_FLAG -ne 0 && $INSTALL_FLAG -ne 0 ]]; then
    print_error "The download and install flags cannot coexist."
    exit 1
fi

if [[ $DOWNLOAD_FLAG -ne 0 ]]; then
    download_and_install
elif [[ $INSTALL_FLAG -ne 0 ]]; then
    install
fi

if [[ $UPGRADE_FLAG -ne 0 ]]; then
    upgrade
fi
