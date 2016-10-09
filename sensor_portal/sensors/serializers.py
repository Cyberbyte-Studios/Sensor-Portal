from rest_framework import serializers

from sensor_portal.sensors.models import Sensor, Metric, Reading

class SensorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sensor
        fields = ('name', 'position', 'active','description')

class MetricSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Metric
        fields = ('name', 'unit', 'eu_limit', 'description')

class ReadingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Reading
        fields = ('sensor', 'message', 'metric', 'value', 'recorded')
