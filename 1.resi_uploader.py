import csv, os, django, sys

os.chdir(".")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "checkout11am.settings")
django.setup()

from residences.models import *

CSV_PATH_RESIDENCE = 'db_csv/residenceMock.csv'
CSV_PATH_PLACE = 'db_csv/placesMock.csv'
CSV_PATH_IMAGE = 'db_csv/residenceimageMock.csv'

with open(CSV_PATH_RESIDENCE) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        region_title = row[0]
        if not Region.objects.filter(title = region_title).exists():
            Region.objects.create(
                title = region_title
            )

        region = Region.objects.get(title = region_title)
        category_title = row[1]
        if not Category.objects.filter(title = category_title).exists():
            Category.objects.create(
                title  = category_title,
                region = region
            )
        
        name         = row[2]
        sub_name     = row[3]
        description  = row[4]
        thumbnail    = row[5]
        address      = row[6]
        latitude     = row[7]
        longitude    = row[8]
        phone_number = row[9]
        email        = row[10]
        residence = Residence.objects.create(
            name         = name,
            sub_name     = sub_name,
            description  = description,
            thumbnail    = thumbnail,
            address      = address,
            latitude     = latitude,
            longitude    = longitude,
            phone_number = phone_number,
            email        = email,
            region       = Region.objects.get(title = region_title),
            category     = Category.objects.get(title = category_title)
        )
    
with open(CSV_PATH_PLACE) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    
    for row in data_reader:
        residence_id = row[0]
        name         = row[1]
        description  = row[2]
        latitude     = row[3]
        longitude    = row[4]
        Place.objects.create(
            residence   = Residence.objects.get(id = residence_id),
            name        = name,
            description = description,
            latitude    = latitude,
            longitude   = longitude
        )

with open(CSV_PATH_IMAGE) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    
    for row in data_reader:
        residence_id = row[0]
        image_url = row[1]
        ResidenceImage.objects.create(
            residence =  Residence.objects.get(id = residence_id),
            image_url = image_url
        )
