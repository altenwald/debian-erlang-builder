FROM debian:squeeze

LABEL maintainer="Manuel Rubio <manuel@altenwald.com>"
LABEL description="Debian Stretch to build Erlang/OTP packages"

ENV ERLANG_VSN 19.3
ENV VSN 1.0.0
ENV DEBIAN_FRONTEND noninteractive
ENV DEBEMAIL manuel@altenwald.com
ENV DEBFULLNAME "Manuel Rubio"

ADD sources.list /etc/apt/sources.list
ADD 00noexpire /etc/apt/apt.conf.d/00noexpire
RUN apt-get update -qq
RUN apt-get dist-upgrade -y
RUN apt-get build-dep -y --force-yes erlang
RUN apt-get install -y --force-yes build-essential curl devscripts libxml2-utils

RUN apt-get clean

WORKDIR /usr/local/src
ADD debian debian
ADD debian_erlang.sh /usr/local/bin/debian_erlang.sh
RUN chmod +x /usr/local/bin/debian_erlang.sh

CMD ["debian_erlang.sh"]
