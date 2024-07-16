import csv
from django.conf import settings
import os

def read_csv(file_path):
    data = []
    csv_file_path = os.path.join(settings.BASE_DIR, file_path)

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data