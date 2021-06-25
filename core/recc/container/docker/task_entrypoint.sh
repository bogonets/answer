#!/usr/bin/env bash

PYTHON_CMD="$(which python3 2> /dev/null)"

function print_recc_envs
{
    env | grep "^RECC_.*"
}

function print_recc_version
{
    "$PYTHON_CMD" -m recc --version 2> /dev/null
}

function install_recc
{
    local install_version=$1

    if [[ -n "$install_version" ]]; then
        "$PYTHON_CMD" -m pip install "recc==$install_version"
    else
        "$PYTHON_CMD" -m pip install -U recc
    fi
}

function uninstall_recc
{
    "$PYTHON_CMD" -m pip uninstall -y recc
}

function assert_env
{
    local var_name=$1
    if [[ -z "${!var_name}" ]]; then
        echo "Undefined $var_name env" 1>&2
        exit 1
    fi
}

function assert_required_envs
{
    assert_env RECC_ENTRYPOINT_MINIMUM_REQUIRED_VERSION
    assert_env RECC_ENTRYPOINT_PYTHON_PACKAGE_DIR
}

function assert_minimum_version_number
{
    local prefix=$1
    local number=$2
    local min_number=$3

    if [[ $number -lt $min_number ]]; then
        echo "$prefix version mismatch" 1>&2
        echo " - Actually: $number" 1>&2
        echo " - Minimum: $min_number" 1>&2
        exit 1
    fi
}

function assert_minimum_version
{
    local version=$1
    local min_version=$2

    local version_tuple
    local min_version_tuple
    version_tuple=("${version//./ }")
    min_version_tuple=("${min_version//./ }")

    assert_minimum_version_number "Major" "${version_tuple[0]}" "${min_version_tuple[0]}"
    assert_minimum_version_number "Minor" "${version_tuple[1]}" "${min_version_tuple[1]}"
    assert_minimum_version_number "Patch" "${version_tuple[2]}" "${min_version_tuple[2]}"
}

function run_task_main
{
    if [[ $RECC_VERBOSE -ge 1 ]]; then
        print_recc_envs
    fi

    assert_required_envs

    local min_version
    min_version=$RECC_ENTRYPOINT_MINIMUM_REQUIRED_VERSION

    local recc_version
    recc_version=$(print_recc_version)

    if [[ -z $recc_version ]]; then
        echo "Install 'recc' module ..."
        install_recc "$min_version"
        recc_version=$(print_recc_version)
    fi

    if [[ -z $recc_version ]]; then
        PYTHONPATH="$RECC_ENTRYPOINT_PYTHON_PACKAGE_DIR:$PYTHONPATH"
        export PYTHONPATH
        recc_version=$(print_recc_version)
    fi

    if [[ -z $recc_version ]]; then
        echo "Not found 'recc' module." 1>&2
        exit 1
    fi

    assert_minimum_version "$recc_version" "$min_version"

    "$PYTHON_CMD" -m recc task
}

run_task_main
