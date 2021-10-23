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
    local name=$2

    echo "Protocolizing module ${module}/${name} ..."

    "$RECC_DIR/python" -m grpc_tools.protoc \
        -Irecc/proto/${module} \
        --python_out=recc/proto/${module} \
        --mypy_out=recc/proto/${module} \
        --grpc_python_out=recc/proto/${module} \
        recc/proto/${module}/${name}.proto

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

run_proto rpc rpc_api
run_proto daemon daemon_api

