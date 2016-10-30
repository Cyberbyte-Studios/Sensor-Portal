from django.shortcuts import render, get_list_or_404
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import (
    GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, Line
)

from django.conf import settings

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
        fields = ('name', 'active', 'description')


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


def sensor_map(request):
    sensors = Sensor.objects.all()

    map_options = GMapOptions(map_type="roadmap", lat=52.3555177, lng=-1.1743197, zoom=6)

    plot = GMapPlot(
        x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, api_key=settings.GEOPOSITION_GOOGLE_MAPS_API_KEY
    )

    plot.title.text = 'Sensor Map'

    # TODO: This is nasty, fix it
    lat = []
    lon = []
    for sensor in sensors:
        lat.append(sensor.position.latitude)
        lon.append(sensor.position.longitude)

    source = ColumnDataSource(data=dict(
        lat=lat,
        lon=lon
    ))

    circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
    plot.add_glyph(source, circle)
    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())

    script, div = components(plot, CDN)

    return render(request, "sensors/map.html", {"map_chart": div, "map_js": script})


def metrics(request):
    sensor = Sensor.objects.get(pk=1)
    metrics = Metric.objects.all()
    tools = "pan,wheel_zoom,box_zoom,reset,save"
    line = Line(x="recorded", y="value", line_width=2)
    charts = []
    for metric in metrics:
        chart = figure(tools=tools)
        chart.title.text = metric.name
        readings = Reading.objects.filter(sensor=sensor, metric=1)
        df = readings.to_dataframe(index='recorded', fieldnames=['value'])
        source = ColumnDataSource(data=df)
        chart.add_glyph(source, line)
        charts.append(chart)

    script, div = components(charts)
    return render(request, "sensors/metrics.html", {"charts": div, "map_js": script})
