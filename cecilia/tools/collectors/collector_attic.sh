#!/bin/bash

while true
do
    ( cd ${0%/*}; python3 collector.py --gpio attic )
done
