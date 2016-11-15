# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.template import Context, loader
from django.views.defaults import page_not_found, server_error
from django.http import HttpResponseServerError

from sensor_portal.sensors.views import SensorViewSet, MetricViewSet, ReadingViewSet, sensor_map, metrics, sensor_list, sensor_metrics
from rest_framework import routers

admin.site.site_header = 'Sensor Panel Admin'

router = routers.DefaultRouter()
router.register(r'sensors', SensorViewSet)
router.register(r'metrics', MetricViewSet)
router.register(r'readings', ReadingViewSet)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),

    url(r'^map/$', sensor_map, name='sensor-map'),
    url(r'^sensors/$', sensor_list, name='sensor-list'),
    url(r'^metrics/$', metrics, name='all-metrics'),
    url(r'^metrics/(?P<id>[0-9]+)/$', sensor_metrics, name='sensor-metrics'),

#    url(r'{}/doc/'.format(settings.ADMIN_URL), include('django.contrib.admindocs.urls')).

    # Django Admin, use {% url 'admin:index' %}
    url(r'{}'.format(settings.ADMIN_URL), admin.site.urls),
    url(r'{}django-ses/'.format(settings.ADMIN_URL), include('django_ses.urls')),

    url(r'{}password_reset/$'.format(settings.ADMIN_URL), auth_views.password_reset, name='admin_password_reset'),
    url(r'{}password_reset/done/$'.format(settings.ADMIN_URL), auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # User management
    url(r'^users/', include('sensor_portal.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('allauth_2fa.urls')),

    url(r'^api/v1/', include(router.urls, namespace='v1')),
    url(r'^invitations/', include('invitations.urls', namespace='invitations')),
    url(r'^nexmo/', include('sensor_portal.nexmo.urls', namespace='nexmo')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]

def handler500(request):
    """500 error handler which includes ``request`` in the context.
    :template:`500.html`
    """

    t = loader.get_template('500.html')
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))
