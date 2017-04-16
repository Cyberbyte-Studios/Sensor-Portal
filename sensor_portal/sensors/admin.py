from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import Sensor, Metric, Reading


class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'active', 'site')
    search_fields = ('id', 'name', 'position', 'site__name')
    list_filter = ('active', 'site')


class MetricAdmin(OrderedModelAdmin):
    list_display = ('id', 'name', 'unit', 'move_up_down_links')


class ReadingAdmin(admin.ModelAdmin):
    date_hierarchy = 'recorded'
    search_fields = ('id', 'message__nexmo_id', 'metric__name', 'recorded', 'recorded', 'value', 'sensor__site__name')
    list_filter = ('sensor', 'metric', 'hidden')
    list_display = ('id', 'metric', 'value', 'hidden', 'recorded')
    actions = ['hide', 'show']
    raw_id_fields = ('message',)

    def hide(self, request, queryset):
        rows_updated = queryset.update(hidden=True)
        if rows_updated == 1:
            message_bit = "1 reading was"
        else:
            message_bit = "%s readings were" % rows_updated
        self.message_user(request, "%s successfully hidden." % message_bit)
    hide.short_description = "Hide selected readings"

    def show(self, request, queryset):
        rows_updated = queryset.update(hidden=False)
        if rows_updated == 1:
            message_bit = "1 reading was"
        else:
            message_bit = "%s readings were" % rows_updated
        self.message_user(request, "%s successfully shown." % message_bit)
    show.short_description = "Show selected readings"


class ReadingInline(admin.TabularInline):
    model = Reading

admin.site.register(Sensor, SensorAdmin)
admin.site.register(Metric, MetricAdmin)
admin.site.register(Reading, ReadingAdmin)
