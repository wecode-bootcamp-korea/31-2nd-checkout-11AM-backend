from django.db import models

from utilities.timestamp import TimeStamp

class Reservation(TimeStamp):
    checkin_date       = models.DateField()
    checkout_date      = models.DateField()
    number_of_people   = models.IntegerField()
    user_request       = models.TextField(blank=True)
    price              = models.DecimalField(max_digits=11, decimal_places=2)
    user               = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reservations')
    residence          = models.ForeignKey('residences.Residence', on_delete=models.CASCADE, related_name='reservations')
    room               = models.ForeignKey('residences.Room', on_delete=models.CASCADE, related_name='reservations')

    class Meta:
        db_table = 'reservations'