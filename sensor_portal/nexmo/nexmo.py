import nexmo
from datetime import datetime
from django.conf import settings
from sensor_portal.sensors.models import Reading, Metric, Site

def verify_webhook(body):
    if not settings.NEXMO_API['WEBHOOK_SIGNATURE_VALIDATION']:
        return True

    client = nexmo.Client(signature_secret=settings.NEXMO_API.SIGNATURE_SECRET)
    return client.check_signature(body)

def parse_message(body, message):
    data = body.split(',')

    metrics = Metric.objects.all()

    site = Site.objects.get(id=data[0]) #todo: define some magic to make this nicer
    time = datetime.now() #Do magic date parsing for values 2 and 3
    readings = []

    field = 3
    for metric in metrics:
        readings.append(Reading(
            site=site,
            value=float(data[field]),
            message=message,
            metric=metric,
            recorded=time
        )) #can I give it just site?

        field += 1

    Reading.objects.bulk_create(readings)
