#!/bin/bash

IMAGE="$1"

if [ ! -d "$IMAGE" ]; then
    echo "No valid image: $IMAGE"
    exit 1
fi

cd $IMAGE
docker build --no-cache --rm -t erlang_$IMAGE .
