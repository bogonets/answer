#!/usr/bin/env bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
WORKING_DIR=$SCRIPT_DIR
DOCKERFILE_PATH=$SCRIPT_DIR/recc-node-python-3.8.9.dockerfile
IMAGE_NAME=osom8979/recc-node
IMAGE_TAG=python-3.8.9
TAG_NAME=$IMAGE_NAME:$IMAGE_TAG
TAG_LATEST=$IMAGE_NAME:latest

USAGE_MESSAGE="
Build recc-node docker image.

  Usage: recc-node-build.sh [options]

Available options are:
  -p, --push    Push an image to a registry.
  -l, --latest  Add 'latest' tag.
  -n, --dry-run Don’t actually do anything, just show what would be done.
  -h, --help    Print this message.
"

function exit_on_error
{
    local code=$?
    if [[ $code -ne 0 ]]; then
        exit $code
    fi
}

function run_command
{
    local dry_run=$1
    shift

    if [[ $dry_run -eq 1 ]]; then
        echo "$@"
    else
        "$@"
    fi

    exit_on_error
}

function recc_node_build_main
{
    local src="$OPM_HOME/INFORMATION"
    local enable_push=0
    local add_latest=0
    local dry_run=0

    while [[ ! -z $1 ]]; do
        case $1 in
        -h|--help)
            echo "$USAGE_MESSAGE"
            return 0
            ;;
        -p|--push)
            enable_push=1
            shift
            ;;
        -n|--dry-run)
            dry_run=1
            shift
            ;;
        -l|--latest)
            add_latest=1
            shift
            ;;
        *)
            break
            ;;
        esac
    done

    local build_commands=("--file" "$DOCKERFILE_PATH" "-t" "$TAG_NAME")
    if [[ $add_latest -eq 1 ]]; then
        build_commands+=("-t" "$TAG_LATEST")
    fi
    build_commands+=("$WORKING_DIR")

    run_command $dry_run docker build ${build_commands[*]}
    if [[ $enable_push -eq 0 ]]; then
        return 0
    fi

    run_command $dry_run docker push $TAG_NAME
    if [[ $add_latest -eq 0 ]]; then
        return 0
    fi

    run_command $dry_run docker push $TAG_LATEST
}

recc_node_build_main "$@"

