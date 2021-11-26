#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

"$RECC_DIR/python" -m black \
    --check \
    --diff \
    --color \
    --exclude '(.*_pb2(_grpc)?\.py(i)?$|/\.git|/\.venv|/ckps|/configs)' \
    recc/ \
    storage/plugin/ \
    storage/daemon/ \
    test/ \
    tester/
