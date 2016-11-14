import nexmo
import logging
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
from sensor_portal.sensors.models import Reading, Metric, Sensor
from sensor_portal.nexmo.models import Message


def get_client():
    nexmo_settings = settings.NEXMO_API
    return nexmo.Client(
        key=nexmo_settings['API_KEY'],
        secret=nexmo_settings['API_SECRET'],
        signature_secret=nexmo_settings['SIGNATURE_SECRET']
    )


def verify_webhook(body):
    if settings.NEXMO_API['SIGNATURE_VALIDATION'] is not True:
        return True

    if settings.NEXMO_API['SIGNATURE_SECRET'] is None:
        return True

    client = get_client()
    return client.check_signature(body)


def parse_message(message):
    metrics = Metric.objects.all()
    values = message.text.split(',')

    if len(metrics) == 0:
        return send_error_text(message.msisdn, 'No metrics have been added')

    if len(values) != len(metrics) + 1:
        return send_error_text(message.msisdn, 'You have not provided the right parameters. Here is what you need "{}"'
                               .format(generate_sample_message()))

    index = 0
    readings = []
    sensor = Sensor.objects.get(pk=values[index])

    for metric in metrics:
        index += 1
        readings.append(Reading(
            sensor=sensor,
            message=message,
            metric=metric,
            value=float(values[index]),
            recorded=timezone.now()
        ))

    Reading.objects.bulk_create(readings)
    return HttpResponse('Thanks nexmo :)')


def generate_sample_message():
    metrics = Metric.objects.all()
    sample = 'site,'
    for metric in metrics:
        sample += metric.name + ','
    return sample


def send_error_text(to, text):
    client = get_client()
    logging.info('Message error: {}'.format(text))

    response = client.send_message({
        'from': 'Sensor Hub',
        'to': to,
        'text': text
    })

    response = response['messages'][0]

    if response['status'] == '0':
        logging.info('Sent error text to {} with message {}'.format(to, text))
        if settings.DEBUG:
            return HttpResponse('It did not work: {}'.format(text))
        return HttpResponse('It did not work, I have text back why')

    logging.error('Failed to send error text: {}'.format(response['error-text']))
    return HttpResponse('Something is really broken')
