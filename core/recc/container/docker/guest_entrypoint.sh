#!/usr/bin/env bash

if [[ $RECC_VERBOSE -ge 1 ]]; then
    env | grep "^RECC_.*"
fi

_RECC_MODULE_FREEZE=$(python -m pip list --format freeze | grep '^recc==.*')

if [[ -z "$_RECC_MODULE_FREEZE" ]]; then
    echo "Not found 'recc' module."
    if [[ -n "$RECC_INSTALL_VERSION" ]]; then
        python -m pip install "recc==$RECC_INSTALL_VERSION"
    else
        python -m pip install -U recc
    fi
fi

python -m recc task
