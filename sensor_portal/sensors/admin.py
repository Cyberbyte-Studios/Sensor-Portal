from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import Sensor, Metric, Reading


class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'active', 'site')
    search_fields = ('id', 'name', 'position', 'site__name')
    list_filter = ('active', 'site')


class MetricAdmin(OrderedModelAdmin):
    list_display = ('name', 'unit', 'move_up_down_links')


class ReadingAdmin(admin.ModelAdmin):
    date_hierarchy = 'recorded'
    search_fields = ('id', 'message__nexmo_id', 'metric__name', 'recorded', 'recorded', 'value', 'sensor__site__name')
    list_filter = ('sensor', 'metric')
    list_display = ('id', 'metric', 'value', 'recorded')


class ReadingInline(admin.TabularInline):
    model = Reading

admin.site.register(Sensor, SensorAdmin)
admin.site.register(Metric, MetricAdmin)
admin.site.register(Reading, ReadingAdmin)
