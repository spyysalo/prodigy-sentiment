#!/usr/bin/env python3

import sys

from collections import Counter


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-a', '--agreed', default=False, action='store_true',
                    help='Also include agreed cases in output')
    ap.add_argument('tsv', nargs='+')
    return ap


def most_common(annotations):
    return Counter(annotations).most_common(1)[0][0]


def agreement(annotations):
    m = most_common(annotations)
    return sum(1 for a in annotations if a == m)/len(annotations)


def remove_flags(annotations):
    cleaned = []
    for a in annotations:
        if a.endswith('+FLAG'):
            a = a[:-len('+FLAG')]
        cleaned.append(a)
    return cleaned


def print_disagreements(fn, options):
    ignored, total = 0, 0
    with open(fn) as f:
        header = f.readline()
        for ln, l in enumerate(f, start=2):
            l = l.rstrip('\n')
            fields = l.split('\t')
            annotations = fields[4:]
            annotations = remove_flags(annotations)
            if '-' in annotations or '-IGNORE-' in annotations:
                ignored += 1
            elif agreement(annotations) == 1:
                if options.agreed:    # skip by default
                    print('perfect\t{}'.format(l))                
            elif agreement(annotations) > 0.5:
                print('majority\t{}'.format(l))                
            elif agreement(annotations) == 0.5 and len(set(annotations)) == 2:
                print('split\t{}'.format(l))
            else:
                print('mixed\t{}'.format(l))
            total += 1


def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.tsv:
        print_disagreements(fn, args)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))

