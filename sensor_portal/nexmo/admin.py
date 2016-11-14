from django.contrib import admin
from sensor_portal.sensors.admin import ReadingInline
from .models import Message, Number


class MessageAdmin(admin.ModelAdmin):
    date_hierarchy = 'received'
    search_fileds = ('nexmo_id', 'text', 'received')
    list_filter = ('to',)
    list_display = ('nexmo_id', 'text', 'received')
    inlines = [
        ReadingInline,
    ]

admin.site.register(Message, MessageAdmin)
admin.site.register(Number)
