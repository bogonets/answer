#!/usr/bin/env bash

find . -name "*.py" | egrep '\./(recc|test)/' | xargs wc -l | tail -1 | awk '{ print $1 }'

