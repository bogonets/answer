#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
VERSION=$(cat "$ROOT_DIR/../VERSION")

ARGS=("--tag" "recc:$VERSION" "--file" "$ROOT_DIR/community.dockerfile")

docker build "${ARGS[@]}" "$ROOT_DIR"
