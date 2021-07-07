#!/usr/bin/env bash

FE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)

SRC=$FE_DIR/src/assets/answer-logo-notext.svg
PUBLIC_DIR=$FE_DIR/public
ICONS_DIR=$FE_DIR/public/img/icons
DENSITY=100

function exit_if_error
{
    local code=$?
    if [[ $code -eq 0 ]]; then
        echo "OK"
    else
        echo "Error ($code)"
        exit $code
    fi
}

function run_convert_png
{
    local dest=$1
    local size=$2

    local input_options=("-density" "$DENSITY" "-background" "none" "-trim")
    local output_options=("-gravity" "center" "-resize" "${size}" "-extent" "${size}x${size}" "-format" "png")

    echo -n "convert(png) '$dest' ..."
    convert ${input_options[@]} "$SRC" ${output_options[@]} "$dest"
    exit_if_error
}

function run_convert_ico
{
    local dest=$1
    local size=$2

    local input_options=("-density" "$DENSITY" "-background" "none" "-trim")
    local output_options=("-gravity" "center" "-resize" "${size}" "-extent" "${size}x${size}" "-format" "ico")

    echo -n "convert(ico) '$dest' ..."
    convert ${input_options[@]} "$SRC" ${output_options[@]} "$dest"
    exit_if_error
}

function run_copy
{
    local dest=$1

    echo -n "copy '$dest' ..."
    cp "$SRC" "$dest"
    exit_if_error
}

run_convert_png "$ICONS_DIR/android-chrome-192x192.png" 192
run_convert_png "$ICONS_DIR/android-chrome-512x512.png" 512
run_convert_png "$ICONS_DIR/android-chrome-maskable-192x192.png" 192
run_convert_png "$ICONS_DIR/android-chrome-maskable-512x512.png" 512
run_convert_png "$ICONS_DIR/apple-touch-icon-120x120.png" 120
run_convert_png "$ICONS_DIR/apple-touch-icon-152x152.png" 152
run_convert_png "$ICONS_DIR/apple-touch-icon-180x180.png" 180
run_convert_png "$ICONS_DIR/apple-touch-icon-60x60.png" 60
run_convert_png "$ICONS_DIR/apple-touch-icon-76x76.png" 76
run_convert_png "$ICONS_DIR/apple-touch-icon.png" 180
run_convert_png "$ICONS_DIR/favicon-16x16.png" 16
run_convert_png "$ICONS_DIR/favicon-32x32.png" 32
run_convert_png "$ICONS_DIR/msapplication-icon-144x144.png" 144
run_convert_png "$ICONS_DIR/mstile-150x150.png" 150
run_convert_ico "$PUBLIC_DIR/favicon.ico" 32
run_copy "$ICONS_DIR/safari-pinned-tab.svg"

