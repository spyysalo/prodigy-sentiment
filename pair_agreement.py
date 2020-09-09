#!/usr/bin/env python3

import sys
import numpy as np

from collections import defaultdict

from sklearn.metrics import cohen_kappa_score


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('--head', default=None, type=int)
    ap.add_argument('--tail', default=None, type=int)
    ap.add_argument('tsv', nargs='+')
    return ap


def load_header(fn, l):
    l = l.rstrip('\n')
    fields = l.split('\t')
    if (fields[0] != 'ID' or
        fields[1] != 'text' or
        fields[2] != 'majority' or
        fields[3] != 'agreement'):
        raise ValueError('{} header: {}'.format(fn, l))
    annotators = fields[4:]
    print('Annotations in {}: {}'.format(fn, ' '.join(annotators)))
    return annotators


def evaluate(fn, options):
    annotations_by_pair = defaultdict(list)
    ignored, total = 0, 0
    with open(fn) as f:
        header = f.readline()
        annotators = load_header(fn, header)
        for ln, l in enumerate(f, start=2):
            l = l.rstrip('\n')
            fields = l.split('\t')
            id_, text, majority, agreement = fields[:4]
            annotations = fields[4:]
            if len(annotators) != len(annotations):
                raise ValueError('{} line {}: {}'.format(fn, ln, l))
            for i in range(len(annotations)):
                for j in range(i+1, len(annotations)):
                    pair = (annotators[i], annotators[j])
                    anns = (annotations[i], annotations[j])
                    if '-' in anns or '-IGNORE-' in anns:
                        # print('skip {}'.format(l))
                        ignored += 1
                    else:
                        annotations_by_pair[pair].append(anns)
                    total += 1
    if ignored:
        print('Note: ignored {}/{} pairs with skip or incomplete'.format(
            ignored, total))
    if options.head is not None:
        for p, anns in annotations_by_pair.items():
            annotations_by_pair[p] = anns[:options.head]
    if options.tail is not None:
        for p, anns in annotations_by_pair.items():
            annotations_by_pair[p] = anns[-options.tail:]
    accuracies, kappas = [], []
    for i in range(len(annotations)):
        for j in range(i+1, len(annotations)):
            pair = (annotators[i], annotators[j])
            a1 = np.array([i for i, j in annotations_by_pair[pair]])
            a2 = np.array([j for i, j in annotations_by_pair[pair]])
            agreed = sum(a1 == a2)
            total = len(annotations_by_pair[pair])
            kappa = cohen_kappa_score(a1, a2)
            print('{}\t{}\taccuracy\t{:.1%}\t({}/{})\tkappa\t{:.2}'.format(
                annotators[i], annotators[j], agreed/total, agreed, total,
                kappa))
            accuracies.append(agreed/total)
            kappas.append(kappa)
    print('AVERAGE ACCURACY\t{:.1%}'.format(np.mean(accuracies)))
    print('AVERAGE KAPPA\t{:.2}'.format(np.mean(kappas)))


def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.tsv:
        evaluate(fn, args)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
