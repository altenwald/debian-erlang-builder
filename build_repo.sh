#!/usr/bin/env bash

BASE_PATH=apt.altenwald.com

if [ ! -f "$BASE_PATH/conf/distributions" ] || [ ! -f "$BASE_PATH/altenwald.key" ]; then
    echo "missing files for repository"
    exit 1
fi

for distro in stretch:9 buster:10 bullseye:11 bookworm:12; do
    DIST_NAME=$(echo $distro | cut -d: -f1)
    DIST_VSN=$(echo $distro | cut -d: -f2)

    reprepro --ask-passphrase \
        --dbdir ./debian/$DIST_VSN/db \
        -Vb $BASE_PATH/ \
        includedeb $DIST_NAME debian/$DIST_VSN/pool/*.deb

    find debian/$DIST_VSN/pool \
        -iname '*.dsc' \
        -exec reprepro \
        --ask-passphrase \
        --dbdir ./debian/$DIST_VSN/db \
        -Vb $BASE_PATH/ includedsc $DIST_NAME {} \;
done
