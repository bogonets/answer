#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)

SOURCE_DIR="$ROOT_DIR/doc"
OUTPUT_DIR="$ROOT_DIR/docs"
LOCALE_DIR="$ROOT_DIR/.sphinx_locale"
CACHED_DIR="$ROOT_DIR/.sphinx_cache"
GETTEXT_DIR="$SOURCE_DIR/_gettext"
PYTHON_EXE="$ROOT_DIR/python"

USAGE_MESSAGE="
Usage: ${BASH_SOURCE[0]} [options] command

Available command are:
  gettext  Run gettext
  intl     Run translate
  html     Run html
  help     Print help message

Available options are:
  -h, --help Print this message.
"

if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "Not found source directory: $SOURCE_DIR" 1>&2
    exit 1
fi

function make_directory
{
    local dir=$1
    if [[ ! -d "$dir" ]]; then
        mkdir -vp "$dir"
    fi
}

function run_sphinx_gettext_builder
{
    local language=$1
    "$PYTHON_EXE" -m sphinx \
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
    "$PYTHON_EXE" -m sphinx_intl \
        update \
        -p "$GETTEXT_DIR/$language" \
        -d "$LOCALE_DIR" \
        -l "$language"
}

function run_sphinx_html_builder
{
    local language=$1
    "$PYTHON_EXE" -m sphinx \
        -W \
        -b html \
        -d "$CACHED_DIR/$language" \
        -D "language=$language" \
        "$SOURCE_DIR" \
        "$OUTPUT_DIR/$language"
}

function print_usage
{
    echo "$USAGE_MESSAGE"
}

function prepare_directories
{
    make_directory "$LOCALE_DIR"
    make_directory "$OUTPUT_DIR"
    make_directory "$CACHED_DIR"
}

function sphinx_main
{
    while [[ -n $1 ]]; do
        case $1 in
        -h|--help)
            print_usage
            return 0
            ;;
        *)
            break
            ;;
        esac
    done

    local command=$1
    if [[ -z $command ]]; then
        echo "Empty command" 1>&2
        return 1
    fi

    case $command in
    gettext)
        prepare_directories
        run_sphinx_gettext_builder en
        ;;
    intl)
        prepare_directories
        run_sphinx_intl en
        ;;
    html)
        prepare_directories
        run_sphinx_html_builder en
        run_sphinx_html_builder ko
        ;;
    help)
        print_usage
        return 0
        ;;
    *)
        echo "Unknown command: $command" 1>&2
        return 1
        ;;
    esac
}

sphinx_main "$@"
