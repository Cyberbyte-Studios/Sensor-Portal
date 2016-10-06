from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import Site, Metric, Reading

class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'active')
    search_fields = ('id', 'name', 'position')
    list_filter = ('active',)

class MetricAdmin(OrderedModelAdmin):
    list_display = ('name', 'unit', 'move_up_down_links')

class ReadingAdmin(admin.ModelAdmin):
    date_hierarchy = 'recorded'
    search_fields = ('id', 'site__name', 'metric__name')
    list_filter = ('site', 'metric')
    list_display = ('id', 'metric', 'value', 'recorded')

class ReadingInline(admin.TabularInline):
    model = Reading

admin.site.register(Site, SiteAdmin)
admin.site.register(Metric, MetricAdmin)
admin.site.register(Reading, ReadingAdmin)
