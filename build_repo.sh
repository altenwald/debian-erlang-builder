#!/usr/bin/env bash

SECTION="interpreters"
COMPONENT="contrib"

if [ -z "$BASE_PATH" ]; then
    echo "missing BASE_PATH"
    exit 1
fi

if [ ! -f "$BASE_PATH/conf/distributions" ] || [ ! -f "$BASE_PATH/altenwald.key" ]; then
    echo "missing files for repository"
    exit 1
fi

function add() {
    DIST_NAME="$1"; shift
    DIST_VSN="$1"; shift
    COMMAND="$1"; shift
    FILE="$1"; shift
    EXTRA="$@"

    echo "[$COMMAND] $DIST_NAME <- $FILE"
    reprepro --ask-passphrase \
      --dbdir ./debian/$DIST_VSN/db \
      -Vb $BASE_PATH/ \
      -S $SECTION \
      -C $COMPONENT/$DIST_NAME \
      $EXTRA $COMMAND $DIST_NAME $FILE
}

for distro in stretch:9 buster:10 bullseye:11 bookworm:12 trixie:13; do 
    DIST_NAME=$(echo $distro | cut -d: -f1)
    DIST_VSN=$(echo $distro | cut -d: -f2)

    for FILE in debian/$DIST_VSN/pool/*; do
        case "${FILE##*.}" in
            "dsc") add $DIST_NAME $DIST_VSN includedsc $FILE ;;
            "deb") add $DIST_NAME $DIST_VSN includedeb $FILE ;;
            "changes") add $DIST_NAME $DIST_VSN include $FILE --ignore=wrongdistribution ;;
        esac
    done
done
