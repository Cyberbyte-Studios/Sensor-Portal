from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError

from sensor_portal.sensors.models import Metric, Reading

from .nexmo import verify_webhook, send_error_text, parse_message
from .models import Message, Number
from .serializers import MessageSerializer
import logging

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

@csrf_exempt
def webhook(request):
    try:
        serializer = MessageSerializer(data=request.GET)
        if not serializer.is_valid():
            return send_error_text(request.GET.get('msisdn'), 'Validation Errors: {}'
                                   .format(JSONRenderer().render(serializer.error_messages)))
        message = serializer.save()

        return parse_message(message)
    except IntegrityError:
        return send_error_text(request.GET.get('msisdn'), 'Your message has been sent already')


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
