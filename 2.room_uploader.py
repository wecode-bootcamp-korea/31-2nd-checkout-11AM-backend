import csv, os, django, sys

os.chdir(".")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "checkout11am.settings")
django.setup()
from residences.models import *

CSV_PATH_RESIDENCE = 'db_csv/roomsMock.csv'
CSV_PATH_IMAGE = 'db_csv/roomimageMock.csv'

with open(CSV_PATH_RESIDENCE) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        room_name      = row[0]
        price          = row[1]
        description    = row[2]
        area           = row[3]
        person         = row[4]
        max_person     = row[5]
        bedspace       = row[6]
        residence_name = row[7]
        Room.objects.create(
            name        = room_name,
            price       = price,
            description = description,
            area        = area,
            person      = person,
            max_person  = max_person,
            bedspace    = bedspace,
            residence   = Residence.objects.get(name = residence_name)
        )
    
with open(CSV_PATH_IMAGE) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    
    for row in data_reader:
        room_id = row[0]
        image_url = row[1]
        RoomImage.objects.create(
            room =  Room.objects.get(id = room_id),
            image_url = image_url
        )    
