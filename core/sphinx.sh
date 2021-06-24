#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

BUILDER=html
SOURCE_DIR="$CORE_DIR/doc"
OUTPUT_DIR="$RECC_DIR/docs"

GETTEXT_DIR="$SOURCE_DIR/_gettext"
LOCALE_DIR="$SOURCE_DIR/_locale"
BUILD_DIR="$SOURCE_DIR/.build"
CACHED_DIR="$BUILD_DIR/doc_trees"

if [[ ! -d "$CACHED_DIR" ]]; then
    mkdir -p "$CACHED_DIR"
fi
if [[ ! -d "$OUTPUT_DIR" ]]; then
    mkdir -p "$OUTPUT_DIR"
fi

nature
function run_sphinx
{
    local language=$1

    "$RECC_DIR/python" -m sphinx_intl \
        update \
        -p "$GETTEXT_DIR/$language" \
        -d "$LOCALE_DIR" \
        -l "$language"

    "$RECC_DIR/python" -m sphinx \
        -W \
        -b "$BUILDER" \
        -d "$CACHED_DIR/$language" \
        -D "language=$language" \
        "$SOURCE_DIR" \
        "$OUTPUT_DIR/$language"
}

run_sphinx en
run_sphinx ko
