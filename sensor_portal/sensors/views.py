from django.shortcuts import render_to_response
from chartit import DataPool, Chart

from .models import Reading


def index(request):
    chart_data = DataPool(series=[
        {'options': {'source': Reading.objects.all()}, 'terms': ['recorded', 'value']}
    ])
    cht = Chart(datasource=chart_data, series_options=[
        {'options': {'type': 'line', 'stacking': False}, 'terms': {'recorded': ['value']}}],
                chart_options={'title': {'text': 'Readings'},
                               'xAxis': {'title': {'text': 'Month number'}}})
    return render_to_response('dashboard/index.html', {'weatherchart': cht})
