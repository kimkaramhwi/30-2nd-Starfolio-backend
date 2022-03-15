from django.db import models

from core.models import TimeStamp

class Galaxy(TimeStamp):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'galaxy'

class Planet(TimeStamp):
    name      = models.CharField(max_length=45)
    theme     = models.CharField(max_length=45)
    thumbnail = models.URLField(max_length=1000)
    galaxy    = models.ForeignKey('Galaxy', on_delete=models.CASCADE)

    class Meta:
        db_table = 'planets'

class PlanetImage(models.Model):
    image_url = models.URLField(max_length=1000)
    planet    = models.ForeignKey('Planet', on_delete=models.CASCADE)

    class Meta:
        db_table = 'planet_images'

class Accomodation(TimeStamp):
    name          = models.CharField(max_length=45)
    price         = models.DecimalField(max_digits=11, decimal_places=2)
    min_of_people = models.PositiveIntegerField()
    max_of_people = models.PositiveIntegerField()
    num_of_bed    = models.PositiveIntegerField()
    description   = models.TextField()
    planet        = models.ForeignKey('Planet', on_delete=models.CASCADE)

    class Meta:
        db_table = 'accomodations'

class AccomodationImage(models.Model):
    image_url    = models.URLField(max_length=1000)
    accomodation = models.ForeignKey('Accomodation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'accomodation_images'
