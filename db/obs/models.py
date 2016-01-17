from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from wq.db.patterns.models import FiledModel


class Site(models.Model):
    name = models.CharField(max_length=100, unique=True)
    geometry = models.GeometryField(srid=settings.SRID)
    accuracy = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class ObservationType(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='forms')
    description = models.TextField()
    author = models.ForeignKey('auth.User')
    html = models.TextField()

    def __str__(self):
        return self.name


class Observation(FiledModel):
    observer = models.ForeignKey('auth.User')
    type = models.ForeignKey(ObservationType)
    entered = models.DateTimeField(auto_now_add=True)
    site = models.ForeignKey(Site)
    values = JSONField(null=True, blank=True)

    def __str__(self):
        return "%s Observation on %s" % (
            self.type, self.entered.date()
        )
