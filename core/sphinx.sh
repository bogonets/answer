#!/usr/bin/env bash

CORE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)

PYTHON_CMD="$RECC_DIR/python"
OUTPUT_DIR="$RECC_DIR/docs"
SOURCE_DIR="$CORE_DIR/doc"
GETTEXT_DIR="$SOURCE_DIR/_gettext"
LOCALE_DIR="$CORE_DIR/.sphinx_locale"
CACHED_DIR="$CORE_DIR/.sphinx_cache"

USAGE_MESSAGE="
Sphinx helper.

  Usage: sphinx.sh [options] [command]

Available options are:
  -h, --help Print this message.

Available command are:
  gettext  Run gettext
  intl     Run translate
  html     Run html
"

if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "Not found source directory: $SOURCE_DIR"
    exit 1
fi
if [[ ! -d "$CACHED_DIR" ]]; then
    echo "Create cached directory: $CACHED_DIR"
    mkdir -p "$CACHED_DIR"
fi
if [[ ! -d "$LOCALE_DIR" ]]; then
    echo "Create locale directory: $LOCALE_DIR"
    mkdir -p "$LOCALE_DIR"
fi
if [[ ! -d "$OUTPUT_DIR" ]]; then
    echo "Create output directory: $OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR"
fi

function run_sphinx_gettext_builder
{
    local language=$1
    "$PYTHON_CMD" -m sphinx \
        -W \
        -b gettext \
        -d "$CACHED_DIR/gettext-$language" \
        -D "language=$language" \
        -D "html_theme=nature" \
        "$SOURCE_DIR" \
        "$GETTEXT_DIR/$language"
}

function run_sphinx_intl
{
    local language=$1
    "$PYTHON_CMD" -m sphinx_intl \
        update \
        -p "$GETTEXT_DIR/$language" \
        -d "$LOCALE_DIR" \
        -l "$language"
}

function run_sphinx_html_builder
{
    local language=$1
    "$PYTHON_CMD" -m sphinx \
        -W \
        -b html \
        -d "$CACHED_DIR/$language" \
        -D "language=$language" \
        "$SOURCE_DIR" \
        "$OUTPUT_DIR/$language"
}

function recc_sphinx_main
{
    while [[ ! -z $1 ]]; do
        case $1 in
        -h|--help)
            echo "$USAGE_MESSAGE"
            return 0
            ;;
        *)
            break
            ;;
        esac
    done

    local command=$1
    if [[ -z $command ]]; then
        echo "Empty command"
        return 1
    fi

    case $command in
    gettext)
        run_sphinx_gettext_builder en
        ;;
    intl)
        run_sphinx_intl en
        ;;
    html)
        run_sphinx_html_builder en
        run_sphinx_html_builder ko
        ;;
    *)
        echo "Unknown command: $command"
        return 1
        ;;
    esac
}

recc_sphinx_main "$@"
