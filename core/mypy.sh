#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit; pwd)

"$RECC_DIR/python" -m mypy \
    --config-file="${CORE_DIR}/mypy.ini" \
    recc/ \
    storage/plugin/ \
    storage/daemon/ \
    test/ \
    tester/
