#!/bin/bash

set -x
set -e

if [ ! -f /input/otp_src_$ERLANG_VSN.tar.gz ]; then
    echo "file doesn't exist /input/otp_src_$ERLANG_VSN.tar.gz"
    exit 1
fi
tar xzf /input/otp_src_$ERLANG_VSN.tar.gz
mv otp_src_$ERLANG_VSN otp-$ERLANG_VSN-$VSN
tar czf otp-"$ERLANG_VSN"_"$VSN".orig.tar.gz otp-$ERLANG_VSN-$VSN

LAST_DEB="$(find /output -iname "otp-$ERLANG_VSN"_"*-1.debian.tar.xz" | sort --version-sort | tail -1)"

cd /usr/local/src/otp-$ERLANG_VSN-$VSN

if [ -z "$LAST_DEB" ]; then
    cp -a /usr/local/src/debian .
    sed -i -e "s/ERLANG_VSN/$ERLANG_VSN/g" debian/control
    sed -i -e "s/ERLANG_VSN/$ERLANG_VSN/g" debian/init.d
    sed -i -e "s/ERLANG_VSN/$ERLANG_VSN/g" debian/postinst
    sed -i -e "s/ERLANG_VSN/$ERLANG_VSN/g" debian/postrm
    sed -i -e "s/ERLANG_VSN/$ERLANG_VSN/g" debian/rules

    dch --create \
        -v "$VSN-1" \
        --urgency low \
        --package otp-$ERLANG_VSN \
        --distribution unstable \
        "Initial release"
else
    tar xJf "$LAST_DEB"
    cat debian/changelog

    if [ "$(grep "($VSN-1)" debian/changelog)" ]; then
        echo "version $VSN exists in debian/changelog"
        exit 1
    fi

    dch -v "$VSN-1" \
        --urgency low \
        --package otp-$ERLANG_VSN \
        --distribution unstable \
        "Release from git"
fi

cat debian/changelog

dpkg-buildpackage -us -uc

cd ..
mv *.dsc *.changes *.deb *.orig.tar.gz *.debian.tar.* /output/
