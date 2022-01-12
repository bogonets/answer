#!/usr/bin/env bash

RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit; pwd)

"$RECC_DIR/python" -m twine upload dist/*
