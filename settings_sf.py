from django.conf import settings


#
USE_CELERY = False

# Path for custom configuration files
SORL_FRONT_CONFIG_PATH = None

# URL to Solr backend
SOLR_URL = ''

try:
    from local_settings import *
except ImportError as e:
    print "No local_settings.py found"
