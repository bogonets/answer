#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit; pwd)

"$RECC_DIR/python" -m pip install --upgrade pip

for f in "$CORE_DIR"/requirements.*.txt; do
    "$RECC_DIR/python" -m pip install -r "$f"
done
