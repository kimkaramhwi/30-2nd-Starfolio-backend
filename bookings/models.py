from django.db import models

from core.models import TimeStamp

class Booking(TimeStamp):
    booking_number     = models.UUIDField()
    start_date         = models.DateField()
    end_date           = models.DateField()
    number_of_adults   = models.IntegerField()
    number_of_children = models.IntegerField()
    user_request       = models.TextField(blank=True)
    user               = models.ForeignKey('users.User', on_delete=models.CASCADE)
    booking_status     = models.ForeignKey('BookingStatus', on_delete=models.CASCADE)
    planet             = models.ForeignKey('planets.Planet', on_delete=models.CASCADE)
    accomodation       = models.ForeignKey('planets.Accomodation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'bookings'

class BookingStatus(models.Model):
    status = models.CharField(max_length=45)

    class Meta:
        db_table = 'booking_status'
