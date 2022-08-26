#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
PROTOC_VERSION=$("$ROOT_DIR/python" -m grpc_tools.protoc --version | sed "s/libprotoc //g")

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

function run_proto
{
    local module=$1
    local name=$2
    local args=(
        "-Irecc/proto/${module}"
        "--python_out=recc/proto/${module}"
        "--mypy_out=recc/proto/${module}"
        "--grpc_python_out=recc/proto/${module}"
        "recc/proto/${module}/${name}.proto"
    )

    print_message "grpc_tools.protoc ${args[*]}"

    "$ROOT_DIR/python" -m grpc_tools.protoc "${args[@]}"

    # Do not use this flag: `--mypy_grpc_out=recc/proto`
    # I need to generate an asynchronous function, but generating a normal function.

    local pattern_regex="^import ${name}_pb2 as "
    local replace_regex="import recc\\.proto\\.${module}\\.${name}_pb2 as "
    local grpc_python_out_path="recc/proto/${module}/${name}_pb2_grpc.py"

    sed -i.tmp \
        -e "s/${pattern_regex}/${replace_regex}/" \
        "${grpc_python_out_path}"
    rm "${grpc_python_out_path}.tmp"
}

if [[ -z $PROTOC_VERSION ]]; then
    "$ROOT_DIR/python" -m pip install grpcio-tools
fi

run_proto rpc rpc_api
