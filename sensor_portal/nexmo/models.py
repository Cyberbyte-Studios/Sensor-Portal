from django.db import models


class Number(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class Message(models.Model):
    nexmo_id = models.CharField(max_length=16, unique=True)
    to = models.ForeignKey(Number, on_delete=models.CASCADE)
    msisdn = models.CharField(max_length=12, verbose_name='sent from')
    text = models.CharField(max_length=140)
    received = models.DateTimeField()

    def __str__(self):
        return str(self.nexmo_id)
