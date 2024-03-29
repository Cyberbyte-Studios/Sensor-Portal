from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import (
    GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool,
    WheelZoomTool, BoxSelectTool, Line,
    Span)

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from datetime import timedelta

from rest_framework import viewsets
from rest_framework import filters

import django_filters
from django_filters.widgets import RangeWidget

from sensor_portal.sensors.models import Sensor, Metric, Reading
from sensor_portal.sensors.serializers import SensorSerializer, MetricSerializer, ReadingSerializer

class ReadingFilter(filters.FilterSet):
    recorded = django_filters.DateTimeFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'dd/mm/yyyy hh:mm'}))

    class Meta:
        model = Reading
        fields = ('sensor', 'message', 'metric', 'value', 'recorded')


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    filter_class = SensorFilter
    serializer_class = SensorSerializer
    search_fields = ('name', 'position', 'description')
    filter_fields = ('name', 'position', 'active')
    ordering_fields = ('name', 'position', 'active')


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    filter_class = MetricFilter
    serializer_class = MetricSerializer
    search_fields = ('name', 'unit', 'eu_limit', 'description')
    filter_fields = ('name', 'unit', 'eu_limit')
    ordering_fields = ('name', 'unit', 'eu_limit')


class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.filter(hidden=False)
    filter_class = ReadingFilter
    serializer_class = ReadingSerializer
    search_fields = ('sensor__name', 'message__text', 'value')
    ordering_fields = ('sensor', 'message', 'metric', 'value', 'recorded')


def sensor_list(request):
    sensors = Sensor.objects.filter(active=True)
    return render(request, "sensors/sensor-list.html", {"sensors": sensors})


def sensor_map(request):
    sensors = Sensor.objects.filter()

    source = ColumnDataSource(data=dict(
        lat=[sensor.position.latitude for sensor in sensors],
        lon=[sensor.position.longitude for sensor in sensors]
    ))

    script, div = render_map(plot=map_graph(source=source))

    return render(request, "sensors/map.html", {"map_chart": div, "map_js": script})


def map_graph(source, title='Sensor Map'):
    map_options = GMapOptions(map_type="roadmap", lat=52.3555177, lng=-1.1743197, zoom=6)

    plot = GMapPlot(
        x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options,
        api_key=settings.GEOPOSITION_GOOGLE_MAPS_API_KEY
    )

    plot.title.text = title

    circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
    plot.add_glyph(source, circle)
    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())


def render_map(plot):
    return components(plot, CDN)


def sensor_metrics(request, id):
    sensor = get_object_or_404(Sensor, pk=id)
    metrics = Metric.objects.all()
    tools = "pan,wheel_zoom,box_zoom,reset,save"
    line = Line(x="recorded", y="value", line_width=2)
    charts = []
    for metric in metrics:
        x_axis_label = metric.x_axis or metric.unit
        y_axis_label = metric.y_axis or "Date"

        chart = figure(
            tools=tools,
            x_axis_type="datetime",
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            logo=None,
            plot_height=200,
            sizing_mode="stretch_both",
        )
        chart.title.text = metric.title or metric.name

        if metric.eu_limit is not None:
            eu_limit = Span(location=metric.eu_limit, line_color='red', line_dash='dashed', line_width=3)
            chart.add_layout(eu_limit)

        last_week = timezone.now().date() - timedelta(days=7)
        readings = Reading.objects.filter(sensor=sensor, metric=metric, recorded__gte=last_week, hidden=False)
        df = readings.to_dataframe(index='recorded', fieldnames=['value'])
        source = ColumnDataSource(data=df)
        chart.add_glyph(source, line)

        charts.append(chart)

    script, div = components(charts)
    return render(request, "sensors/metrics.html", {"sensor": sensor, "charts": div, "map_js": script})
