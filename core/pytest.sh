#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

"$RECC_DIR/python" -m pytest \
    -v \
    --cov \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-config="${CORE_DIR}/pytest.ini"
