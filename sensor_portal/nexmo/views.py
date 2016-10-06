from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .nexmo import verify_webhook
from .models import Message


@csrf_exempt
def webhook(request):
    # if not verify_webhook(request):
    #     return HttpResponse('403 error')

    message = Message(
        nexmo_id=request.GET.get('messageId'),
        to=request.GET.get('to'),
        msisdn=request.GET.get('msisdn'),
        text=request.GET.get('text'),
        received=request.GET.get('message-timestamp'),
    )

    try:
        message.full_clean()
    except ValidationError as e:
        print(e)
        return HttpResponse('Invalid Request')

    message.save()

    return HttpResponse('Thanks Nexmo :)')

