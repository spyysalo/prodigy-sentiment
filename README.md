# prodigy-sentiment

Sentiment annotation config and support for prodigy annotation

## Clone tools

```
git clone https://github.com/spyysalo/prodigy-tools.git
```

## Start an instance of prodigy for each annotator

```
./start_all.sh
```

## Kill all instances of prodigy started by current user

```
./stop_all.sh
```

## Export annotations from DB and convert to TSV

```
./export_all.sh
```

## Combine exported annotations

```
COMBINED="combined-sentiment-annotations-`date '+%d%m%y'`.tsv"
python3 combine.py db-exports/sentiment-{anna,atte,aurora,julia}.tsv > $COMBINED
```

## Filter combined annotations

Only keep annotations with perfect or majority agreement on a label

```
COMBINED="combined-sentiment-annotations-`date '+%d%m%y'`.tsv"
python3 disagreements.py --agreed $COMBINED | egrep '^(perfect|majority)' | cut -f 2- > filtered.tsv
```
