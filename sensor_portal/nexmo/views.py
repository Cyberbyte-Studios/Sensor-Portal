from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from sensor_portal.sensors.models import Metric, Reading

from .nexmo import verify_webhook
from .models import Message, Number


@csrf_exempt
def webhook(request):
    # if not verify_webhook(request):
    #     return HttpResponse('403 error')

    number = Number.objects.get(number=request.GET.get('to'))

    message = Message(
        nexmo_id=request.GET.get('messageId'),
        to=number,
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

    metrics = Metric.objects.all()
    values = message.text.split(',')

    if len(values) != len(metrics) + 1:
        return HttpResponse('There are not enough values in that text...')

    index = 0
    readings = []
    sensor = Sensor.object.get(pk=values[index])

    for metric in metrics:
        readings.append(Reading(
            sensor = sensor,
            message = message,
            metric = metric,
            value = values[index],
        ))
        index += 1

    print(readings)
    Reading.objects.bulk_create(readings)

    return HttpResponse('Thanks Nexmo :)')

