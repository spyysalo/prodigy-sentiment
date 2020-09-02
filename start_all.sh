#!/bin/bash

users="sampo"

port=8082

export PRODIGY_HOST=0.0.0.0

for user in $users; do
    echo "Starting prodigy for $user on port $port"

    export PRODIGY_PORT="$port"
    export PRODIGY_BASIC_AUTH_USER="$user"
    export PRODIGY_BASIC_AUTH_PASS=sentiment
    python -m prodigy sentiment sentiment-"$user" docsample.jsonl "$user" \
	   -F sentiment.py &
    sleep 10
    
    port=$((port+1))
done
