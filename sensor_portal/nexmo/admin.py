from django.contrib import admin
from rleaf_sensor_managment.sensors.admin import ReadingInline
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    inlines = [
        ReadingInline,
    ]

admin.site.register(Message, MessageAdmin)
