#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

BUILDER=html
CACHED_ENVIRONMENT_DIR="$CORE_DIR/build/doc_trees"
SOURCE_DIR="$CORE_DIR/doc"
OUTPUT_DIR="$CORE_DIR/build/$BUILDER"

if [[ ! -d "$CACHED_ENVIRONMENT_DIR" ]]; then
    mkdir -p "$CACHED_ENVIRONMENT_DIR"
fi
if [[ ! -d "$OUTPUT_DIR" ]]; then
    mkdir -p "$OUTPUT_DIR"
fi

"$RECC_DIR/python" -m sphinx \
    -W \
    -b html \
    -d "$CACHED_ENVIRONMENT_DIR" \
    "$SOURCE_DIR" \
    "$OUTPUT_DIR"
