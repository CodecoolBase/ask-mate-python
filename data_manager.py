import csv


def get_questions(id=None):
    """Get the data from the questions csv as an Ordered_Dict list"""
    csv_data = []
    with open('sample_data/questions.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = dict(row)

            if id is not None and id == d['id']:
                return d

            csv_data.append(d)

    return csv_data[::-1]


def get_answers():
    """Get the data from the answers csv as an Ordered_Dict list"""
    csv_data = []
    with open('sample_data/answers.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = dict(row)
            csv_data.append(d)
    return csv_data

