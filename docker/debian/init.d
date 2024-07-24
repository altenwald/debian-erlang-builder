#!/bin/sh
### BEGIN INIT INFO
# Provides:          epmd
# Required-Start:    $network $local_fs
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Erlang Port Mapper Daemon
# Description:       Erlang Port Mapper Daemon
### END INIT INFO

# Author: Manuel Rubio <manuel@altenwald.com>

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC=epmd             # Introduce a short description here
NAME=epmd             # Introduce the short server's name here
DAEMON=/opt/otp-ERLANG_VSN/bin/epmd  # Introduce the server's location here
DAEMON_ARGS=""        # Arguments to run the daemon with

# Exit if the package is not installed
[ -x $DAEMON ] || exit 0

# Load the VERBOSE setting and other rcS variables
. /lib/init/vars.sh

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.0-6) to ensure that this file is present.
. /lib/lsb/init-functions

#
# Function that starts the daemon/service
#
do_start()
{
	log_daemon_msg "Starting $DESC " "$NAME"
	$DAEMON -daemon -relaxed_command_check > /dev/null
        log_end_msg $?
}

#
# Function that stops the daemon/service
#
do_stop()
{
	log_daemon_msg "Stoping $DESC " "$NAME"
	$DAEMON -kill > /dev/null
        log_end_msg $?
}

do_status()
{
	log_daemon_msg "Checking $DESC " "$NAME"
	$DAEMON -names > /dev/null
        log_end_msg $? "is running"
}

case "$1" in
  start)
    do_start
  ;;
  stop)
	do_stop
	;;
  status)
       do_status
       ;;
  restart|force-reload)
	#
	# If the "reload" option is implemented then remove the
	# 'force-reload' alias
	#
	do_stop
	do_start
	;;
  *)
	echo "Usage: $(basename $0) {start|stop|status|restart|force-reload}" >&2
	exit 3
	;;
esac

:
