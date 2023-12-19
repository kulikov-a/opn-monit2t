#!/bin/sh

if t_errors=$(/usr/local/bin/python3 /usr/local/opnsense/scripts/OPNsense/Monit2T/monit2t.py $1 2>&1); then
    echo "OK"
else
    echo "$t_errors"
fi

exit 0
