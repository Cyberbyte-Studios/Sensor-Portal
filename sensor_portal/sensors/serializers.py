from rest_framework import serializers

from sensor_portal.sensors.models import Sensor, Metric, Reading


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('name', 'position', 'active', 'description')


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ('name', 'unit', 'eu_limit', 'description')


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ('sensor', 'metric', 'value', 'recorded')
