#!/bin/bash

users="sampo aurora anna atte julia valtteri"

port=8082

export PRODIGY_HOST=0.0.0.0

for user in $users; do
    echo "Starting prodigy for $user on port $port"
    echo "$user: http://ann.turkunlp.org:$port"

    export PRODIGY_PORT="$port"
    export PRODIGY_BASIC_AUTH_USER="$user"
    export PRODIGY_BASIC_AUTH_PASS=sentiment123
    python -m prodigy sentiment sentiment-"$user" docsample.jsonl "$user" \
	   -F sentiment.py &
    sleep 3
    
    port=$((port+1))
done
