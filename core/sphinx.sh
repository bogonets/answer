#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
OUTPUT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../docs" || exit; pwd)

SOURCE_DIR="$ROOT_DIR/doc"
LOCALE_DIR="$ROOT_DIR/.sphinx_locale"
CACHED_DIR="$ROOT_DIR/.sphinx_cache"
GETTEXT_DIR="$SOURCE_DIR/_gettext"

USAGE_MESSAGE="
Usage: ${BASH_SOURCE[0]} [options] command

Available command are:
  gettext  Run gettext
  intl     Run translate
  html     Run html

Available options are:
  -h, --help Print this message.
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
    "$ROOT_DIR/python" -m sphinx \
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
    "$ROOT_DIR/python" -m sphinx_intl \
        update \
        -p "$GETTEXT_DIR/$language" \
        -d "$LOCALE_DIR" \
        -l "$language"
}

function run_sphinx_html_builder
{
    local language=$1
    "$ROOT_DIR/python" -m sphinx \
        -W \
        -b html \
        -d "$CACHED_DIR/$language" \
        -D "language=$language" \
        "$SOURCE_DIR" \
        "$OUTPUT_DIR/$language"
}

function recc_sphinx_main
{
    while [[ -n $1 ]]; do
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

    local command=${1:-html}
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
