#!/usr/bin/env bash

function create_dir
{
    local dir=$1
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        echo "Create directory: $dir"
    else
        echo "Exists directory: $dir"
    fi
}

ROOT_DIR=/usr/local/recc
RECC_PYENV_DIR=$ROOT_DIR/python

create_dir "$ROOT_DIR"
create_dir "$RECC_PYENV_DIR"

RECC_PYTHON_EXECUTABLE_PATH=$RECC_PYENV_DIR/bin/python3
if [[ ! -x "$RECC_PYTHON_EXECUTABLE_PATH" ]]; then
    # apt install python3.8-venv
    python3 -m venv --copies --prompt recc "$RECC_PYENV_DIR"
fi

