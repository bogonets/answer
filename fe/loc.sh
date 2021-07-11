#!/usr/bin/env bash

find src/ \
    -name "*.vue" \
    -o -name "*.js" \
    -o -name "*.ts" \
    -o -name "*.css" \
    -o -name "*.sass" | \
  xargs wc -l | tail -1 | awk '{ print $1 }'
