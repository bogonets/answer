#!/usr/bin/env bash

RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit; pwd)

"$RECC_DIR/python" -m black \
    --check \
    --diff \
    --color \
    --exclude '(.*_pb2(_grpc)?\.py(i)?$|/\.git|/\.venv|/ckps|/configs|/storage)' \
    recc/ \
    test/ \
    tester/
