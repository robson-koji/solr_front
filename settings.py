from django.conf import settings


class Settings(object):
    """ Extend project´s settings.py variables """
    def __init__(self):
        import settings
        self.settings = settings
    def __getattr__(self, name):
        return getattr(self.settings, name)


settings = Settings()

TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS = (
    'solr_front.context_processors.get_navigate_fields',
    'solr_front.context_processors.navigation_tree',
    'solr_front.context_processors.settings_vars'
    )
