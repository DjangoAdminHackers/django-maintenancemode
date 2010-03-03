from django.conf import settings

MAINTENANCE_MODE = getattr(settings, 'MAINTENANCE_MODE', False)
MAINTENANCE_MODE_ADMIN = getattr(settings, 'MAINTENANCE_MODE_ADMIN', False)
