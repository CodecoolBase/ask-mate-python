import csv


def read_file(filename):
    with open(filename, "r", encoding='utf-8') as f:
        reader_file = csv.DictReader(f)
        datas = []
        for line in reader_file:
            datas.append(dict(line))
        return datas


def write_to_file(filename, user_story):
    with open(filename, 'a', encoding='utf-8') as csvfile:
        datas_to_export = csv.DictWriter(csvfile)
        datas_to_export.writerow(user_story)
