#!/bin/bash

user="smp"

ps aux | egrep '^'"$user"'\b' | egrep '[p]rodigy' | awk '{ print $2 }' | \
while read p; do
    echo "Killing $p ...."
    kill $p
    sleep 10
done
