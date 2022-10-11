#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
VERSION=$(cat "$ROOT_DIR/../VERSION")

PREFIX=bogonets/recc
TAG=$PREFIX:$VERSION
LATEST=$PREFIX:latest
ARGS=("--tag" "$TAG" "--file" "$ROOT_DIR/community.dockerfile")

docker build "${ARGS[@]}" "$ROOT_DIR"
docker tag "$TAG" "$LATEST"

read -r -p "push image? (y/n) " YN
if [[ "${YN,,}" == 'y' ]]; then
    docker push "$TAG"
    docker push "$LATEST"
fi
