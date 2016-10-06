from django.db import models


class Message(models.Model):
    nexmo_id = models.CharField(max_length=16, unique=True)
    to = models.CharField(max_length=12)
    msisdn = models.CharField(max_length=12, verbose_name='sent from')
    text = models.CharField(max_length=140)
    received = models.DateTimeField()

    def __str__(self):
        return str(self.nexmo_id)

