#!/bin/bash

set -e
set -x

ERLANG_VSN="${ERLANG_VSN:-19.3}"
VSN="${VSN:-1.0.0}"

docker build -t erlang_bookworm .
docker run -e ERLANG_VSN=$ERLANG_VSN \
	   -e ERL_TOP=/usr/local/src/otp-$ERLANG_VSN-$VSN \
           -v `pwd`/output:/output \
           -v `pwd`/../input:/input \
           --rm \
           -it erlang_bookworm
