from rest_framework import viewsets
from rest_framework import filters

import django_filters
from django_filters.widgets import RangeWidget

from sensor_portal.sensors.models import Sensor, Metric, Reading
from sensor_portal.sensors.serializers import SensorSerializer, MetricSerializer, ReadingSerializer


FILTERS = (
    filters.DjangoFilterBackend,
    filters.SearchFilter,
    filters.OrderingFilter
)

class SensorFilter(filters.FilterSet):

    class Meta:
        model = Sensor
        fields = ('name', 'active','description')

class MetricFilter(filters.FilterSet):

    class Meta:
        model = Metric
        fields = ('name', 'unit', 'eu_limit', 'description')

class ReadingFilter(filters.FilterSet):
    recorded = django_filters.DateTimeFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'dd/mm/yyyy hh:mm'}))

    class Meta:
        model = Reading
        fields = ('sensor', 'message', 'metric', 'value', 'recorded')


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    filter_backends = FILTERS
    filter_class = SensorFilter
    serializer_class = SensorSerializer
    search_fields = ('name', 'position', 'description')
    ordering_fields = ('name', 'position', 'active')

class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    filter_backends = FILTERS
    filter_class = MetricFilter
    serializer_class = MetricSerializer
    search_fields = ('name', 'unit', 'eu_limit', 'description')
    ordering_fields = ('name', 'unit', 'eu_limit')

class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all()
    filter_backends = FILTERS
    filter_class = ReadingFilter
    serializer_class = ReadingSerializer
    search_fields = ('sensor__name', 'message__text', 'value')
    ordering_fields = ('sensor', 'message', 'metric', 'value', 'recorded')
