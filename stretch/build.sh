#!/bin/bash

set -e
set -x

ERLANG_VSN="${ERLANG_VSN:-19.3}"

docker build -t erlang_stretch .
docker run -e ERLANG_VSN=$ERLANG_VSN \
           -v `pwd`/output:/output \
           -v `pwd`/../input:/input \
           --rm \
           -it erlang_stretch
