import datetime
import prodigy

from prodigy.components.loaders import JSONL


def iso8601_now():
    """Return current time in ISO 8601 format w/o microseconds."""
    return datetime.datetime.now().replace(microsecond=0).isoformat(' ')


def count_lines(file_path):
    return sum(1 for i in open(file_path))


@prodigy.recipe(
    'sentiment',
    dataset=('The dataset to save to', 'positional', None, str),
    file_path=('Path to texts', 'positional', None, str),
    annotator=('Annotater name', 'positional', None, str),
)
def sentiment(dataset, file_path, annotator):
    """Annotate the sentiment of texts using different mood options."""
    stream = JSONL(file_path)     # load in the JSONL file
    stream = add_options(stream)  # add options to each task

    # TODO need to remove previously annotated
    total_lines = count_lines(file_path)
    def progress(controller, update_return_value):
        return controller.total_annotated / total_lines

    def before_db(examples):
        for e in examples:
            if 'created' not in e:
                e['created'] = iso8601_now()
            if 'annotator' not in e:
                e['annotator'] = annotator
        return examples
    
    return {
        'dataset': dataset,   # save annotations in this dataset
        'view_id': 'choice',  # use the choice interface
        'stream': stream,
        'progress': progress,
        'before_db': before_db,
    }


def add_options(stream):
    # Helper function to add options to every task in a stream
    options = [
        { 'id': 'positive', 'text': '😀 Positive' },
        { 'id': 'negative', 'text': '🙁 Negative' },
        { 'id': 'neither', 'text': '😶 Neither' },
        { 'id': 'mixed', 'text': '🤨 Mixed' },
    ]
    for task in stream:
        task['options'] = options
        yield task
