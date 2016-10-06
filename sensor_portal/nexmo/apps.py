from django.apps import AppConfig


class NexmoConfig(AppConfig):
    name = 'sensor_portal.nexmo'

    NEXMO_API = {
        'SIGNATURE_SECRET': '',
        'WEBHOOK_SIGNATURE_VALIDATION': False,
        'WEBHOOK_IP_VALIDATION': False,
        'ALLOWED_IPS': [
            '174.37.245.32',
            '174.36.197.192',
            '173.193.199.16',
            '119.81.44.0'
        ]
    }
