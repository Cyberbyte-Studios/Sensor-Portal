from django.utils import timezone
from rest_framework import serializers
from .nexmo import send_error_text
from .models import Message, Number
import re


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ('name', 'number')


class MessageSerializer(serializers.Serializer):
    messageId = serializers.CharField(max_length=16)
    to = serializers.IntegerField()
#    to = NumberSerializer()
    msisdn = serializers.CharField(max_length=12)
#    text = serializers.RegexField(r'^[0-9,]*$', max_length=140, min_length=1)
    text = serializers.CharField(max_length=140, min_length=1)
    received = serializers.DateTimeField(default=timezone.now, read_only=True)

    def create(self, validated_data):
#        print (validated_data.get('message-time'))
        return Message.objects.create(
            nexmo_id=validated_data.get('messageId'),
            to=validated_data.get('to'),
            msisdn=validated_data.get('msisdn'),
            text=validated_data.get('text'),
#            received=validated_data.get('message-timestamp'),
            received=timezone.now(),
        )

    def validate_to(self, value):
        try:
            return Number.objects.get(number=value)
        except Number.DoesNotExist:
            raise serializers.ValidationError('Sent to number not found')

    def validate_text(self, value):
        if re.match("^[0-9,]*$", value):
            return value
        raise serializers.ValidationError('Message text is not in the allowed format')
