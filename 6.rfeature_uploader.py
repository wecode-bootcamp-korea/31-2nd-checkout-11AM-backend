import csv, os, django, sys

os.chdir(".")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "checkout11am.settings")
django.setup()

from residences.models import *

CSV_PATH_RESIDENCE = 'db_csv/roomfeatureMock.csv'

with open(CSV_PATH_RESIDENCE) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        room_id    = row[0]
        feature_id = row[1]
        RoomFeature.objects.create(
            room    = Room.objects.get(id = room_id),
            feature = Feature.objects.get(id = feature_id)
        )
    
    
