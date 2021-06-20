#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

PROTOC_VERSION=$("$RECC_DIR/python" -m grpc_tools.protoc --version | sed 's/libprotoc //g')

if [[ -z $PROTOC_VERSION ]]; then
    "$RECC_DIR/python" -m pip install grpcio-tools
fi

"$RECC_DIR/python" -m grpc_tools.protoc \
    -Irecc/proto \
    --python_out=recc/proto \
    --mypy_out=recc/proto \
    --grpc_python_out=recc/proto \
    recc/proto/api.proto

# Do not use this flag: `--mypy_grpc_out=recc/proto`
# I need to generate an asynchronous function, but generating a normal function.

PATTERN_REGEX='^import api_pb2 as api__pb2$'
REPLACE_REGEX='import recc\.proto\.api_pb2 as api__pb2'
GRPC_PYTHON_OUT_PATH=recc/proto/api_pb2_grpc.py

sed -i.tmp \
    -e "s/${PATTERN_REGEX}/${REPLACE_REGEX}/" \
    "${GRPC_PYTHON_OUT_PATH}"
rm "${GRPC_PYTHON_OUT_PATH}.tmp"

