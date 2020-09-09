#!/usr/bin/env python

# Split annotated data in TSV format with fields ID, text, label [...]

import sys
import random

from logging import warning


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('--seed', default=None, type=int)
    ap.add_argument('ratio', type=float)
    ap.add_argument('out1')
    ap.add_argument('out2')
    ap.add_argument('tsv', nargs='+')
    return ap


def document_id(id_):
    try:
        doc_id, idx = id_.split('.')
        idx = int(idx)
    except:
        raise ValueError('Failed to parse ID as DOC.IDX: {}'.format(id_))
    return doc_id


def load_annotations(fn, options):
    seen_doc_ids = set()
    annotations = []
    with open(fn) as f:
        header = f.readline().rstrip('\n')
        print('skip header {}'.format(header), file=sys.stderr)
        prev_doc_id = None
        for ln, l in enumerate(f, start=2):
            l = l.rstrip('\n')
            fields = l.split('\t')
            id_, text, label = fields[:3]
            doc_id = document_id(id_)
            if doc_id != prev_doc_id:
                annotations.append([])
                if doc_id in seen_doc_ids:
                    warning('dup doc ID: {}'.format(doc_id))
                seen_doc_ids.add(doc_id)
            annotations[-1].append(l)
            prev_doc_id = doc_id
    return annotations


def main(argv):
    args = argparser().parse_args(argv[1:])
    random.seed(args.seed)
    data = []
    for fn in args.tsv:
        data.extend(load_annotations(fn, args))
    random.shuffle(data)
    total = sum(len(d) for d in data)
    idx, out1_count, out2_count = 0, 0, 0
    with open(args.out1, 'wt') as out:
        while out1_count/total < args.ratio:
            for l in data[idx]:
                print(l, file=out)
                out1_count += 1
            idx += 1
    with open(args.out2, 'wt') as out:
        while idx < len(data):
            for l in data[idx]:
                print(l, file=out)
                out2_count += 1
            idx += 1
    print('Wrote {:.1%} ({}/{}) to {}, {:.1%} ({}/{}) to {}'.format(
        out1_count/total, out1_count, total, args.out1,
        out2_count/total, out2_count, total, args.out2
    ), file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
