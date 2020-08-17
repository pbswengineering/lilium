#!/bin/bash
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

make checkdb  # repair tables if needed
UWSGI="$HOME/anaconda3/bin/uwsgi"
if [ -f "$UWSGI" ]; then
    echo "Using $UWSGI"
else
    echo "$UWSGI not found, looking for uwsgi in PATH"
    UWSGI=uwsgi
fi
SCRIPT_PATH=$(dirname "$(readlink -f "$0")")
"$UWSGI" --chdir="$SCRIPT_PATH" \
    --module=lilium.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=lilium.settings \
    --master \
    --pidfile=/tmp/lilium-master.pid \
    --http=0.0.0.0:2710 \
    --processes=5 \
    --uid=1000 \
    --gid=1000 \
    --harakiri=20 \
    --max-requests=5000 \
    --vacuum \
    --daemonize="$SCRIPT_PATH/logs/uwsgi.log"
