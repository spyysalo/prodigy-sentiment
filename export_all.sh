#!/bin/bash

set -euo pipefail

# https://stackoverflow.com/a/246128
BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

OUTDIR="$BASEDIR/db-exports"

mkdir -p "$OUTDIR"

prodigy stats -l -NF \
    | python3 -c 'import sys; import json; print("\n".join(json.load(sys.stdin)["datasets"]))' \
    | while read d; do
    o="$OUTDIR/$d.jsonl"
    echo "Exporting $d to $o"
    python -m prodigy db-out "$d" > "$o"
    c="$OUTDIR/$d.tsv"
    echo "Converting $o to $c"
    python3 prodigy-tools/jsonl2tsv.py "$o" > "$c"
done
