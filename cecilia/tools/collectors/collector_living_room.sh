#!/bin/bash

while true
do
    ( cd ${0%/*}; python3 collector.py --arduino=192.168.16.11 living_room )
done
