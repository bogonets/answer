#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

PROTOC_VERSION=$("$RECC_DIR/python" -m grpc_tools.protoc --version | sed 's/libprotoc //g')

if [[ -z $PROTOC_VERSION ]]; then
    "$RECC_DIR/python" -m pip install grpcio-tools
fi

function run_proto
{
    local module=$1

    echo "Protocolizing module ${module} ..."

    "$RECC_DIR/python" -m grpc_tools.protoc \
        -Irecc/proto \
        --python_out=recc/proto \
        --mypy_out=recc/proto \
        --grpc_python_out=recc/proto \
        recc/proto/${module}.proto

    # Do not use this flag: `--mypy_grpc_out=recc/proto`
    # I need to generate an asynchronous function, but generating a normal function.

    local pattern_regex="^import ${module}_pb2 as ${module}__pb2$"
    local replace_regex="import recc\\.proto\\.${module}_pb2 as ${module}__pb2"
    local grpc_python_out_path="recc/proto/${module}_pb2_grpc.py"

    sed -i.tmp \
        -e "s/${pattern_regex}/${replace_regex}/" \
        "${grpc_python_out_path}"
    rm "${grpc_python_out_path}.tmp"
}

run_proto api
run_proto daemon
