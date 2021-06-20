#!/usr/bin/env bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)

BUILDER=html
SOURCE_DIR="$SCRIPT_DIR"
OUTPUT_DIR="$SCRIPT_DIR/docs"

if [[ ! -d "$OUTPUT_DIR" ]]; then
    mkdir -p "$OUTPUT_DIR"
fi

python -m sphinx \
    -W \
    -b $BUILDER \
    "$SOURCE_DIR" \
    "$OUTPUT_DIR"
