import csv, os, django, sys

os.chdir(".")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "checkout11am.settings")
django.setup()

from residences.models import *

CSV_PATH_RESIDENCE = 'db_csv/featureMock.csv'

with open(CSV_PATH_RESIDENCE) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        name = row[0]
        Feature.objects.create(
            name = name
        )
    
    
