from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError

from .nexmo import send_error_text, parse_message
from .models import Message, Number
from .serializers import MessageSerializer

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ValidationError

@csrf_exempt
def webhook(request):
    try:
        serializer = MessageSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        return parse_message(message)
    except IntegrityError:
        return send_error_text(request.GET.get('msisdn'), 'Your message has been sent already')
    except ValidationError as e:
        return send_error_text(request.GET.get('msisdn'), 'Validation Error: {}'.format(str(e)))


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
