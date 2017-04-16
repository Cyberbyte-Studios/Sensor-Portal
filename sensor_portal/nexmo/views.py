from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError

from .nexmo import handle_nexmo_error, parse_message
from .serializers import MessageSerializer

from rest_framework.exceptions import ValidationError


@csrf_exempt
def webhook(request):
    try:
        serializer = MessageSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return parse_message(message)

    except IntegrityError:
        return handle_nexmo_error(
            'Your message is already in the database',
            to=request.GET.get('msisdn'),
            message=request.GET.get('text'))

    except ValidationError as e:
        return handle_nexmo_error(
            'Validation Error: {}'.format(str(e)),
            to=request.GET.get('msisdn'),
            message=request.GET.get('text'))
