from django.db import models
from utilities.timestamp import TimeStamp

class User(TimeStamp):
    kakaoid       = models.IntegerField()
    nickname      = models.CharField(max_length=50, unique=True)
    email         = models.CharField(max_length=100, null=True)
    date_of_birth = models.DateField()
    
    class Meta:
        db_table = 'users'
        
class Wishlist(models.Model):
    user      = models.ForeignKey('users.User', on_delete=models.CASCADE)
    residence = models.ForeignKey('residents.Residence', on_delete=models.CASCADE)
    room      = models.ForeignKey('residents.Room', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'wishlists'
        constraints = [models.UniqueConstraint(
            fields = ['user', 'residence'],
            name = 'wishlists_user_residence_unq'
            )
        ]