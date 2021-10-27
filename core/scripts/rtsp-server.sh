#!/usr/bin/env bash

VIDEO_PATH=$1
GUEST_VIDEO_PATH=/tmp/video.mp4
HOST_PORT=8554

if [[ ! -f "$VIDEO_PATH" ]]; then
    echo "Stream noise screen."
    docker run --rm \
        -e ENABLE_TIME_OVERLAY=true \
        -p $HOST_PORT:8554 \
        ullaakut/rtspatt
else
    echo "Stream a video file: $VIDEO_PATH"
    docker run --rm \
        -e ENABLE_TIME_OVERLAY=true \
        -e INPUT=$GUEST_VIDEO_PATH \
        -p $HOST_PORT:8554 \
        -v $VIDEO_PATH:$GUEST_VIDEO_PATH \
        ullaakut/rtspatt
fi
