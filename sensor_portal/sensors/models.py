from django.db import models
from sensor_portal.nexmo.models import Message
from ordered_model.models import OrderedModel
from geoposition.fields import GeopositionField
from django.contrib.sites.models import Site

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    position = GeopositionField(null=True, blank=True)
    active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    site = models.ForeignKey(Site, )

    def __str__(self):
        return self.name


class Metric(OrderedModel):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=5)
    eu_limit = models.IntegerField(null=True, blank=True, verbose_name='EU Concentration Limits')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        pass


class Reading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, null=True, blank=True)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    value = models.FloatField()
    recorded = models.DateTimeField()

    def __str__(self):
        return str(self.id)
