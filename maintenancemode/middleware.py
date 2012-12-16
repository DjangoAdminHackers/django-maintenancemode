import django
from django.conf import settings
from django.core import urlresolvers

if django.VERSION[:2] <= (1, 3):
    from django.conf.urls import defaults as urls
else:
    from django.conf import urls

urls.handler503 = 'maintenancemode.views.defaults.temporary_unavailable'
urls.__all__.append('handler503')

from maintenancemode.conf.settings import MAINTENANCE_MODE, MAINTENANCE_MODE_ADMIN

class MaintenanceModeMiddleware(object):
    def process_request(self, request):
        # Allow access if middleware is not activated
        if not MAINTENANCE_MODE:
            return None

        # Allow access if remote ip is in INTERNAL_IPS
        if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            pass # TODO I currently don't trust internal IPs with Webfaction's proxying although it could just be a middleware order problem
            #return None
        
        # Allow acess if the user doing the request is logged in and a
        # staff member.
        if hasattr(request, 'user') and request.user.is_staff:
            return None
        
        # Allow admin
        if not MAINTENANCE_MODE_ADMIN and request.META['PATH_INFO'].startswith(urlresolvers.reverse('admin:index')):
            return None

        # Allow specific urls
        allow_urls = getattr(settings, 'MAINTENANCE_MODE_ALLOW_URLS', None)
        if allow_urls:
            for item in allow_urls:
                if request.META['PATH_INFO'].startswith(item):
                    return None

        # Otherwise show the user the 503 page
        resolver = urlresolvers.get_resolver(None)
        
        callback, param_dict = resolver._resolve_special('503')
        return callback(request, **param_dict)