from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView, RedirectView
from django.views.decorators.cache import never_cache


from solr_front.views import *


urls = patterns('',
    (r'^foo/$', TemplateView.as_view(template_name='solr_front/graficos/parallel_coord.html')),

    # Pesquisa
    url(r'^$', never_cache(HomeBuscador.as_view()), name='home' ),
    url(r'^clean_session/(?P<id>\d+)/$',  never_cache(CleanSession.as_view()), name='clean_session'),

    # consulta celery tasks
    url(r'^consulta_pedido/$', AjaxCeleryStatusView.as_view(), name='consulta_pedido'),

    # Colecao principal
    url(r'^(?P<collection>\w+)/(?P<id>\d+)/$',  never_cache(SearchView.as_view()), name='search'),
    url(r'^(?P<collection>\w+)/(?P<id>\d+)/params/$',  never_cache(ParamsView.as_view()), name='params_id' ),

    # Colecoes relacionadas
    url(r'^(?P<collection>\w+)/$',  never_cache(HomeCollection.as_view()), name='home_collection'),
    url(r'^(?P<collection>\w+)/autocomplete/',  never_cache(AutoComplete.as_view()), name='autocomplete'),
        url(r'^(?P<collection>\w+)/(?P<id>\d+)/funil/(?P<collection_destino>\w+)/(?P<hash_querybuilder>\d+)/$', never_cache(AddVerticeView.as_view()), name='funil'),
    url(r'^(?P<collection>\w+)/(?P<id>\d+)/relacionadas/$',  never_cache(RelatedCollection.as_view()), name='colecoes_relacionadas'),
    url(r'^(?P<collection>\w+)/(?P<id>\d+)/totalizadores/$',  TotalizadorView.as_view(), name='totalizadores'),
    url(r'^(?P<collection>\w+)/(?P<id>\d+)/multidimensional_chart/(?P<chart_type>\w+)/$',  MultidimensionalChartView.as_view(), name='multidimensional_chart'),
    url(r'^(?P<collection>\w+)/(?P<id>\d+)/multidimensional_table/(?P<table_type>\w+)/$',  MultidimensionalTableView.as_view(), name='multidimensional_table'),
    url(r'^(?P<collection>\w+)/start_research/$', never_cache(AddVerticeView.as_view()), name='start_research'),

    # Report
    url(r'^(?P<collection>\w+)/(?P<id>\d+)/export_data/$',  ExportDataView.as_view(), name='export_data'),

    # ajax editable
    url(r'^(?P<collection>\w+)/(?P<id>\d+)/params/node_edit$', AjaxVerticeEditFieldView.as_view(), name='node_edit'),
)
