from django.conf import settings

# For development purpose it is better to config this on localsettings.
SORL_FRONT_CONFIG_PATH = getattr(settings, "SORL_FRONT_CONFIG_PATH", None)


# Set path to configuration dir here.
#SORL_FRONT_CONFIG_PATH = ''


USE_CELERY = True
