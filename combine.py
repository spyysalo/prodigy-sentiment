#!/usr/bin/env python3

# Combine annotations in TSV format with fields ID, annotator,
# timestamp, label, text.

import sys

from datetime import datetime
from collections import Counter, defaultdict
from logging import warning


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('tsv', nargs='+')
    return ap


def remove_flags(annotations):
    cleaned = []
    for a in annotations:
        if a.endswith('+FLAG'):
            a = a[:-len('+FLAG')]
        cleaned.append(a)
    return cleaned


def load_annotations(fn, text_by_id, annotations_by_id, annotations_by_date):
    with open(fn) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip('\n')
            fields = l.split('\t')
            try:
                id_, annotator, created, label, text = fields
                created = datetime.fromisoformat(created)    # Python 3.7
                created = str(created.date())
            except:
                raise ValueError('{} line {}: {}'.format(fn, ln, l))
            if id_ in text_by_id:
                assert text_by_id[id_] == text, 'text mismatch'
            text_by_id[id_] = text
            if annotator in annotations_by_id:
                assert annotations_by_id[id_][annotator] == label
                warning('redundant label: {}/{}'.format(id_, annotator))
            annotations_by_id[id_][annotator] = label
            annotations_by_date[created][annotator] += 1


def most_common(annotations):
    annotations = remove_flags(annotations)
    if not annotations:
        return '-'
    else:
        return Counter(annotations).most_common(1)[0][0]


def agreement(annotations):
    annotations = remove_flags(annotations)
    m = most_common(annotations)
    return sum(1 for a in annotations if a == m)/len(annotations)


def main(argv):
    args = argparser().parse_args(argv[1:])
    text_by_id = {}
    annotations_by_id = defaultdict(dict)
    annotations_by_date = defaultdict(lambda: defaultdict(int))
    for fn in args.tsv:
        load_annotations(fn, text_by_id, annotations_by_id, annotations_by_date)
    annotators = sorted(set(
        a for anns in annotations_by_id.values() for a in anns.keys()
    ))
    print('\t'.join(['ID', 'text', 'majority', 'agreement'] + annotators))
    for id_, text in text_by_id.items():
        fields = [id_, text]
        fields.append(most_common(annotations_by_id[id_].values()))
        fields.append(str(agreement(annotations_by_id[id_].values())))
        for a in annotators:
            fields.append(annotations_by_id[id_].get(a, '-'))
        print('\t'.join(fields))
    total_by_annotator = Counter()
    for d in sorted(annotations_by_date.keys()):
        counts = [(a, annotations_by_date[d][a]) for a in annotators]
        print(d, '\t'.join('{}:{}'.format(a, c) for a, c in counts), file=sys.stderr)
        for a in annotators:
            total_by_annotator[a] += annotations_by_date[d][a]
    print('TOTAL     ', '\t'.join('{}:{}'.format(a, t) for a, t in total_by_annotator.items()),
          file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
