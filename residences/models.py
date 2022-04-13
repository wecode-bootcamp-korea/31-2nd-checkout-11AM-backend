from django.db import models

from utilities.timestamp import TimeStamp

class Region(models.Model): 
    title = models.CharField(max_length=50)

    class Meta: 
        db_table = 'regions'

class Category(models.Model):
    title  = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='categories')

    class Meta: 
        db_table = 'categories'

class Residence(TimeStamp):
    name         = models.CharField(max_length=200)
    sub_name     = models.CharField(max_length=200)
    region       = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='residences')
    category     = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='residences')
    description  = models.TextField()
    thumbnail    = models.CharField(max_length=200)
    address      = models.CharField(max_length=200, default='')
    latitude     = models.DecimalField(max_digits=11, decimal_places=8)
    longitude    = models.DecimalField(max_digits=11, decimal_places=8)
    phone_number = models.CharField(max_length=50)
    email        = models.CharField(max_length=200)

    class Meta: 
        db_table = 'residences'

class ResidenceImage(models.Model):
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE, related_name='residence_images')
    image_url = models.CharField(max_length=2000)

    class Meta: 
        db_table = 'residence_images'
        
class Amenity(models.Model): 
    name = models.CharField(max_length=100)

    class Meta: 
        db_table = 'amenities'

class Feature(models.Model): 
    name = models.CharField(max_length=100)

    class Meta: 
        db_table = 'features'

class Room(models.Model):
    name        = models.CharField(max_length=200)
    price       = models.DecimalField(max_digits=30, decimal_places=2)
    description = models.TextField()
    area        = models.IntegerField()
    person      = models.IntegerField()
    max_person  = models.IntegerField()
    bedspace    = models.IntegerField()
    residence   = models.ForeignKey(Residence, on_delete=models.CASCADE, related_name='rooms')
    features    = models.ManyToManyField('Feature', through='RoomFeature', related_name='rooms')
    amenities   = models.ManyToManyField('Amenity', through='RoomAmenity', related_name='rooms')

    class Meta: 
        db_table = 'rooms'

class RoomFeature(models.Model):
    room    = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_features')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='room_features')
    
    class Meta:
        db_table = 'room_features'
        
class RoomAmenity(models.Model):
    room    = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_amenities')
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE, related_name='room_amenities')
    
    class Meta:
        db_table = 'room_amenities'

class RoomImage(models.Model):
    room      = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_images')
    image_url = models.CharField(max_length=2000)

    class Meta: 
        db_table = 'room_images'

class Place(models.Model):
    residence   = models.ForeignKey(Residence, on_delete=models.CASCADE, related_name='places')
    name        = models.CharField(max_length=50)
    description = models.TextField()
    latitude    = models.DecimalField(max_digits=11, decimal_places=8)
    longitude   = models.DecimalField(max_digits=11, decimal_places=8)
    
    class Meta:
        db_table = 'places'
    