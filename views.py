# -*- coding: utf-8 -*-
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from conf import *

from django.shortcuts import render, render_to_response
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings

from xml.etree import ElementTree as ET

import collections
import datetime
import requests
import textwrap
import hashlib
import locale
import urllib
import json
import sys
import re
import time

import pandas

from solr_front.forms import *
from solr_front.models import *

from solr_front.tasks import update_atomico as update_atomico_celery
from solr_front.tasks import makeCsv as makeCsv_celery
from solr_front.tasks import makeData as makeData_celery

from django.contrib.auth.decorators import login_required

from celery.result import AsyncResult


"""

!!! Sem verificacao de login !!!

"""
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        if not settings.DEBUG:
            return login_required(view)

        return view



# class LoadCollection(object)



class AjaxCeleryStatusView(View):
    def dispatch(self, request, *args, **kwargs):
        task_id = request.GET.get('id')
        if task_id:
            async_result = AsyncResult(task_id)
            if async_result.failed():
                return JsonResponse({'status': -1, 'msg':async_result.traceback})
            else:
                if async_result.ready():
                    return JsonResponse({'status': 1, 'msg':async_result.state})
                else:
                    return JsonResponse({'status': 0, 'msg':async_result.state})
        return JsonResponse({'status': 'undefined', 'msg':'enviar id!'})



class AjaxVerticeEditFieldView(View):
    """
    Recebe os requests ajax para editar o campo de um vertice.
    O pai (EntryPointView) trata o request, recupera resultados no Solr e retorna para o frontend.
    """
    def dispatch(self, request, *args, **kwargs):
        #self.collection =  body_json.keys()[0]
        self.collection =  kwargs['collection']

        self.navigate = NavigateCollection(self.request, self.collection)
        self.vertice = self.navigate.get_vertice(int(kwargs['id']))

        data = self.request.POST

        # recupera field enviado pelo plugin
        field = data['pk']
        # recupera label do field enviado pelo plugin
        label = data['name']

        change = self.navigate.update_vertice_field(field, data['value'], self.vertice['id'])

        navigation_tree = self.navigate.get_navigation_tree()
        if change:
            return JsonResponse(data={'status':'success', 'vertice': self.vertice, 'navigation_tree': navigation_tree })
        else:
            return JsonResponse(data={'status':'error', 'msg':'Erro ao atualizar '+ label +', tente novamente'})




class NavigateCollection(View):
    """
    Manipula a montagem de um caminho no grapho.
    Esta view eh acessada qdo o usuario solicita a visualizacao dos subconjuntos
    de dados de uma segunda collection
    Armazena na sessao.
    """
    def __init__(self, request, collection):
        self.request = request
        self.collection = collection
        self.vertice_inicial = ''
        # self.count_id = 1

        self.idioma = request.resolver_match.kwargs.get('idioma')
        self.id = request.resolver_match.kwargs.get('id')

        if 'navigation' in self.request.session:
            self.vertice_inicial = self.request.session['navigation'].itervalues().next()


    def get_navigation_tree(self):
        """ Retorna arvore de navegacao """

        request = self.request
        if not 'navigation' in request.session:
            return {}

        navigation_tree = []
        def get_rec_navigate_fieds(dict, collection, parent_id):
            my_dict = {'title':dict['title'], 'description':dict['description'], 'label':dict['label'], 'id':dict['id'], 'collection':dict['collection'], 'parent_id':parent_id, 'hash_querybuilder':dict['hash_querybuilder'] }
            navigation_tree.append(my_dict)

            for vertice in dict['tree']:
                # analisa recursivamente os vertices da navegacao.
                get_rec_navigate_fieds(vertice, dict['collection'], dict['id'])

        # Pega na sessao o objeto navigation.
        navigation = request.session['navigation']

        # inicia captura dos fields dos vertices contidos na navegacao.
        get_rec_navigate_fieds(navigation[navigation.keys()[0]], navigation.keys()[0], "null")

        return navigation_tree


    def remove_tree(self, tree, id):
        vertices = []
        for item in tree:
            if item['id'] != id and item['tree']:
                item['tree'] = self.remove_tree(item['tree'], id)
                vertices.append(item)

            elif item.get('id') != id:
                vertices.append(item)
        return vertices

    def count_vertices(self, vertices):
        """ Conta a quantidade de vertices recursivamente """
        return int(hashlib.sha1(str(datetime.now())).hexdigest(), 16) % (10 ** 8)


    def add_vertice(self, collection, pai_id, selected_facets, hash_querybuilder, initial_search, pedido=None):
        """
        Se existe grapho recupera o vertice atual e adiciona um filho.
        Se nao, cria vertice.
        """

        # print '\n\n add_vertice 1'
        # import pdb; pdb.set_trace()


        def set_vertice(collection, hash_id, pai_id, pedido):

            return {'label':COLLECTIONS[collection]['label'],
                    'collection':collection,
                    'pedido': pedido if pedido else '',
                    'body_json': {
                         collection: {
                            'query': 'null',
                            'collection': collection,
                            'selected_facets_col1': selected_facets['qs_selected_facets'],
                            'selected_facets_col2': {},
                         }
                      },
                    'id':hash_id,
                    'parent_id':pai_id,
                    'hash_querybuilder':hash_querybuilder,
                    'tree':[],
                    'initial_search':initial_search,
                        'title': COLLECTIONS[collection]['label'],
                    'description': u'Descrição'
                    }


        if pai_id is not None:
            vertice = self.get_vertice(pai_id)
            hash_id = self.count_vertices(self.vertice_inicial['tree'])
            vertice_filho = set_vertice(collection, hash_id, pai_id, pedido)
            vertice['tree'].append(vertice_filho)

            # print '\n\n add_vertice 2'
            # import pdb; pdb.set_trace()

            return hash_id

        else:
            # If master parent, create a "random" id
            random_id =  int(hashlib.sha1(str(datetime.now())).hexdigest(), 16) % (10 ** 8)
            self.request.session['navigation'] = {}
            self.request.session['navigation'][collection] = set_vertice(collection, random_id, None, pedido)
            # import pdb; pdb.set_trace()
            return random_id # Nova navegacao.



    def get_vertice(self, id):
        """ Localiza recursivamente um vertice especifico """

        if not 'navigation' in self.request.session:
            return

        id = int(id)

        def get_rec_vertice(lista, id):
            for vertice in lista:
                if vertice['id'] == id:
                    return vertice
                if vertice['tree']:
                    rec_vertice = get_rec_vertice(vertice['tree'], id)
                    if rec_vertice:
                        return rec_vertice


        vertice = None
        if self.request.session['navigation'].itervalues().next()['tree']:
            vertice = get_rec_vertice(self.vertice_inicial['tree'], id)

        if vertice:
            return vertice
        else:
            return self.request.session['navigation'].itervalues().next()


    def update_vertice(self, body_json, hash_querybuilder, id, fq, selected_facets, initial_search):
        vertice = self.get_vertice(id)

        if isinstance(vertice['body_json'], dict) and not vertice['body_json'].keys()[0] == self.collection:
            # Se parar aqui eh pq tem erro de navegacao.
            alerta = "Erro de navegação!"
            return render_to_response('solr_front/muda_collection.html', {'alerta': alerta, 'collection':self.collection, 'idioma':'pt'})

        # print '\n\n update_vertice'
        # import pdb; pdb.set_trace()

        vertice['body_json'] = body_json
        vertice['hash_querybuilder'] = hash_querybuilder
        vertice['fq'] = fq
        vertice['selected_facets_col1'] = selected_facets['se_selected_facets']
        vertice['initial_search'] = initial_search


    def remove_vertice(self, id):
        if id == 0:
            if 'navigation' in  self.request.session: del self.request.session['navigation']
        else:

            """
            acertar a recursividade. estah excluindo somente filho do primeiro nivel.
            """
            navigation = self.request.session['navigation']

            # converte navigation em lista
            vertices = []
            if navigation[navigation.keys()[0]]['id'] == id:
                del self.request.session['navigation']
                return True

            for item in navigation[navigation.keys()[0]]['tree']:
                vertices.append(item)
            vertices = self.remove_tree(vertices, id)

            navigation[navigation.keys()[0]]['tree'] = vertices


    def update_vertice_field(self, field, value, id):
        vertice = self.get_vertice(id)
        if isinstance(vertice['body_json'], dict) and not vertice['body_json'].keys()[0] == self.collection:
            # Se parar aqui eh pq tem erro de navegacao.
            return False
        vertice[field] = value
        return True





###################
### View - SOLR ###
###################


class StreamingExpressions(View):
    """
    Esta classe monta Streaming Expressions somente. Ela nao executa requests
    no Solr. Quem faz isso eh a classe SolrQueries.
    """

    def __init__(self, collection, solr_queries):
        """
        Recupera as configuracoes do grapho do arquivo conf.py e inicializa as
        variaveis que serao utilizadas para montar as streaming expressions do Solr.
        """
        self.hash_join = {}
        self.count = {}
        self.top = {}
        self.collection = collection
        self.vertices = BV_GRAPH[self.collection]
        self.edges = EDGES[self.collection]
        self.solr_queries = solr_queries
        # import pdb; pdb.set_trace()


    def get_search(self, collection, fq, selected_facets):
        """
        Monta a expressao de search para um vertice
        Por ora usando para o vertice raiz na exportacao de dados.
        """
        selected_facets = selected_facets.replace('"*"', '*')

        # Limpando sujeiras no mecanismo de facets.
        # Juntar todos os fqs na funcao do solr_queries.
        # if not selected_facets and not fq:
        #     fq2 = ''
        # if fq:
        #     fq = ',fq=' + fq
        # fq2 = fq + ', ' + selected_facets

        search_se = 'search(%s, qt="/export", q=*:*, fl="id", sort="id asc", %s)'
        search_se  = search_se % (collection, selected_facets)

        # import pdb; pdb.set_trace()
        return search_se

        # import pdb; pdb.set_trace()


    def get_join(self, fq, selected_facets, facets_col2):
        """
        Monta a expressao de Join para cada vertice do noh raiz.
        O Join eh a base para se recuperar dados e informacoes agregadas de duas
        collections ligadas.
        """
        edge = self.edges
        facets_col2 = facets_col2.replace('"*"', '*')
        selected_facets = selected_facets.replace('"*"', '*')

        # Limpando sujeiras no mecanismo de facets.
        # Juntar todos os fqs na funcao do solr_queries.
        if not selected_facets and not fq:
            fq2 = ''
        if fq:
            fq = ',fq=' + fq
        fq2 = fq + ', ' + selected_facets


        for v in self.vertices:
            vertice = edge['vertices'][v]

            if vertice['relationship_type'] == 'one_to_many':
                hash_join = """\
                    hashJoin(
                      search(%s, qt="/export",  q=*:*, fl="%s", sort="%s asc" %s),
                      hashed=cartesianProduct(
                        search(%s, qt="/export", q=*:*, fl="%s, id", sort="id asc",  fq=%s:*, %s),
                      %s),
                    on=%s=%s
                    )
                """
                hash_join  = hash_join % (edge['collection'], vertice['one'], vertice['one'], fq2, vertice['collection'], vertice['many'], vertice['many'], facets_col2, vertice['many'], vertice['one'], vertice['many'])
                # hash_join = (textwrap.fill(textwrap.dedent(hash_join))).replace('\n', ' ')
            elif vertice['relationship_type'] == 'many_to_one':
                hash_join = """\
                    hashJoin(
                      search(%s, qt="/export", q=*:*, fl="%s, id", sort="%s asc",  fq=%s:*, %s),
                      hashed=cartesianProduct(
                        select(
                            search(%s, qt="/export",  q=*:*, fl="%s, id", sort="id asc" %s),
                        %s, %s),
                      %s),
                    on=%s=%s
                    )
                """
                hash_join  = hash_join % (vertice['collection'], vertice['one'], vertice['one'], vertice['one'], facets_col2, edge['collection'], vertice['many'], fq2, vertice['many'], 'id as id_2', vertice['many'], vertice['one'],vertice['many'])
                # hash_join = (textwrap.fill(textwrap.dedent(hash_join))).replace('\n', ' ')
            elif vertice['relationship_type'] == 'one_to_one':
                hash_join = """\
                    innerJoin(
                      search(%s, qt="/export", q=*:*, fl="%s", sort="%s asc",  fq=%s:*, %s),
                      search(%s, qt="/export", q=*:*, fl="%s", sort="%s asc" %s),
                      on="%s=%s"
                    )
                """
                hash_join  = hash_join % (edge['collection'], vertice['from_one'], vertice['from_one'], vertice['from_one'], facets_col2, vertice['collection'], vertice['to_one'],  vertice['to_one'], fq2,  vertice['from_one'],  vertice['to_one']  )
                # hash_join = (textwrap.fill(textwrap.dedent(hash_join))).replace('\n', ' ')

            pat = re.compile(r'\n\s+')
            hash_join = pat.sub('', hash_join).lstrip()

            hash_join = hash_join.replace('%', '%25')

            self.hash_join[v] = hash_join # Streaming expression de hashJoin




    def get_count_joined(self, related_collection):
        """ Recupera o valor total de registros joins de duas collections """

        v = related_collection

        self.solr_queries.streaming_expression = self.hash_join[v]
        self.solr_queries.hash_querybuilder = self.solr_queries.create_hash_querybuilder()
        self.count[v] = {'col1':{'value':0, 'se':''}, 'col2':{'value':0, 'se':''}}
        self.count[v]['col2']['label'] = self.edges['vertices'][v]['label']
        self.count[v]['col2']['parent_hash_querybuilder'] = [self.solr_queries.hash_querybuilder]
        vertice =  self.edges['vertices'][v]

        count = 'null(unique(sort( %s, by="%s asc"),over="%s"),sort="%s asc")'

        # Monta SE de contagem com base no SE JOIN
        # Metodo da Classe SolrQueries faz request no Solr e retorna Json.
        # Atribui resultado ao dict de contagem, no valor do vertice
        # Faz isso para col1 e col2


        if vertice['relationship_type'] == 'one_to_many':
            count_sort_field = self.edges['vertices'][v]['many']
            count_col1 = count % (self.hash_join[v], count_sort_field, count_sort_field, count_sort_field )
            count_col2 = count % (self.hash_join[v], 'id', 'id', 'id')

        elif vertice['relationship_type'] == 'many_to_one': # Inverte
            count_sort_field = self.edges['vertices'][v]['many']
            count_col2 = count % (self.hash_join[v], count_sort_field, count_sort_field, count_sort_field )
            count_col1 = count % (self.hash_join[v], 'id_2', 'id_2', 'id_2')

        elif vertice['relationship_type'] == 'one_to_one': # Inverte
            count_sort_field = self.edges['vertices'][v]['from_one']
            count_col2 = count % (self.hash_join[v], count_sort_field, count_sort_field, count_sort_field )
            count_col1 = count % (self.hash_join[v], 'id', 'id', 'id')

        # import pdb; pdb.set_trace()
        #
        ## Tirar as chamadas do solr_queries daqui e passar para o objeto que as usa.
        #
        response_json = self.solr_queries.executaStreamingExpression(count_col1)
        self.count[v]['col1']['value'] = response_json['result-set']['docs'][0]['nullCount']

        response_json = self.solr_queries.executaStreamingExpression(count_col2)
        self.count[v]['col2']['value'] = response_json['result-set']['docs'][0]['nullCount']


    def get_top_joined(self, related_collection):
        """ Recupera os ultimos n registros do join de duas collections """

        vertice = related_collection

        self.top[vertice] = {}

        if self.edges['vertices'][vertice]['relationship_type'] == 'one_to_one':
            top_sort_field = self.edges['vertices'][vertice]['from_one']

        else:
            top_sort_field = self.edges['vertices'][vertice]['many']

        top = 'top(n=3,unique(sort( %s, by="%s asc"),over="%s"),sort="%s asc")'
        top = top % (self.hash_join[vertice], top_sort_field, top_sort_field, top_sort_field )
        response_json = self.solr_queries.executaStreamingExpression(top)
        self.top[vertice]['value'] = response_json['result-set']['docs']
        self.top[vertice]['label'] = self.edges['vertices'][vertice]['label']




class SolrQueries(LoginRequiredMixin, View):
    """
    Encapsula as buscas no Solr
    """
    def __init__(self, collection):
        self.collection = collection

        self.solr_connection = 'http://leydenh/solr/'
        self.server_stream_url = self.solr_connection + self.collection + '/stream?expr='
        self.server_zkhost =  'http://leydenh:9983'
        self.server_qt = '/select'
        self.hash_querybuilder = 0
        self.campo_dinamico_busca = COLLECTIONS[self.collection]['campo_dinamico_busca']


    def executaStreamingExpression(self, se):
        # Se necessario, fazer a conversao html entities geral.
        se = se.replace('%', '%25')
        url = self.server_stream_url + se
        # import pdb; pdb.set_trace()
        response =  requests.get(url).json()
        return response

    def sorlGenericConnection(self, select):
        """ Executa url do Solr a partir do raiz """
        url = self.solr_connection + select
        response =  requests.get(url).json()
        return response

    def sorlJsonQuery(self, data):
        """
        Executa url json do Solr
        """
        solr_url = self.solr_connection + self.collection + '/query'

        # Se necessario, fazer o escape de todos os caracterese que
        solr_url = solr_url.replace('%', '%25')
        try:
            response = requests.post(solr_url, data=data).json()
            return response
        except Exception as e:
            print "\n\n\n"
            print e
            print "1 Nao retornou um JSON valido.\n Eh provavel que o request esteja com problema\n\n\n"





    def facets2query(self, selected_facets):
        """
        Estrutura do Solr antigo, sem o Facets JSON. Solr 4.9.
        Monta uma string para busca de facet via URL e uma string para busca via StreamingExpressions
        """

        """
        Recebe os facets do front e converte para parametro fq do Solr.
        - Se selected_facets for uma lista de um mesmo attributo, considera todos
        adicionando o operador OR.
        - Inclue !tag para nao excluir os resultados filtrados.
        """

        """
        fq_list = []
        for sf in selected_facets:
            for i in selected_facets[sf]:
                facet = sf + ':"' + i + '"'
                fq_list.append(facet)

        import pdb; pdb.set_trace()
        """

        fq_qstring = ''
        se_fqs = ''

        # import pdb; pdb.set_trace()
        # {u'bolsas_pt': [u'01;Bolsas no Brasil'], u'situacao': [u'Em andamento']}

        for sf in selected_facets:
            #categoria = sf.replace('_exact', '')
            categoria = sf
            if len(selected_facets[sf]) > 1:
                # import pdb; pdb.set_trace()
                for i, item in enumerate(selected_facets[sf]):

                    if i: # O primeiro item do enumerate retorna falso
                        fq += 'OR "' + item + '" '
                        #se_fq += ' fq=' + categoria + ':"' + item + '", '
                        se_fq += 'OR "' + item + '" '
                    else: # Primeiro item do enumerate
                        # import pdb; pdb.set_trace()
                        fq = '&fq={!tag=' + categoria + '}'  + categoria + ':( "' + item + '" '
                        #se_fq = ' fq={!tag=' + categoria + '_tag}' + categoria + ':("' + item + '" '
                        se_fq = ' fq=' + categoria + ':(\"' + item + '\" '
                fq += ')'
                se_fq += '),'
                # import pdb; pdb.set_trace()
            elif len(selected_facets[sf]) > 0:
                # import pdb; pdb.set_trace()
                fq = '&fq={!tag=' + categoria + '}' + categoria + ':"' + selected_facets[sf][0] + '"'
                se_fq = ' fq=' + categoria + ':\"' + selected_facets[sf][0] + '\",'
                #se_fq = ' fq=' + categoria + ':"' + selected_facets[sf][0] + '",'
                # import pdb; pdb.set_trace()
            else:
                fq = ''
                se_fq = ''

            if '[' in fq:
                fq = fq.replace('"', '')
                se_fq = se_fq.replace('"', '')

            if '*' in fq:
                fq = fq.replace('"', '')

            fq_qstring += fq
            se_fqs +=  se_fq

            se_fqs = se_fqs.replace('"*"', '*')
            fq_qstring = fq_qstring.replace('"*"', '*')

            # import pdb; pdb.set_trace()

        # import pdb; pdb.set_trace()
        # Retorna dict com facets para a querystring e para a streaming_expression.
        return ({'qs_selected_facets':fq_qstring, 'se_selected_facets':se_fqs})



    def facets2fq_post(self, selected_facets):
        """
        Verificar se eh tudo o que precisa para recuperar os facets do front
        e converter em um unico fq para o Solr.


        !!!! Ver se dah para apgar o metodo acima
        """
        lot = [] # list of tuples
        for key in selected_facets:
            facets = '('
            for item in selected_facets[key]:
                # double quotes bumps Solr.
                item = item.replace('"', '\\"')
                facets += '"' + item + '" OR '

            facets = facets.rstrip(' OR ')
            facets = '{!tag='+ key +'_tag}' + key + ':' + facets + ')'

            if item == '*':
                facets = '{!tag='+ key +'_tag}' + key + ':*'

            lot.append(('fq', facets))
        return lot




    def get_facets_json_api(self):
        """
        Gera string de facet para pegar o resultado facetado na API JSON
        """
        facet_fields = ''
        json_facet = '{'
        for group in COLLECTIONS[self.collection]['facets_categorias']:
            for f in group['facetGroup']:
                for item in f['facets']:
                    json_facet += item['chave'] +':{type:terms, field:'+ item['chave'] + ',limit:-1, domain:{excludeTags:'+ item['chave'] + '_tag}},'
                    facet_fields += '&json.facet={' + item['chave'] +':{type:terms, field:'+ item['chave'] + ',limit:-1, domain:{excludeTags:'+ item['chave'] + '}}}'

        json_facet = json_facet.rstrip(',')
        json_facet += '}'
        return (facet_fields, json_facet)



    def get_facet_4_autocomplete(self, request_get, facet, selected_facets):
        """
        Recupera o facet de um elemento solicitado pelo autocomplete

        json.facet nao tem a opcao de facet.contains
        Voltando para o facet via metodo get.

        json_facet = '{' + request_get['ac_facet_field'] +':{type:terms, prefix:' + fq_split[1] + ', field:'+ request_get['ac_facet_field'] + ',limit:50, domain:{excludeTags:'+ request_get['ac_facet_field'] + '_tag}}}'
        data = [('q','*:*'), ('wt', 'json'), ('rows', 0), ('fl',','), ('json.facet',json_facet)] + fqs + selected_facets
        """

        fqs = []
        fq_split = request_get['fq'].split(':')
        for term in fq_split[1].split():
            fq = fq_split[0] + ':' + term
            fqs.append(('fq', fq))

        solr_url = 'http://leydenh/solr/' + self.collection + '/select?q=*:*&'
        data = [('wt', 'json'), ('rows', 1), ('facet.field', request_get['ac_facet_field']),('facet', 'on'),('facet.contains', fq_split[1]), ('facet.contains.ignoreCase', 'true')] + fqs + selected_facets
        solr_url += urllib.urlencode(data)

        # Se necessario, fazer o escape de todos os caracterese que
        solr_url = solr_url.replace('%', '%25')

        try:
            docs = []
            response = requests.post(solr_url, data=data)
            resultado = response.json()['facet_counts']['facet_fields'][request_get['ac_facet_field']]
            for i,k in zip(resultado[0::2], resultado[1::2]):
                docs.append({'count':k, 'val':i})
            return ({'buckets':docs})
        except Exception as e:
            print "\n\n\n"
            print e
            print "2 Nao retornou um JSON valido.\n Eh provavel que o request esteja com problema\n\n\n"



    def get_facets_json_api_sum(self, sum_field, fq, selected_facets):
        """ Soma todos os valores de um determinado facet """
        sum = '{sum:"sum(' + sum_field + ')"}'
        data = [('q','*:*'), ('fl','*'), ('json.facet',sum)] + selected_facets
        return data


    def get_facets_json_api_avg(self, avg_field, fq, selected_facets):
        """ Retorna a media dos valores numericos de um facet """
        avg = '{avg:"avg(' + avg_field + ')"}'
        data = [('q','*:*'), ('fl',','), ('fq', fq), ('json.facet',avg)] + selected_facets
        return data


    def get_facets_json_api_unique(self, unique_field, fq, selected_facets):
        """ Recupera a qt de valores unicos para um determinado facet """
        se = 'null(unique(search(%s, qt="/export", q=*:*, fl="%s", sort="%s asc", %s),over="%s"),)'
        se  = se % (self.collection, unique_field, unique_field, selected_facets, unique_field)

        result = self.executaStreamingExpression(se)

        if not 'result-set' in result:
            return None

        result = result['result-set']['docs'][0]['nullCount']
        return result


    def create_hash_querybuilder(self):
        """
        Cada busca do querybuilder e os filtros do facet (incluir os facets) teem um
        hash, que eh um campo dinamico criado na collection relacionada.
        Por exemplo, ao buscar publicacoes de processos filtrados, as publicacoes
        passam a ter esse campo, para que esse subconjunto seja identificado e possa
        ser trabalhdo (filtrado).
        """
        return str(int(hashlib.sha1(self.streaming_expression).hexdigest(), 16) % (10 ** 8))






    def update_atomico(self, url, collection2, campo_dinamico_busca):
        """
        @param: url Chamada para o Solr via StreamingExpressions para recuperar o id dos objetos que
        serao indexados (funil).
        @param: collection2 Collection que serah reindexada (funil)
        @param: campo_dinamico_busca Nao estah usando
        Faz update atomico da collection solicitada
        Recebe uma lista e manda de uma vez para o Solr, que cuida fazer o update
        no documento, criando ou excluindo o campo enviando no "jsons_ids".
        """


        def monta_json_para_update(campo, operador):
            """
            :param valor_campo: utilizado para criar ou excluir campo dinamico no Solr
            :type valor_campo: Tipo string. Valores aceitos sao 'true' e vazio
            """

            # Executa o request no Solr e recupera o json de memoria.
            related_collection_json =  requests.get(url).json()

            # import pdb; pdb.set_trace()

            """
            Prepara o uma lista de dict para fazer o update atomico.
            Como o algoritmo map reduce acima retorna publicacoes repetidas, o update
            eh repetido, gerando overhead. Eh preciso melhorar o algoritmo acima de
            map reduce, ou o update.
            """
            json_ids = []
            for doc in related_collection_json['result-set']['docs']:
                if 'id' in doc:
                    json_ids.append({
                        'id':doc['id'],
                        campo:{operador:self.hash_querybuilder}
                    })
            return json_ids

        # Indexa atomicamente (cria campos dinamicos nos documentos enviados em jsons_ids)
        json_ids = monta_json_para_update(campo_dinamico_busca, 'add')

        # Chamar o Celery
        update_url = 'http://leydenh/solr/' + collection2 + '/update?commit=true'
        requests.post(update_url, json=json_ids)


    def get_or_create_related_collection_db(self, collection, streaming_expression):
        """
        Verifica se contagem (count e top) das collections relacionadas
        estao armazenadas no DB.
            1. Sim - retorna para o template mostrar
            2. Nao - contabiliza novamente, armazena e retorna para o template.
        Se nao estiver no banco:
            Contabiliza, armazena e retorna para o template.
        """

        def get_count_get_top(streaming_expression, collection):
            streaming_expression.get_count_joined(collection)
            streaming_expression.get_top_joined(collection)

            count = streaming_expression.count[collection]
            top = streaming_expression.top[collection]
            return (count, top)

        # Se registro jah existe no banco
        try:
            related_collection_chk = RelatedCollectionsCheck.objects.get(hash_querybuilder = self.hash_querybuilder )
            # Se nao precisar recontar, retorna objeto recuperado.
            if not related_collection_chk.recount():
                return related_collection_chk
            # Senao, reconta, grava e retorna objeto atualizado.
            else:
                (count, top) = get_count_get_top(streaming_expression, collection)
                related_collection_chk.join=streaming_expression.hash_join[collection]
                related_collection_chk.qt_col1 = count['col1']['value']
                related_collection_chk.qt_col2 = count['col2']['value']
        # Senao, cria registro no banco.
        except RelatedCollectionsCheck.DoesNotExist:
            print "\n\n\n Does not exist"
            (count, top) = get_count_get_top(streaming_expression, collection)
            related_collection_chk = RelatedCollectionsCheck(hash_querybuilder=self.hash_querybuilder,
                join=streaming_expression.hash_join[collection],
                qt_col1 = count['col1']['value'],
                qt_col2 = count['col2']['value'],
                )
        related_collection_chk.save()
        return related_collection_chk



    def do_reindex(self, se, collection_destino):
        self.streaming_expression = se
        """
        @params: se StreamingExpressions que gera url para recuperar o id dos documentos
        que serao reindexados (funil)
        @params: collection_destino Collection que serah reindexada (funil)

        Abre thread para indexar os documentos relacionados.
        Melhorar essa verificacao pq em muitos casos nao vai haver docs relacionados pelo
        fato de que realmente nao existem docs relacionados para muitas buscas.
        """
        url = "http://leydenh/solr/graph_auxilios/stream?expr=" + se


        # print
        # print collection_destino
        # print self.campo_dinamico_busca
        # print self.hash_querybuilder


        # Metodo deley eh do celery.
        pedido = update_atomico_celery.delay(url, collection_destino, self.campo_dinamico_busca, self.hash_querybuilder)

        # Desta maneira, nao chama no Celery, chama diretamente no script da task.
        #pedido = update_atomico_celery(url, collection_destino, self.campo_dinamico_busca, self.hash_querybuilder)
        # import pdb; pdb.set_trace()
        return pedido





    def get_content(self, content_type, fq, selected_facets):
        facet_fields = self.get_facets_json_api()[1]

        solr_url = 'http://leydenh/solr/' + content_type + '/query'
        data = [('q','*:*'), ('fl','*'), ('fq', fq), ('json.facet',facet_fields)] + selected_facets

        # Se necessario, fazer o escape de todos os caracterese que
        solr_url = solr_url.replace('%', '%25')
        # import pdb; pdb.set_trace()
        try:
            response = requests.post(solr_url, data=data).json()
            return response
        except Exception as e:
            print "\n\n\n"
            print e
            print "2 Nao retornou um JSON valido.\n Eh provavel que o request esteja com problema\n\n\n"




    def get_totalizador(self, content_type, fq, sf, docs):
        fl = ','
        # Transforma o field label no retorno do json do Solr.
        if 'url' in docs and 'text' in docs:
            fl = 'url:' + docs['url'] + ', text:' + docs['text']
        # Limpa os campos que passam a query para o solr, como por exemplo: auxilio:"*"

        sf = sf.replace('"*"', '*')

        if fq:
            fq = 'fq='+fq

        #solr_url = 'http://leydenh/solr/' + content_type + '/query?q=*:*&rows=3&' + fq + sf + '&fl=' + fl

        solr_url = 'http://leydenh/solr/%s/query?q=*:*&rows=3&%s%s&fl=%s' % (str(content_type), fq, sf, fl)


        response = requests.get(solr_url).json()['response']
        return ({'numFound':response['numFound'], 'docs':response['docs']})


    def get_content_json_facet(self, content_type, fq, json_facet, selected_facets):
        """
        Metodo chamado pelo Ajax para montar o grafico multinivel.
        Utilizar a estrutura de facet multinivel do Solr.
        """
        facet_fields = self.get_facets_json_api()[0]
        solr_url = 'http://leydenh/solr/' + content_type + '/query?q=*:*&rows=0&json.facet=' + json_facet + '&fq=' + fq + selected_facets
        resposta = requests.get(solr_url)

        if resposta.status_code != 200:
            raise Exception('Solr error response - grafico multinivel: ', resposta.status_code)
        return resposta



    def get_content_bubble_json_facet(self, content_type, fq, levels_list, selected_facets):
        """
        Recupera dados facetados no Solr e retorna dois objetos para o front end
        para geracao do grafico d3js Bubble.
        """
        solr_url = 'http://leydenh/solr/' + content_type + '/query'


        # import pdb; pdb.set_trace()
        # Recebe as variaveis do grafico.
        json_facet = '{x_axis:{type: terms, field:' +  levels_list[0]['nivel_1'] + ', sort:{count:asc}, limit: -1 , facet:{y_axis:{type: terms,field: ' +  levels_list[1]['nivel_2'] + ',sort:{count:asc},limit: -1}}}}'

        #print json.dumps(resposta.json(), indent=4, sort_keys='true')

        data = [('q','*:*'), ('rows','0'), ('fl','*'), ('fq',fq), ('json.facet', str(json_facet))] + selected_facets
        resposta = requests.post(solr_url, data=data)

        # import pdb; pdb.set_trace()
        try:
            """
            Caso o Solr tenha retornado um json
            """
            resposta_json = []
            x_tick = 0
            for x_elemen in resposta.json()['facets']['x_axis']['buckets']:
                y_tick = 0
                for y_elemen in x_elemen['y_axis']['buckets']:
                    facet = {'name': 'label', 'y_elemen':y_elemen['val'], 'x_elemen':x_elemen['val'], 'count':y_elemen['count'], 'x_tick':x_tick, 'y_tick':y_tick }
                    resposta_json.append(facet)
                    y_tick += 1
                x_tick += 1
            return resposta_json
        except:
            return None



    def get_content_sankey_json_facet(self, content_type, fq, levels_list, selected_facets):
        """
        Recupera dados facetados no Solr e retorna dois objetos para o front end
        para geracao do grafico d3js Sankey.
        """

        json_facet = ''
        for idx, val in enumerate(levels_list):
            nivel = 'nivel_' + str(idx + 1)
            if idx == 0 :
                json_facet = '{"' + nivel + '":{"field":"' +  val[nivel] + '", "type": "terms", "limit": -1'
            else:
                json_facet += ', "facet":{"' + nivel + '":{"field":"' +  val[nivel] + '", "type": "terms", "limit": -1}}'
        json_facet += '}}'
        json_facet = json_facet.replace('\n', '').replace(' ', '')

        solr_url = 'http://leydenh/solr/' + content_type + '/query'
        data = [('q','*:*'), ('rows','0'), ('fl','*'), ('fq',fq), ('json.facet', str(json_facet))] + selected_facets


        resposta = requests.post(solr_url, data=data)
        links = []
        nodes = collections.OrderedDict() # Utiliza dict para facilitar a busca do elemento

        def rec_niveis(source, facets, nivel):
            """
            recupera recursivamente os niveis do facet.
            """


            nivel_str = 'nivel_' + str(nivel)

            if not nivel_str in facets:
                """
                Se nao tem o nivel_str no facet, quer dizer que estah no ultimo nivel e finaliza a recursao.
                """
                return

            for f_dict in facets[nivel_str]['buckets']:
                """
                Itera o objeto e remonta para a estrutura do grafico d3js.
                """
                # Altera o nome da chave para nao haver colisao.
                f_dict['val'] = unicode(f_dict['val']) + '_' + str(nivel)

                if not f_dict['val'] in nodes:
                    nodes[f_dict['val']] = len(nodes)
                if source:
                    # if nodes[source] == nodes[f_dict['val']]:
                    #     continue
                    links.append({'source':nodes[source], 'target':nodes[f_dict['val']], 'value':f_dict['count']})
                rec_nivel = nivel + 1
                rec_niveis(f_dict['val'], f_dict, rec_nivel)

        try:
            """
            Caso o Solr tenha retornado um json, chama funcao recursiva para
            montar a estrutura de dados do grafico sankey.
            """
            resposta_json = resposta.json()
            rec_niveis(0, resposta_json['facets'], 1)
            return (links,  nodes.keys())
        except:
            return None

    def get_content_pivot_table_json_facet(self, content_type, fq, levels_list, selected_facets):
        """
        Recupera dados facetados no Solr e retorna dois objetos para o front end
        para geracao da tabela OLAP.
        """
        json_facet = ''

        for idx, val in enumerate(levels_list):
            nivel = 'nivel_' + str(idx + 1)
            if idx == 0 :
                json_facet = '{"' + nivel + '":{"field":"' +  val[nivel] + '", "type": "terms", "limit": -1'
            else:
                json_facet += ', "facet":{"' + nivel + '":{"field":"' +  val[nivel] + '", "type": "terms", "limit": -1}}'

        json_facet += '}}'

        json_facet = json_facet.replace('\n', '').replace(' ', '')

        solr_url = 'http://leydenh/solr/' + content_type + '/query'
        data = [('q','*:*'), ('rows','0'), ('fl','*'), ('fq',fq), ('json.facet', str(json_facet))] + selected_facets


        resposta = requests.post(solr_url, data=data)
        links = []
        nodes = collections.OrderedDict() # Utiliza dict para facilitar a busca do elemento
        conf = {'rows':['Ano'], 'cols': ['Situação']}

        def rec_niveis(source, facets, nivel):
            """
            recupera recursivamente os niveis do facet.
            """


            nivel_str = 'nivel_' + str(nivel)

            if not nivel_str in facets:
                """
                Se nao tem o nivel_str no facet, quer dizer que estah no ultimo nivel e finaliza a recursao.
                """
                return

            for f_dict in facets[nivel_str]['buckets']:
                """
                Itera o objeto e remonta para a estrutura do grafico d3js.
                """
                # Altera o nome da chave para nao haver colisao.
                f_dict['val'] = unicode(f_dict['val']) + '_' + str(nivel)

                if not f_dict['val'] in nodes:
                    nodes[f_dict['val']] = len(nodes)
                if source:
                    if nodes[source] == nodes[f_dict['val']]:
                        continue
                    # import pdb; pdb.set_trace()

                    links.append({'source':source, 'target':f_dict['val'], 'value':f_dict['count']})
                rec_nivel = nivel + 1
                rec_niveis(f_dict['val'], f_dict, rec_nivel)

        try:
            """
            Caso o Solr tenha retornado um json, chama funcao recursiva para
            montar a estrutura de dados do grafico sankey.
            """
            resposta_json = resposta.json()
            rec_niveis(0, resposta_json['facets'], 1)
            return (links, conf)
        except:
            return None


######################
### EntryPointView ###
######################

class EntryPointView(LoginRequiredMixin, View):
    """
    Classe pai de SearchView, RelatedCollection, #Collection2View e VinculadosView
    Recupera todos os valores do request, trata os dados do json enviados pelo front e
    converte para o formato do Solr.
    """

    model = Pesquisa
    form_class = PesquisaForm


    def get_project_template():
        """
        Verifica se existe template especifico para o projeto, senao usa o default.
        """
        from solr_front import PROJECT_NAME
        return 'base_%s.html' % (PROJECT_NAME)

    template_name = 'solr_front/custom/%s' % (get_project_template())

    try:
        get_template(template_name)
    except TemplateDoesNotExist as e:
        template_name = 'solr_front/default/base_default.html'

    # template_name = 'solr_front/base_spa.html'

    def dispatch(self, request, *args, **kwargs):
        #self.collection =  body_json.keys()[0]
        self.collection =  kwargs['collection']
        self.solr_queries = SolrQueries(self.collection)
        self.hash_querybuilder = self.solr_queries.hash_querybuilder
        self.vertices = BV_GRAPH[self.collection]
        self.body_json = json.loads(request.body)
        self.data = self.body_json[self.collection]
        self.query = self.data['query']

        self.navigate = NavigateCollection(self.request, self.collection)
        self.vertice = self.navigate.get_vertice(int(kwargs['id']))

        # import pdb; pdb.set_trace()
        # Converte os facets do front para a string do Solr.
        self.selected_facets = self.solr_queries.facets2query(self.data['selected_facets_col1'])

        # Caso esse metodo funcione, substituir o acima.
        self.json_selected_facets = self.solr_queries.facets2fq_post(self.data['selected_facets_col1'])

        # Caso tenha uma query, transforma para query do Solr.
        # ALterer o front para sempre mandar esses paramentros vazios.
        self.fq = ''
        if self.query and  not 'null' in self.query:
            (self.fq, ultimo) = self.rec_json('', self.query['rules'], self.query['condition'], 0)
        solr_json = self.json_response()

        try:
            return JsonResponse(solr_json)
        except:
            print "\n\n\n ERRO! Chamando grafico indevidamente."
            print request.path_info
            # Chamando graficos indevidamente. Tratar no front-end.
            raise Exception('JsonResponse: ', solr_json)




    def update_vertice(self):

        initial_search = ''
        if not self.vertice['parent_id']:
            initial_search = self.se.get_search(self.collection, self.fq, self.selected_facets['se_selected_facets'])




        self.navigate.update_vertice(self.body_json, self.solr_queries.hash_querybuilder, int(self.kwargs['id']), self.fq, self.selected_facets, initial_search)




    def split_value(self, value):
        if isinstance(value, int):
            return value
        if ',' in value:
            lego = value.split(',')
            result = ''

            # modifica mecanica de palavras chaves incluindo aspas em cada palavra
            for frase in lego:

                if result == '':
                    result = '"'+frase+'"'
                else:
                    result +=  ' OR ' + '"'+frase+'"'

            value = result
            return '(' + value + ')'
        else:
            return '"' + value + '"'


    def dict_to_solr(self, dict):
        """
        Converte as regras recebidas do frontend em operacoes do Solr.
        Os dicionarios "dict_operators" traduzem os operadores do front em operacoes
        do Solr. Cada operador do dict tem a estrutura correta com placeholders
        que recebem os argumentos e entrega a expressao do Solr pronta.
        Sao 3 dicts, um que espera um argumento, um que espera dois argumentos e
        um que espera 3 argumentos.
        """
        if not dict['value']:
            return self.dict_operators_1[dict['operator']] % (dict['field'])

        # Por enquanto somente para data
        elif isinstance(dict['value'], list):
            #return self.dict_operators_3[dict['operator']] % (dict['field'], dict['value'][0], dict['value'][1])
            return 'data_inicio_ano:[%s TO *] AND data_termino_ano:[%s TO *]' % (dict['value'][0], dict['value'][1])
        else:

            #import pdb; pdb.set_trace()

            dict['value'] = dict['value'].replace('\t', '')

            if dict['field'] == 'data_inicio':
                dict['field'] = 'data_inicio_ano'
            if dict['field'] == 'data_termino':
                dict['field'] = 'data_termino_ano'

            if dict['field'] == 'text':
                dict['value'] = dict['value'].replace('"', '')

            return self.dict_operators_2[dict['operator']] % (dict['field'], self.split_value(dict['value']))


    def rec_json(self, fq, rules, condition, ultimo):
        """
        Recebe json do front com os filtros e converte em um unico parametro fq.
        Essa funcao eh recursiva para interpretar recursivamente a arvore de filtros
        (arquivo json enviado pelo frontend).
        A variavel fq eh concatenada sucessivamente para montar uma expressao logica
        (filtragem a ser passada para o Solr).
        """

        for idx, dict in enumerate(rules):
            if idx == 0:
                fq += '('
            if ultimo:
                fq += condition + ' '
                ultimo = 0

            # Qdo tem somente uma regra, tira da lista e joga no dict.
            if 'rules' in dict and len(dict['rules']) == 1:
                dict = dict['rules'][0]

            if not 'rules' in dict:                     # Se for uma regra, monta a chamada.
                if idx == 0 and idx == len(rules) -1:   # Regra solitaria, sem irmaos
                    fq += self.dict_to_solr(dict) + ') '
                elif idx == len(rules) -1:              # Ultima regra
                    fq += self.dict_to_solr(dict) + ') '
                    return (fq, 1)
                else:                                   # Primeira regra e regras intermediarias
                    fq += self.dict_to_solr(dict) + ' '
            else:                                       # Se for uma lista de regras, chama recursivamente.
                (fq, ultimo) = self.rec_json(fq, dict['rules'], dict['condition'], 0)

                # Se houver mais de um rules o ultimo 'rules', significando que existe no minimo uma
                # indentacao de rules, e o ultimo rules sair, incluir um parenteses no final.
                if len(rules) > 1 and (len(rules) -1 == idx):
                    fq += ') '
            if len(rules) > 1 and not ultimo:
                fq += condition + ' '
        return (fq, ultimo)


    def consolida_totalizador(self, solr_json, generic_json, totalizador):
        """ Metodo utilizado nas classes TotalizadorView e RelatedCollection """
        generic_json['order'] = totalizador['order']
        generic_json['label'] = totalizador['label']
        if 'colunas' in totalizador:
            generic_json['colunas'] = totalizador['colunas']
        if 'type' in totalizador:
            generic_json['type'] = totalizador['type']

        solr_json[totalizador['order']] = generic_json
        return solr_json

    # Dicionario de operadores.
    # Para operacoes com 1, 2 e 3 parametros.
    dict_operators_1 = {'is_empty':'-%s:["" TO *]',
                        'is_not_empty':'%s:["" TO *]',
                    }
    dict_operators_2 = {'equal':'%s:%s',
                        'not_equal':'-%s:%s',
                        'less_or_equal':'%s:[* TO %s]',
                        'greater_or_equal':'%s:[%s TO *]',
                        'contains':'%s:%s',
                        'not_contains':'-%s:%s',
                    }
    dict_operators_3 = {'between':'%s:[%s TO %s]',
                    }






class MultidimensionalTableView(EntryPointView):
    """
    Multidimensional charts endpoint
    """

    def json_response(self):
        # Sankey Chart
        # import pdb; pdb.set_trace()
        if self.kwargs['table_type'] == 'pivot_table' and not 'pivot_table' in COLLECTIONS[self.collection]['omite_secoes']:
            levels_list = self.data['json_levels_list']
            retorno = self.solr_queries.get_content_pivot_table_json_facet(self.collection, self.fq, levels_list , self.json_selected_facets)


            # import pdb; pdb.set_trace()
            if retorno:
                solr_json = {'links': json.dumps(retorno[0]), 'conf': json.dumps(retorno[1])}
                # import pdb; pdb.set_trace()
                return solr_json



class MultidimensionalChartView(EntryPointView):
    """
    Multidimensional charts endpoint
    """

    def json_response(self):
        # Sankey Chart
        if self.kwargs['chart_type'] == 'sankey' and not 'sankey' in COLLECTIONS[self.collection]['omite_secoes']:
            levels_list = self.data['json_levels_list']
            retorno = self.solr_queries.get_content_sankey_json_facet(self.collection, self.fq, levels_list , self.json_selected_facets)
            if retorno:
                solr_json = {'links': json.dumps(retorno[0]), 'nodes': json.dumps(retorno[1])}
                # import pdb; pdb.set_trace()
                return solr_json

        # Bubble Chart
        if self.kwargs['chart_type'] == 'bubble' and not 'bubblechart' in COLLECTIONS[self.collection]['omite_secoes']:
            levels_list = self.data['json_levels_list']
            retorno_list = self.solr_queries.get_content_bubble_json_facet(self.collection, self.fq, levels_list, self.json_selected_facets)
            retorno_list = {'result':retorno_list}
            return retorno_list if retorno_list else None




class SearchView(EntryPointView):
    """
    Ajax get_data chama essa view.
    Recebe os requests de busca aa partir do querybuilder e dos facets.
    O pai (EntryPointView) trata o request, recupera resultados no Solr e retorna para o frontend.
    Atualmente ela filtra o tipo de request, situacao, cx_pesquisa, json_facet.
    Fazer uma URL e uma view para cada.
    """

    def json_response(self):
        """
        Check if vertice has children.
        If true, former query cant be changed. If parents is changed
        the state of the seach tree will be inconsistent.
        """

        # Compare session and request query to verify if changed
        query_session = self.vertice['body_json'].itervalues().next()['query']
        query_request = self.data['query']
        dif_query = cmp(query_session, query_request)

        # Compare session and request selected_facets to verify if changed
        sf_session = self.vertice['body_json'].itervalues().next()['selected_facets_col1']
        sf_request = self.data['selected_facets_col1']
        dif_sf = cmp(sf_session, sf_request)


        if (dif_query or dif_sf) and self.vertice['tree']:
            data = {'message':'<p><strong>Atenção! </strong></p><p> Esta busca possui filhos (funil). <br>'
                        'Não é possível alterar a busca desta collection '
                        'porque isso tornaria a árvore de navegação inconsistente.</p>'
                        '<p>Você pode continuar analisando os resultados desta busca. </p>'
                        '<p>Caso você queira iniciar uma nova busca '
                        'ou alterar a estrutura da árvore de navegação, clique abaixo para iniciar nova navegação. <br> Ou clique no botão voltar para visualizar a busca atual. </p>',
                        'status':409}
            return data

        self.se = StreamingExpressions(self.collection, self.solr_queries)

        if self.vertice['pedido']:
            consulta = 0
            while consulta != 1:
                resultado = self.celery_check(self.vertice)

                #sucesso
                if resultado['status'] == 1:
                    consulta = resultado['status']
                #falhou
                elif resultado['status'] == -1:
                    return {'status': 500, 'message': 'Erro de indexação', 'log': resultado['msg']}
                #em processo
                else:
                    time.sleep(1)

        return self.geraJson()


    """Retorna JSON do solr"""
    def get_solr_json(self):
        # Multilevel chart
        # import pdb; pdb.set_trace()
        if 'json_facet' in self.data and self.data['json_facet'] != '':
            json_facet = json.dumps(self.data['json_facet'])

            solr_json = self.solr_queries.get_content_json_facet(self.collection, self.fq, json_facet , self.selected_facets['qs_selected_facets']).json()
        else: # Main request
            #import pdb; pdb.set_trace()
            solr_json = self.solr_queries.get_content(self.collection, self.fq, self.json_selected_facets)

        # import pdb; pdb.set_trace()
        self.update_vertice()
        return solr_json


    """ Função gera JSON modificado apartir do JSON retornado do solr """
    def geraJson(self, pivot=None):
        # API JSON FACET
        solr_json = self.get_solr_json()
        hierarquia = {}

        for f in solr_json['facets']:
            hierarquia[f] = []
            if f == 'count': continue # ignora item caso chave for count

            if solr_json['facets'][f]['buckets']:
                for bucket in solr_json['facets'][f]['buckets']:
                    hierarquia[f].append({
                        'value' : bucket['val'],
                        'count' : bucket['count']
                    })

        pivot_solr = {}
        def monta_dict(elemento_pai, chave, elemento, count, group_by):
            if not elemento in elemento_pai:
                elemento_pai[elemento] = {
                    'chave':chave,
                    'count':count,
                    'label':elemento,
                    'facets':{},
                    "groupBy":group_by
                }
            return elemento_pai[elemento]['facets']


        #Itera elementos da colection no dict do conf.py
        for group in COLLECTIONS[self.collection]['facets_categorias']:
            for f in group['facetGroup']:
                for item in f['facets']:
                    counter_facets = 0
                    if not item['chave'] in hierarquia or not hierarquia[item['chave']]:
                        continue

                    #if item['chave'] != 'AREAS-DO-CONHECIMENTO-DE-ATUACAO_FACET':
                    #if item['chave'] != 'LIVRE-DOCENCIA':
                    #    continue

                    facet = hierarquia[item['chave']]
                    dict_inicial = {item['chave']: {
                                        'label': item['label'],
                                        'chave': item['chave'],
                                        'facets': {},
                                        'groupBy': group['groupBy'],
                                        'order': counter_facets,
                                        'count': 10
                                        }
                                    }

                    for idx_facet, value in enumerate(facet):
                        # if not 'CIENCIAS_BIOLOGICAS|Química' in value['value']:
                        #     continue
                        # print value

                        dict_ref = dict_inicial[ item['chave'] ]['facets']
                        if '|' in unicode(value['value']):
                            valores = unicode(value['value']).split('|')
                            chave = ''
                            for idx, val in enumerate(valores):
                                if idx == 0:
                                    chave = val
                                else:
                                    chave += '|' + val
                                dict_ref = monta_dict(dict_ref, chave, unicode(val), value['count'], group['groupBy'])
                        else:
                            chave = value['value']
                            monta_dict(dict_ref, chave, unicode(value['value']), value['count'], group['groupBy'])
                    pivot_solr.update(dict_inicial)
                    counter_facets += 1
        solr_json['facet_counts'] = {'hierarquico':pivot_solr}
        return solr_json


    """ função limpa numeros que vem no inciio do texto no padrão 'xx;texto' retornando apenas texto """
    def limpa_label(self,label, parents = None):
        label = str(label)
        #parents é usado para remover duplicatas no label quando repete o mesmo nome do facet pai
        if parents:
            label = label.replace('-', '')
            for parent in parents:
                if ';' in parent and parent[2] == ';':
                    label = label.replace(parent[3:], '')
        if ';' in label and label[2] == ';':
            return label[3:]
        else:
            return label


    def celery_check(self, vertice):
        task_id = vertice['pedido']

        if not self.vertice['hash_querybuilder'] == 0:
            """ Atualiza a data de indexacao da sub-collection """
            sub_collection = RelatedCollectionsCheck.objects.get(hash_querybuilder = self.vertice['hash_querybuilder'])
            sub_collection.indexed_date = datetime.now()
            sub_collection.save()

        async_result = AsyncResult(task_id)
        if async_result.failed():
            return {'status': -1, 'msg':async_result.traceback}
        else:
            if async_result.ready():
                # Armazena modified_date no registro da collection relacionada.
                # self.solr_queries.update_indexed(hash_querybuilder)
                return {'status': 1, 'msg':async_result.state}
            else:
                return {'status': 0, 'msg':async_result.state}


class RelatedCollection(EntryPointView):
    """
    Captura os dados agregados de todas as collections relacionadas no grapho
    da collection principal
    Herda collection do EntryPoint e chama a classe StreamingExpressions, que acessa o
    conf.py com o Grapho e recupera os dados agregados do vertices relacionados.
    Essa View serve duas URLS. A primeira recupera os dados agregados de todas as
    collections do grapho, a segunda recupera somente da collection relacionada solicitada.
    """

    def json_response(self):
        count = {}
        top = {}

        self.se = StreamingExpressions(self.collection, self.solr_queries)
        self.se.get_join(self.fq, self.selected_facets['se_selected_facets'], '')

        related_content = {}

        # Para cada vertice ligada a collection
        for vertice in self.vertices:
            self.solr_queries.streaming_expression = self.se.hash_join[vertice]
            self.solr_queries.hash_querybuilder = self.solr_queries.create_hash_querybuilder()

            # Executa SE para recuperar as qtds de cada collection relacionada (vertice)
            # Se nao houver registro no banco cria.
            # Se houver, verifica a data segunda uma regra no model e atualiza ou nao.
            # ! Isso eh soh para apresentar a quantidade de relacionados.
            # A verificacao da indexacao e indexacao da sub-collection eh feito
            # no AddVerticeView e na SearchView respectivamente.
            related_collection_chk = self.solr_queries.get_or_create_related_collection_db(vertice, self.se)

            count[vertice]={'col2':{'value':related_collection_chk.qt_col2,
                             'label':EDGES[self.collection]['vertices'][vertice]['label'],
                             'parent_hash_querybuilder':related_collection_chk.hash_querybuilder},
                      'col1':{'value':related_collection_chk.qt_col1}}
            totalizadores = COLLECTIONS[vertice]['totalizadores']

            solr_json = {'facet':{}, 'sum':{}, 'unique':{}, 'avg':{}}
            for totalizador in totalizadores:
                if 'facet' in totalizador:
                    selected_facets_col2 = self.solr_queries.facets2query(totalizador['facet'])
                    sum_facets = selected_facets_col2['qs_selected_facets']  + self.selected_facets['qs_selected_facets']
                    docs = totalizador['docs']

                    fq = self.solr_queries.campo_dinamico_busca + ':' + str(related_collection_chk.hash_querybuilder)

                    totalizador_dict = self.solr_queries.get_totalizador(vertice, fq, selected_facets_col2['qs_selected_facets'], docs)
                    solr_json['facet'] = self.consolida_totalizador(solr_json['facet'], totalizador_dict, totalizador)

            related_content[vertice] = solr_json

        self.update_vertice()

            # print "\n\n\n - RelatedCollection"
            # print json.dumps(self.navigate.get_navigation_tree(), sort_keys=True, indent=4)
            # import pdb; pdb.set_trace()

        #   import pdb; pdb.set_trace()
        return {'count':count, 'top':top, 'related_content':related_content}





class TotalizadorView(EntryPointView):
    """
    Recupera a collection para mostrar as respectivas totalizacoes.
    Essa view mostra apenas totalizacoes da propria collection. A totalizacao de relacionados
    eh recuperada na view RelatedCollection.
    """

    def check_data_type(self, totalizador):
        """
        Get defined string as a data type and converts to the refered function
        defined here somewhere.
        """
        if 'data_type' in totalizador:
            possibles = globals().copy()
            possibles.update(locals())
            function = possibles.get(totalizador['data_type'])
            return function


    def json_response(self):
        """
         Os totalizadores tem entradas diferentes mas retornos iguais. Exemplo de retorno:
        {'docs': [], 'numFound': 4260, 'order': 1, 'label': 'Aux\xc3\xadlios - Em andamento'}
        """
        totalizadores = COLLECTIONS[self.collection]['totalizadores']
        solr_json = {'facet':{}, 'sum':{}, 'unique':{}, 'avg':{}}
        for totalizador in totalizadores:
            data_type_fn = self.check_data_type(totalizador)

            if 'facet' in totalizador:
                selected_facets = self.solr_queries.facets2query(totalizador['facet'])
                sum_facets = selected_facets['qs_selected_facets']  + self.selected_facets['qs_selected_facets']
                docs = totalizador['docs']
                totalizador_dict = self.solr_queries.get_totalizador(self.collection, self.fq, sum_facets, docs)
                solr_json['facet'] = self.consolida_totalizador(solr_json['facet'], totalizador_dict, totalizador)
            elif 'sum' in totalizador:
                data = self.solr_queries.get_facets_json_api_sum(totalizador['sum'], self.fq, self.json_selected_facets)
                totalizador_dict = {}
                totalizador_dict['numFound'] = self.solr_queries.sorlJsonQuery(data)['facets']['sum']
                totalizador_dict['numFound'] = totalizador_dict['numFound']
                if data_type_fn:
                    totalizador_dict['numFound'] = data_type_fn(totalizador_dict['numFound'])
                solr_json['sum'] = self.consolida_totalizador(solr_json['sum'], totalizador_dict, totalizador)
            elif 'unique' in totalizador:
                totalizador_dict = {}
                totalizador_dict['numFound'] = self.solr_queries.get_facets_json_api_unique(totalizador['unique'], self.fq, self.selected_facets['se_selected_facets'])
                solr_json['unique'] = self.consolida_totalizador(solr_json['unique'], totalizador_dict, totalizador)
            elif 'avg' in totalizador:
                data = self.solr_queries.get_facets_json_api_avg(totalizador['avg'], self.fq, self.json_selected_facets)
                totalizador_dict = {}
                totalizador_dict['numFound'] = self.solr_queries.sorlJsonQuery(data)['facets']['avg']
                totalizador_dict['numFound'] = totalizador_dict['numFound']
                if data_type_fn:
                    totalizador_dict['numFound'] = data_type_fn(totalizador_dict['numFound'])
                solr_json['avg'] = self.consolida_totalizador(solr_json['avg'], totalizador_dict, totalizador)

        return solr_json








##################
### CreateView ###
##################

class AddVerticeView(CreateView):
    """
    Recebe a collection de destino e um hash_querybuilder.
    Instancia um objeto da classe StreamingExpressions para indexar essa collection
    de destino com os dados do hash_querybuilder.
    Ao final, redireciona o usuario para busca na collection de destino.
    """
    model = Pesquisa
    form_class = PesquisaForm

    def get_project_template():
        """
        Verifica se existe template especifico para o projeto, senao usa o default.
        """
        from solr_front import PROJECT_NAME
        return 'base_%s.html' % (PROJECT_NAME)

    template_name = 'solr_front/custom/%s' % (get_project_template())

    try:
        get_template(template_name)
    except TemplateDoesNotExist as e:
        template_name = 'solr_front/default/base_default.html'

    # template_name = 'solr_front/base_spa.html'

    def dispatch(self, request, *args, **kwargs):
        self.collection =  kwargs['collection']
        self.solr_queries = SolrQueries(self.collection)
        self.se = StreamingExpressions(self.collection, self.solr_queries)
        return super(AddVerticeView, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        if 'collection_destino' in kwargs:
            """ Se for funil, pega vertice pai e adiciona um vertice filho """
            self.navigate = NavigateCollection(self.request, kwargs['collection_destino'])
            parent_vertice = self.navigate.get_vertice(kwargs['id'])
            parent_fq = parent_vertice['fq']

            # import pdb; pdb.set_trace()
            """
            Para indexar somente os documentos que ainda nao foram indexados, para o respectivo campo dinamico
            O campo dinamico identifica todos os relacionados de uma collection a outra.
            Como a base muda, os documentos que nao foram indexados precisam ser. E nao indexa tudo sempre pq eh
            muito custoso.
            """
            # 1 - Primeiro recupera a Streaming Expression
            # def get_join(self, fq, selected_facets, facets_col2):

            self.se.get_join(parent_fq,parent_vertice['selected_facets_col1'], '')
            se = self.se.hash_join[kwargs['collection_destino']]

            # 2 - Configura instancia do solr_queries para pegar o hash_querybuilder
            self.solr_queries.streaming_expression = se
            self.solr_queries.hash_querybuilder = self.solr_queries.create_hash_querybuilder()

            # 3 - Depios gera a Streaming Expression excluindo os documentos que jah estao num_indexados
            # com o respectivo campo.
            exclui_campo_dinamico_busca = 'fq=-' + self.solr_queries.campo_dinamico_busca + ':' + self.solr_queries.hash_querybuilder

            self.se.get_join(parent_fq,parent_vertice['selected_facets_col1'], exclui_campo_dinamico_busca)
            se = self.se.hash_join[kwargs['collection_destino']]

            """
            Sempre (re)indexa a sub-collection. Se na primeira indexacao da sub-collection
            nao indexou tudo, por algum problema no Celery, na proxima indexa somente o que faltou.
            Essa eh uma caracteristica da funcao de indexacao. Ver o do_reindex.
            Se necessario, eh possivel indexar somente uma vez, mas corre-se o risco de
            nao indexar tudo e faltarem registros na sub-collection
            """
            pedido = self.solr_queries.do_reindex(se, kwargs['collection_destino']).id
            self.id = self.navigate.add_vertice( kwargs['collection_destino'], int(kwargs['id']), {'qs_selected_facets':{self.solr_queries.campo_dinamico_busca:[self.solr_queries.hash_querybuilder]}}, self.solr_queries.hash_querybuilder, '', pedido)
            return HttpResponseRedirect(self.get_success_url(self.kwargs['collection_destino']))
        else:
            """ Se for uma nova navegacao, inicializa objeto navigation na sessao """
            # A busca inicial fica na sessao. Os joins de collections ficam em banco.
            initial_search = self.se.get_search(self.collection, '', '')
            self.navigate = NavigateCollection(self.request, self.collection)
            self.id = int(self.navigate.add_vertice(self.collection, None, {'qs_selected_facets':{}}, self.solr_queries.hash_querybuilder, initial_search))
            return HttpResponseRedirect(self.get_success_url(self.collection))

    def get_success_url(self, collection):
        return reverse('params_id',kwargs={'collection':collection, 'idioma':self.kwargs['idioma'], 'id':self.id})











####################
### TemplateView ###
####################

class HomeBuscador(LoginRequiredMixin, TemplateView):
    """
    Home inicial do buscador, que sempre verifica se jah tem pesquisa na sessao.
    """
    def get(self, request, *args, **kwargs):
        erro = {}
        if 'navigation' in self.request.session.keys():
            erro = {'titulo':'Já existe uma pesquisa em andamento',
                'descricao': ''}

        # Get project´s template for the homepage or return default template
        template_name = 'solr_front/custom/%s' % (self.get_project_template())
        try:
            get_template(template_name)
        except TemplateDoesNotExist as e:
            template_name = 'solr_front/default/home_default.html'

        # import pdb; pdb.set_trace()


        return render_to_response(template_name, {'erro': erro, 'idioma':kwargs['idioma'] }, context_instance=RequestContext(self.request))


    def get_project_template(self):
        from solr_front import PROJECT_NAME
        return 'home_%s.html' % (PROJECT_NAME)





class HomeCollection(LoginRequiredMixin, TemplateView):
    """
    Home page da collection.
    Para informacoes a respeito da collection na visao da collection no Grapho,
    nao da instancia de uma busca.
    Utilizar por exemplo como pagina de ajuda, como ela se relaciona com outras
    collectios etc.
    """
    def get(self, request, *args, **kwargs):
            return render_to_response('solr_front/home_collection.html', {'collection':kwargs['collection'], 'idioma':kwargs['idioma']}, context_instance=RequestContext(request))



class AutoComplete(View):
    def get(self, request, *args, **kwargs):
        self.solr_queries = SolrQueries(kwargs['collection'])
        autocomplete = self.solr_queries.get_facet_4_autocomplete(request.GET, 'instituicao_exact', [])
        return JsonResponse(autocomplete)


class ParamsView(LoginRequiredMixin, TemplateView):
    """ Carrega a pagina inicial da pesquisa de uma determinada collection """

    def get_project_template():
        """
        Verifica se existe template especifico para o projeto, senao usa o default.
        """
        from solr_front import PROJECT_NAME
        return 'base_%s.html' % (PROJECT_NAME)

    template_name = 'solr_front/custom/%s' % (get_project_template())

    try:
        get_template(template_name)
    except TemplateDoesNotExist as e:
        template_name = 'solr_front/default/base_default.html'


    def dispatch(self, request, *args, **kwargs):
        """
        Recebe uma collectino e respectivo id.
        Caso não exista este vertice na pesquisa (objeto navigation da sessao), cria.
        Se existir, retorna pagina desse vertice.
        """
        self.collection = kwargs['collection']
        self.id = int(kwargs['id'])
        self.idioma = kwargs['idioma']
        self.navigate = NavigateCollection(self.request, self.collection)
        self.vertice = self.navigate.get_vertice(int(kwargs['id']))

        # import pdb; pdb.set_trace()

        if not self.vertice:
            return redirect(reverse('start_research',kwargs={'collection':self.collection, 'idioma':self.kwargs['idioma']}), permanent=False )
        elif self.vertice['id'] != self.id:
            # import pdb; pdb.set_trace()
            return redirect(reverse('home',kwargs={'idioma':kwargs['idioma']}), permanent=False )



        self.get_context_data()
        return super(ParamsView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(ParamsView, self).get_context_data(**kwargs)
        context['facets_categorias'] = COLLECTIONS[self.collection]['facets_categorias']
        context['omite_secoes'] = COLLECTIONS[self.collection]['omite_secoes']
        # context['documentos'] =   json.dumps(COLLECTIONS[self.collection]['documentos'], ensure_ascii=False ).encode('utf8')
        context['collection'] = self.collection
        # context['vertice'] = json.dumps(self.vertice, ensure_ascii=False ).encode('utf8')

        context['vertice'] = json.dumps(self.vertice)#, ensure_ascii=False ).encode('utf8')

        context['id_collection'] = self.id
        context['collection_label'] = COLLECTIONS[self.collection]['label']
        context['totalizadores'] = json.dumps(COLLECTIONS[self.collection]['totalizadores'])#, ensure_ascii=False ).encode('utf8')
        context['totalizadores_rel'] = json.dumps(self.get_totalizadores_rel())#, ensure_ascii=False ).encode('utf8')


        # context['totalizadores'] = json.dumps(COLLECTIONS[self.collection]['totalizadores'], ensure_ascii=False ).encode('utf8')
        # context['totalizadores_rel'] = json.dumps(self.get_totalizadores_rel(), ensure_ascii=False ).encode('utf8')
        try:
            context['omite_secoes'] = json.dumps(COLLECTIONS[self.collection]['omite_secoes'], ensure_ascii=False ).encode('utf8')
        except:
            context['omite_secoes'] = []


        context['multilevel_barchart_1'] =  ''
        if self.collection in MULTILEVEL_BARCHART_1:
            context['multilevel_barchart_1'] = MULTILEVEL_BARCHART_1[self.collection]

        context['sankey_chart'] =  ''
        if self.collection in SANKEY_CHART:
            context['sankey_chart_json'] = json.dumps(SANKEY_CHART[self.collection])
            context['sankey_chart'] = SANKEY_CHART[self.collection]

        context['pivot_table'] =  ''
        if self.collection in PIVOT_TABLE:
            context['pivot_table_json'] = json.dumps(PIVOT_TABLE[self.collection])
            context['pivot_table'] = PIVOT_TABLE[self.collection]

        context['bubble_chart'] =  ''
        if self.collection in BUBBLE_CHART:
            context['bubble_chart_json'] = json.dumps(BUBBLE_CHART[self.collection])
            context['bubble_chart'] = BUBBLE_CHART[self.collection]



        #envia form para template
        context['form_csv'] = ExportForm()

        context['graph'] = BV_GRAPH[self.collection]


        return context

    def get_totalizadores_rel(self):
        """ Recupera os totalizadores das collections relacionadas """
        totalizadores_rel = []
        for edge in BV_GRAPH[self.collection]:
            totalizadores_rel.append({edge: COLLECTIONS[edge]['totalizadores']})
        return totalizadores_rel



class CleanSession(TemplateView):
    """ Limpa a sessao do usuario """

    def get(self, request, *args, **kwargs):
        self.navigate = NavigateCollection(self.request, '')
        self.navigate.remove_vertice(int(kwargs['id']))
        erro = {}
        return redirect(reverse('home',kwargs={'idioma':kwargs['idioma']}), permanent=False )



class ExportDataView(View):
    """
    Create Report
    If no join is required due to search on the first level only,
    session object has the search query to get data and export.
    If data requested to export comes from a joint search, it is necessary
    to get de join query from database in order to export data.
    """

    def dispatch(self, request, *args, **kwargs):
        self.collection =  self.kwargs['collection']
        self.navigate = NavigateCollection(self.request, self.collection)
        self.vertice = self.navigate.get_vertice(int(self.kwargs['id']))
        self.solr_queries = SolrQueries(self.collection)
        return super(ExportDataView, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        if not self.vertice['parent_id']:
            se = self.vertice['initial_search']
        else:
            navigation = self.navigate.get_navigation_tree()
            # Recupera o id do hash_join para pegar no db o hash_join
            # Com essa streaming expression eh possivel recuperar os dados no Solr.
            hash_querybuilder = navigation[0]["hash_querybuilder"]
            se = RelatedCollectionsCheck.objects.get(hash_querybuilder = hash_querybuilder).join


        #recria form apartir do request
        form = ExportForm(request.GET)


        if form.is_valid():

            self.makeDataFrame(se, form.cleaned_data['name'], form.cleaned_data['email_from'], form.cleaned_data['email_to'],form.cleaned_data['comentario'], form.cleaned_data['formato'] )

            # Return information about the status of report
            # User will receive e-mail with link to download the report.
            data = {'message':'Seu pedido está em processamento e será enviado por e-mail.', 'status': 200}

        else:
            data = {'message':'erro', 'status':500, 'error': form.errors }

        return JsonResponse(data)



    def dict_values_to_string(self, data):

        if isinstance(data, dict):
            final_dict = {}
            for key,value in data.iteritems():
                if isinstance(value, str):
                    final_dict[key] = value
                elif isinstance(value, list):
                    final_dict[key] = ' ,'.join(value)
                elif isinstance(value, dict):
                    final_dict[key] = self.dict_values_to_string(value)
                elif isinstance(value, int):
                    final_dict[key] = int(value)

        elif isinstance(data, list):
            final_list = []
            for dados in data:
                if isinstance(dados, dict):
                    final_dict = {}
                    for key,value in dados.iteritems():
                        if isinstance(value, basestring):
                            if isinstance(value, unicode):
                                final_dict[key] = value
                            else:
                                final_dict[key] = unicode(value, "utf-8")

                        elif isinstance(value, list):
                            valor =' ,'.join(value)
                            if isinstance(valor, unicode):
                                final_dict[key] = valor
                            else:
                                final_dict[key] = unicode(valor, "utf-8")
                        elif isinstance(value, dict):
                            final_dict[key] = self.dict_values_to_string(value)
                        elif isinstance(value, int):
                            final_dict[key] = unicode(str(value), "utf-8")

                else:
                    raise ValueError("Parametro data não é um dict ou lista de dicts")

                final_list.append(final_dict)
        else:
            print 'else'
            raise ValueError("Parametro data não é um dict ou lista de dicts")

        if final_list:
            return final_list
        elif final_dict:
            return final_dict

    def makeDataFrame(self, se, nome, email, para, msg, formato):
        if 'export_fields' in COLLECTIONS[self.vertice['collection']]:
            fields = COLLECTIONS[self.vertice['collection']]['export_fields']


            if 'export_sort_by' in COLLECTIONS[self.vertice['collection']]:
                sort = COLLECTIONS[self.vertice['collection']]['export_sort_by']
            else:
                sort = fields[0] +' asc'

            se = se.replace(', sort="id asc"',', sort="'+sort+'"')
            se = se.replace('fl="id"','fl="'+ ', '.join(fields)+'"')

            if self.limite_itens_export:
                data_list = self.solr_queries.executaStreamingExpression(se)['result-set']['docs'][:self.limite_itens_export]
            else:
                data_list = self.solr_queries.executaStreamingExpression(se)['result-set']['docs']

            data_list = self.dict_values_to_string(data_list)

            #converte para dataframe
            makeData_celery.delay(data_list, nome, email, para, msg, fields, formato)

            return data_list

        else:
            raise ValueError("export_fields nao foi definido na configuracao desta collection")

    def makeCsv(self, se, nome, email, para, msg):
        data_list = self.solr_queries.executaStreamingExpression(se)['result-set']['docs']
        makeCsv_celery.delay(data_list, nome, email, para, msg)

        if 'export_fields' in COLLECTIONS[self.vertice['collection']]:
            fields = COLLECTIONS[self.vertice['collection']]['export_fields']


            if 'export_sort_by' in COLLECTIONS[self.vertice['collection']]:
                sort = COLLECTIONS[self.vertice['collection']]['export_sort_by']
            else:
                sort = fields[0] +' asc'

            se = se.replace(', sort="id asc"',', sort="'+sort+'"')
            se = se.replace('fl="id"','fl="'+ ', '.join(fields)+'"')

            if self.limite_itens_export:
                data_list = self.solr_queries.executaStreamingExpression(se)['result-set']['docs'][:self.limite_itens_export]
            else:
                data_list = self.solr_queries.executaStreamingExpression(se)['result-set']['docs']

            data_list = self.dict_values_to_string(data_list)

            #celery
            # makeCsv_celery.delay(data_list, nome, email, para, msg, fields)
            #local
            makeCsv_celery(data_list, nome, email, para, msg, fields)

        else:
            raise ValueError("export_fields nao foi definido na configuracao desta collection")


    def pos_process(self, data, list_fields_extraction):
        """Metodo utiliza configuração do fields_extraction para extrair valores de data e tratalos com a função especificada"""
        final_data = []
        dict_fields_extraction = self.list_tuple_to_dict(list_fields_extraction)

        for item in data:
            item_data = {}

            for key, value in item.iteritems():

                #se existir no lista de tratamento trata
                #valor usando função especificada, caso não retorna valor original
                if key in fields_extraction:
                    method_to_call = getattr(extractors, dict_fields_extraction[key])
                    item_data[key] = method_to_call(value)
                else:
                    item_data[key] = value

            final_data.append(item_data)


        return final_data


    def list_tuple_to_dict(self, list_tuple):
        dict = {}
        for key,value in list_tuple:
            if value:
                dict[key] = value

        return dict
