#!/bin/bash

ps aux | egrep '^'"$USER"'\b' | egrep '[p]rodigy' | awk '{ print $2 }' | \
while read p; do
    echo "Killing $p ...."
    kill $p
    sleep 3
done
