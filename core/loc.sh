#!/usr/bin/env bash

find . -name '*.py' \
    | grep -E '\./(recc|test|tester)/' \
    | xargs wc -l \
    | tail -1 \
    | awk '{print($1)}'
