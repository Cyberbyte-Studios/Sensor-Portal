import re

from django.utils import timezone
from rest_framework import serializers
from .models import Message, Number


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ('name', 'number')


class MessageSerializer(serializers.Serializer):
    messageId = serializers.CharField(max_length=16)
    to = serializers.IntegerField()
    msisdn = serializers.CharField(max_length=12)
    text = serializers.CharField(max_length=140, min_length=1)
    received = serializers.DateTimeField(default=timezone.now, read_only=True)

    def create(self, validated_data):
        return Message.objects.create(
            nexmo_id=validated_data.get('messageId'),
            to=validated_data.get('to'),
            msisdn=validated_data.get('msisdn'),
            text=validated_data.get('text'),
            received=timezone.now(),
        )

    def validate_to(self, value):
        try:
            return Number.objects.get(number=value)
        except Number.DoesNotExist:
            raise serializers.ValidationError('Sent to number not found')

    def validate_text(self, value):
        if re.match("^[0-9,.]*$", value):
            return value
        raise serializers.ValidationError('Message text contains invalid chars. Allowed: 0-9,.')
