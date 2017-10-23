#!/bin/bash

set -x
set -e

if [ ! -f /input/otp_src_$ERLANG_VSN.tar.gz ]; then
    curl -O http://erlang.org/download/otp_src_$ERLANG_VSN.tar.gz
    cp otp_src_$ERLANG_VSN.tar.gz /input/
else
    cp /input/otp_src_$ERLANG_VSN.tar.gz .
fi
tar xzf otp_src_$ERLANG_VSN.tar.gz
rm -f otp_src_$ERLANG_VSN.tar.gz
mv otp_src_$ERLANG_VSN otp-$ERLANG_VSN-$VSN
tar czf otp-"$ERLANG_VSN"_"$VSN".orig.tar.gz otp-$ERLANG_VSN-$VSN

cd /usr/local/src/otp-$ERLANG_VSN-$VSN
cp -a /usr/local/src/debian .
sed -i -e "s/ERLANG_VSN/$ERLANG_VSN/g" debian/control
sed -i -e "s/ERLANG_VSN/$ERLANG_VSN/g" debian/init.d
sed -i -e "s/ERLANG_VSN/$ERLANG_VSN/g" debian/postinst
sed -i -e "s/ERLANG_VSN/$ERLANG_VSN/g" debian/postrm
sed -i -e "s/ERLANG_VSN/$ERLANG_VSN/g" debian/rules

dch --create \
    -v $VSN-1 \
    --urgency low \
    --package otp-$ERLANG_VSN \
    --distribution unstable \
    "Initial release"

cat debian/changelog

dpkg-buildpackage -us -uc

cd ..
mv *.dsc *.changes *.deb *.orig.tar.gz /output/
