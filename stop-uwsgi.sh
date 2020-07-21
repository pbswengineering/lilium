#!/bin/bash
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

UWSGI="$HOME/anaconda3/bin/uwsgi"
if [ -f "$UWSGI" ]; then
    echo "Using $UWSGI"
else
    echo "$UWSGI not found, looking for uwsgi in PATH"
    UWSGI=uwsgi
fi
"$UWSGI" --stop /tmp/lilium-master.pid
