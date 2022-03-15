from django.db import models

from core.models import TimeStamp

class WishList(TimeStamp):
    user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    planet = models.ForeignKey('planets.Planet', on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlists'
