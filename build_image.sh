#!/bin/bash

IMAGE="$1"
DOCKERFILE="Dockerfile.$IMAGE"

cd docker

if [ ! -f "$DOCKERFILE" ]; then
    echo "No valid dockerfile for $IMAGE"
    exit 1
fi

IMAGE_NAME="erlang_$IMAGE"

if [ ! -z "$SUFFIX" ]; then
    DOCKERFILE="$DOCKERFILE.$SUFFIX"
    IMAGE_NAME="erlang_$IMAGE"_"$SUFFIX"
fi

docker build -f $DOCKERFILE --no-cache --rm -t $IMAGE_NAME .
