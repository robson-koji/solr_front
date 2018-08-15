from django.conf.urls import include, patterns, url
import os

PROJECT_PATH = os.path.realpath(
        os.path.dirname(
            os.path.dirname(__file__)
            )
        )

#path de paginas do Sphinks Docs
DOCS_ROOT = os.path.join(PROJECT_PATH, 'docs/_build/html')
JSDOCS_ROOT = os.path.join(PROJECT_PATH, 'docs/jsdocs/build')

urls = []
#inclui JSDOC no projeto
urls += patterns('',
    url(r'^js/$', 'django.views.static.serve',
    {
    'document_root': JSDOCS_ROOT,
    'path': 'index.html'
    }),

    url(r'^js/(?P<path>.*)$', 'django.views.static.serve',
    {
    'document_root': JSDOCS_ROOT
    })
)
#inclui sphinks no projeto
urls += patterns('',
    url(r'^$', 'django.views.static.serve',
     {
        'document_root': DOCS_ROOT,
        'path': 'index.html'
    }),

    url(r'^(?P<path>.*)$', 'django.views.static.serve',
     {
         'document_root': DOCS_ROOT
     }),
 )
