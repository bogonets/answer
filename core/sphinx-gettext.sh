#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

SOURCE_DIR="$CORE_DIR/doc"
OUTPUT_DIR="$SOURCE_DIR/_gettext"

BUILD_DIR="$SOURCE_DIR/.build"
CACHED_DIR="$BUILD_DIR/doc_trees"

if [[ ! -d "$CACHED_DIR" ]]; then
    mkdir -p "$CACHED_DIR"
fi

"$RECC_DIR/python" -m sphinx \
    -W \
    -b gettext \
    -d "$CACHED_DIR/$language" \
    -D "html_theme=nature" \
    "$SOURCE_DIR" \
    "$OUTPUT_DIR"
