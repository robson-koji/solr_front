# -*- coding: utf-8 -*-


def generate_edges(graph):
    """ Lista todos os nohs do grapho """
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))
    return edges


BV_GRAPH = {
            "graph_auxilios": ["bv_memoria", "graph_auxilios", "bv_empresas", "bv_pesquisadores"],
            #"graph_auxilios": ["bv_pesquisadores"],
            "bv_memoria": ["memoria_autoria"],
            "bv_empresas": ["graph_auxilios"],
            "bv_pesquisadores": ["graph_auxilios", "lattes"],
            "memoria_autoria": [],
            "pesquisa_pipe": ["graph_auxilios"],
            "inep_docentes": [],
            "inep_alunos": [],
            "fazenda_sp": [],
            "rais": [],
            "lattes": [],
            "wos": [],
            "enade": [],
            }

# Vertices


"""
Collection definition template.

'< collection >':{
    # 'django_ct':'geral.pesquisador',
    'label': '< > ',
    'omite_secoes':['refine', 'sankey'], # Caso nao queira uma determinada secao no buscador.

    'campo_dinamico_busca':'cross_collection_< collection name >',
    'id_index_from':'< field from this collection >',
    'id_index_to':'< field of another collection >',
    'facets_categorias':[
        {'groupBy':{'id':' < > ', 'label':' < > ','order':1},
        'facetGroup':[
            {'label':' < >' , 'render':'barChart_1', 'facets':[{'chave':' < > ', 'label': ' < > '}]},
        ]},


    ],
    'totalizadores':[
        {'label':'' , 'facet':{'*':["*"]}, 'docs':{'':'', 'text':'snipet'}, 'type':['doc'],  'colunas': 12, 'order':1},
        {'label':'' , 'sum':'', 'order':2, 'docs':{}, 'type':['main']},
        {'label':'' , 'unique':'', 'order':3, 'docs':{}, 'type':['main']},

    ],
},
"""
COLLECTIONS = {

    'graph_auxilios': {
        'omite_secoes': ['refine', 'sankey', 'bubblechart'],
        'django_ct': 'projetos.projeto OR bolsas.bolsa',
        'label': u'Projetos (Auxílios e Bolsas)',
        'campo_dinamico_busca': 'cross_collection_auxilios',
        # Qdo acertar a indexacao esse campo pode sumir e usar a chave do dict.
        'facets_categorias': [
            {'groupBy': {'id': 'projetos', 'label': 'Projetos', 'order': 0},
             'facetGroup': [
                 {'label': 'Situação', 'render': 'halfPieChart',
                  'facets': [{'chave': 'situacao', 'label': 'Situação'}]},
                 # , 'situacao_en_exact']},
                 {'label': 'Bolsas', 'render': 'halfPieChart', 'facets': [{'chave': 'bolsas_pt', 'label': 'Bolsas'}]},
                 # , 'situacao_en_exact']},
                 {'label': 'Auxilios', 'render': 'barChart_1',
                  'facets': [{'chave': 'auxilio_pesquisa_pt', 'label': 'Auxílios a Pesquisa'}]},
                 # , 'situacao_en_exact']},
             ]},
            {'groupBy': {'id': 'area', 'label': 'Área', 'order': 1},
             'facetGroup': [
                 {'label': 'Área do conhecimento', 'render': 'barChart_1',
                  'facets': [{'chave': 'area_pt', 'label': 'Área do conhecimento'}]},
                 # 'area_conhecimento_exact', 'area_exact''area_conhecimento_en_exact']},
                 {'label': 'Instituição-Sede', 'render': 'barChart_1',
                  'facets': [{'chave': 'entidade_exact', 'label': 'Entidade'}]},
                 # ,'sigla_instituicao_exact',  'unidade_exact' 'sigla_unidade_exact','instituicao_exact', 'id_instituicao_sede_exact',]},
             ]},
            {'groupBy': {'id': 'acordos', 'label': 'Acordos e Convênios', 'order': 2},
             'facetGroup': [
                 {'label': 'Convênios e Acordos', 'render': 'barChart_1',
                  'facets': [{'chave': 'tipo_convenio_exact', 'label': 'Tipo de convenio'},
                             {'chave': 'convenio_exact', 'label': 'Convenio'},
                             {'chave': 'pais_convenio_exact', 'label': 'País de convenio'}]},
             ]},
            {'groupBy': {'id': 'geolocalizacao', 'label': 'Geolocalização', 'order': 4},
             # {'label':'Resultados dos projetos' , 'render':'resultados', 'facets':[{'chave':'publicacoes_cientificas_exact','label':'Publicações cientificas'},{'chave': 'publicacoes_academicas_exact','label': 'Publicações academicas'}, {'chave':'materias_agencia_exact','label':'Materias da agencia'}, {'chave':'materias_revista_exact', 'label':'Materias da revista' }]},
             'facetGroup': [
                 {'label': 'Geolocalização Exterior', 'render': 'barChart_1', 'facets': [
                     # {'chave':'cidade_exterior_lat_lon_exact','label':'Cidades no exterior'}, {'chave':'conexao_cidade_sp_exterior_exact','label':'Conexões da cidade de sp com exterior'},{'chave':'pais_exterior_lat_lon_exact','label':'País no exterior'}, {'chave':'conexao_pais_sp_exterior_exact', 'label':'Conexao do pais com exterior'},
                     {'chave': 'pais_colaboracao_exact', 'label': 'Colaboração no país'},
                     {'chave': 'cidade_colaboracao_exact', 'label': 'Colaboração na cidade'},
                     {'chave': 'instituicao_colaboracao_exact', 'label': 'Colaboração em instituição'},
                     {'chave': 'cidade_exact', 'label': 'Cidade de origem'}]},
                 # {'chave': 'cidade_lat_lon_exact','label':'Cidade Latitude Longitude '},
             ]},
            {'groupBy': {'id': 'temporal', 'label': 'Série Temporal', 'order': 5},
             'facetGroup': [
                 {'label': 'Série Temporal', 'render': '',
                  'facets': [{'chave': 'ano_inicio', 'label': 'Ano de início'}]},
                 # {'chave':'data_termino_mes_exact','label':'Mês de término'}, {'chave':'data_inicio_ano_exact','label':'Ano de inicio'}, {'chave':'data_termino_ano_exact','label':'Ano de termino'}, {'chave':'ano_exact','label':'Ano'}]},
             ]},

            # duplicado existe no grupo Area
            # {'groupBy':{'id':'inst', 'label':'Instituição','order':5},
            # 'facetGroup':[
            #     {'label':'Instituição-Sede' , 'render':'instituicao',  'facets':[{'chave':'entidade_exact','label':'Entidade'}]},#,'sigla_instituicao_exact',  'unidade_exact' 'sigla_unidade_exact','instituicao_exact', 'id_instituicao_sede_exact',]},
            # ]},
            {'groupBy': {'id': 'prog', 'label': 'Programas', 'order': 3},
             'facetGroup': [
                 {'label': 'Programas', 'facets': [{'chave': 'programa_tema_pt', 'label': 'Por tema'},
                                                   {'chave': 'programa_aplicacao_pt', 'label': 'Aplicação'},
                                                   {'chave': 'programa_percepcao_pt', 'label': 'Percepção'},
                                                   {'chave': 'programa_infra_pt', 'label': 'Infra'}]},
             ]},

        ],

        'totalizadores': [
            {'label': 'Total de Projetos', 'facet': {'auxilio': ["*"]}, 'docs': {}, 'type': ['main'], 'order': 1},
            # {'label':'Total de Projetos em Andamentos' , 'facet':{'situacao_exact':["Em andamento"]}, 'docs':{}, 'type':['main'], 'order':1},
            {'label': 'Bolsas no Brasil - Em andamento',
             'facet': {'fomento': ['Bolsas*no*Brasil*'], 'situacao': ["Em andamento"]},
             'docs': {'url': 'absolute_url_pt_t', 'text': 'titulo_pt_t'}, 'type': ['doc', 'main'], 'order': 13},
            {'label': 'Bolsas no Brasil - Concluídas',
             'facet': {'fomento': ['Bolsas*no*Brasil*'], 'situacao': ["Concluídos"]},
             'docs': {'url': 'absolute_url_pt_t', 'text': 'titulo_pt_t'}, 'type': ['doc', 'main'], 'order': 14},
            {'label': 'Bolsas no Exterior - Em andamento',
             'facet': {'fomento': ["Bolsas*no*Exterior*"], 'situacao': ["Em andamento"]},
             'docs': {'url': 'absolute_url_pt_t', 'text': 'titulo_pt_t'}, 'type': ['doc', 'main'], 'order': 15},
            {'label': 'Bolsas no Exterior - Concluídas',
             'facet': {'fomento': ["Bolsas*no*Exterior*"], 'situacao': ["Concluídos"]},
             'docs': {'url': 'absolute_url_pt_t', 'text': 'titulo_pt_t'}, 'type': ['doc', 'main'], 'order': 16},
            {'label': 'Auxílios - Em andamento', 'facet': {'auxilio': ["*"], 'situacao': ["Em andamento"]},
             'docs': {'url': 'absolute_url_pt_t', 'text': 'titulo_pt_t'}, 'type': ['doc', 'main'], 'order': 11},
            {'label': 'Auxílios - Concluídos', 'facet': {'auxilio': ["*"], 'situacao': ["Concluídos"]},
             'docs': {'url': 'absolute_url_pt_t', 'text': 'titulo_pt_t'}, 'type': ['doc', 'main'], 'order': 12},

            {'label': 'Com Publicações Científicas', 'facet': {'publicacoes_cientificas_exact': ["Sim"]}, 'docs': {},
             'type': ['secondary'], 'order': 2},
            {'label': 'Com Publicações Acadêmicas', 'facet': {'publicacoes_academicas_exact': ["Sim"]}, 'docs': {},
             'type': ['secondary'], 'order': 3},
            {'label': 'Com Matéria na Revista FAPESP', 'facet': {'materias_revista_exact': ["Sim"]}, 'docs': {},
             'type': ['secondary'], 'order': 4},
            {'label': 'Com Matéria na Agência FAPESP', 'facet': {'materias_agencia_exact': ["Sim"]}, 'docs': {},
             'type': ['secondary'], 'order': 5},

        ],
    },
    'bv_memoria': {
        'omite_secoes': ['busca', 'refine', 'sankey', 'bubble'],
        'django_ct': 'memoria.serie_periodica',
        'label': 'Publicações científicas',
        'campo_dinamico_busca': 'cross_collection_memoria',
        'facets_categorias': [
            {'groupBy': {'id': 'class', 'label': 'Classificação', 'order': 1},
             'facetGroup': [
                 {'label': 'Ano de publicacao', 'render': '',
                  'facets': [{'chave': 'ano_publicacao', 'label': 'Ano de publicacao'}]},
                 {'label': 'Revista', 'render': 'barChart_1', 'facets': [{'chave': 'revista', 'label': 'Revistas'}]}
             ]},
            {'groupBy': {'id': 'area', 'label': 'Área', 'order': 2},
             'facetGroup': [
                 {'label': 'Área do conhecimento', 'render': 'barChart_1',
                  'facets': [{'chave': 'area_pt', 'label': 'Área do conhecimento'}]},
                 # 'area_conhecimento_exact', 'area_exact''area_conhecimento_en_exact']},
             ]},
            {'groupBy': {'id': 'fomento', 'label': 'Linha de fomento', 'order': 3},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'auxilio_pesquisa_pt', 'label': 'Auxílios'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'bolsas_pt', 'label': 'Bolsas'}]},
             ]},
        ],
        'totalizadores': [
            {'label': 'Publicações Científicas - Com link interno', 'facet': {'absolute_url_pt_t': ["*"]},
             'docs': {'url': 'absolute_url_pt_t', 'text': 'referencia'}, 'type': ['doc', 'main'], 'colunas': 12,
             'order': 1},
            {'label': 'Citações', 'sum': 'numero_citacoes', 'order': 2, 'docs': {}, 'type': ['main']},
            {'label': 'Revistas', 'unique': 'revista', 'order': 3, 'docs': {}, 'type': ['main']},
        ],
    },
    'memoria_autoria': {
        'omite_secoes': ['documentos', 'busca', 'refine', 'sankey'],
        # Caso nao queira uma determinada secao no buscador.

        'django_ct': 'memoria.serie_periodica',
        'label': 'Autores de Publicações Científicas',
        'campo_dinamico_busca': 'cross_collection_memoria_autoria',
        'facets_categorias': [
            {'groupBy': {'id': 'class', 'label': 'Classificação', 'order': 1},
             'facetGroup': [
                 {'label': 'Instituição', 'render': 'datas',
                  'facets': [{'chave': 'instituicao_list_exact', 'label': 'Instituição do Autor'}]},
                 {'label': 'País', 'render': 'barChart_1',
                  'facets': [{'chave': 'pais_list_exact', 'label': 'País da Instituição'}]},
                 {'label': 'Autor', 'render': 'barChart_1', 'facets': [{'chave': 'autor_exact', 'label': 'Autores'}]},
             ],
             }],
        'totalizadores': [
            {'label': 'Autores com Instituição definida', 'facet': {'instituicao_list': ["*"]},
             'docs': {'url': '""', 'text': 'snipet'}, 'type': ['doc', 'main'], 'order': 1},
            {'label': 'Autores sem Instituição definida', 'facet': {'-instituicao_list': ["*"]},
             'docs': {'url': '""', 'text': 'autor'}, 'type': ['doc', 'main'], 'order': 2},
        ],
    },

    'bv_empresas': {
        'django_ct': 'empresas.empresa',
        'label': 'Empresas do PIPE',
        'omite_secoes': ['outros_indicadores', 'busca', 'refine', 'sankey'],
        # Caso nao queira uma determinada secao no buscador.

        'campo_dinamico_busca': 'cross_collection_bv_empresas',
        'facets_categorias': [
            {'groupBy': {'id': 'class', 'label': 'Classificação', 'order': 0},
             'facetGroup': [
                 {'label': 'Município', 'render': 'barChart_1',
                  'facets': [{'chave': 'municipio_cpd', 'label': 'Município'}]},
                 {'label': 'CNAE', 'render': 'barChart_1', 'facets': [{'chave': 'lista_cnae', 'label': 'CNAE'}]},
             ]},
            {'groupBy': {'id': 'temporal', 'label': 'Temporal', 'order': 1},
             'facetGroup': [
                 {'label': 'Acumulado por ano de entrada no Programa PIPE', 'render': 'barChart_1',
                  'facets': [{'chave': 'ano_primeiro_processo', 'label': 'Entrada no programa PIPE'}]}
             ]}
        ],
        'totalizadores': [
            {'label': 'Empresas com Projetos PIPE apoiados', 'facet': {'quantidade_projetos': ['[1 TO *]']},
             'docs': {'url': 'absolute_url_pt_t', 'text': 'razao_social'}, 'type': ['doc', 'main'], 'order': 2},
            {'label': 'Empresa sem Projetos', 'facet': {'quantidade_projetos': ["0"]}, 'docs': {}, 'type': ['main'],
             'order': 3},
            {'label': 'Total de Empresas ', 'facet': {'*': ["*"]}, 'docs': {}, 'type': ['main'], 'order': 1},
        ],
    },
    'bv_pesquisadores': {
        'django_ct': 'geral.pesquisador',
        'label': 'Pesquisadores FAPESP',
        'omite_secoes': ['refine', 'sankey', 'bubblechart'],  # Caso nao queira uma determinada secao no buscador.

        'campo_dinamico_busca': 'cross_collection_bv_pesquisadores',
        'id_index_from': 'id_pesquisador',
        'id_index_to': 'django_id',
        'facets_categorias': [
            {'groupBy': {'id': 'Gerais', 'label': 'Instituição', 'order': 1},
             'facetGroup': [
                 {'label': 'Instituição de afiliação', 'render': 'barChart_1',
                  'facets': [{'chave': 'instituicao_afiliacao_exact', 'label': 'Instituição de afiliação'}]},
                 {'label': 'Quantidade de Processos', 'render': 'barChart_1',
                  'facets': [{'chave': 'quantidade_processos', 'label': 'Quantidade de Processos'}]},
             ]},
            {'groupBy': {'id': 'Pesquisador', 'label': 'Gênero', 'order': 1},
             'facetGroup': [
                 {'label': 'Gênero', 'render': 'barChart_1', 'facets': [{'chave': 'sexo', 'label': 'Gênero'}]},
                 {'label': 'Nacionalidade (País)', 'render': 'barChart_1',
                  'facets': [{'chave': 'nacionalidade', 'label': 'Nacionalidade (País)'}]},
             ]},

        ],
        'totalizadores': [

            {'label': 'Pesquisadores (Beneficiário e/ou responsável)', 'facet': {'*': ["*"]},
             'docs': {'url': 'url_pt', 'text': 'snipet'}, 'type': ['doc'], 'colunas': 12, 'order': 0},
            #
            {'label': 'Com CV Lattes', 'facet': {'cv_lattes': ["*"]}, 'docs': {}, 'type': ['main'], 'order': 1},
            {'label': 'Com Researcher ID', 'facet': {'researcherid': ["*"]}, 'docs': {}, 'type': ['main'], 'order': 3},
            {'label': 'Com Google Citations', 'facet': {'google_citations': ["*"]}, 'docs': {}, 'type': ['main'],
             'order': 4},
            {'label': 'Com ORCID', 'facet': {'orcid': ["*"]}, 'docs': {}, 'type': ['main'], 'order': 2},
        ],
    },

    'pesquisa_pipe': {
        # 'django_ct':'geral.pesquisador',
        'label': 'Pesquisa PIPE 2017',
        'campo_dinamico_busca': 'cross_collection_pesquisa_pipe',
        'omite_secoes': ['documentos', 'outros_indicadores', 'busca', 'refine'],
        # Caso nao queira uma determinada secao no buscador.
        # 'id_index_from':'id_pesquisador',
        # 'id_index_to':'django_id',
        'facets_categorias': [
            {'groupBy': {'id': 'preenchimento', 'label': 'Etapas preenchidas', 'order': 0},
             'facetGroup': [
                 {'label': '', 'render': '', 'facets': [{'chave': 'iden_preenchido', 'label': 'Identificação'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'pess_preenchido', 'label': 'Dados pessoais'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'cust_preenchido', 'label': 'Custos do projeto'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'inov_preenchido', 'label': 'Inovação'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'prop_preenchido', 'label': 'Propriedade Intelecutal'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'parc_preenchido', 'label': 'Parceirias'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'gove_preenchido', 'label': 'Governança'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'socio_f_preenchido', 'label': 'Socieconomico Financeiro'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'socio_p_preenchido', 'label': 'Socioeconomico Pessoal'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'aval_preenchido', 'label': 'Avaliação do programa PIPE'}]},
             ]},

            {'groupBy': {'id': 'iden', 'label': 'Identificação', 'order': 1},
             'facetGroup': [
                 {'label': '', 'render': '', 'facets': [{'chave': 'iden_participacao_capital_estrangeiro',
                                                         'label': 'Participação de capital estrangeiro'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'iden_estado', 'label': 'Estado'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'iden_municipio_ibge', 'label': 'Município'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'iden_sede_propria', 'label': 'Sede própria'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'iden_mundanca_acionaria', 'label': 'Mudança Acionária'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'iden_respondente_responsavel',
                                                         'label': 'Respondente é o pesquisador responsável do projeto?'}]},
             ]},

            {'groupBy': {'id': 'CNAE', 'label': 'CNAE', 'order': 2},
             'facetGroup': [
                 {'label': '', 'render': '', 'facets': [{'chave': 'iden_Emp_cnae_facet', 'label': 'CNAE da empresa'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'iden_cnae_facet', 'label': 'CNAE do projeto'}]},
             ]},

            {'groupBy': {'id': 'esfor_gastos',
                         'label': 'Esforço de P&D e Inovação: Total de gastos com P&D realizados com recursos da empresa',
                         'order': 3.1},
             'facetGroup': [
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'esfo_DEPOIS2_valor_decorrencia_pipe', 'label': 'Depois 2'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'esfo_DEPOIS1_valor_decorrencia_pipe', 'label': 'Depois 1'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'esfo_DURANTE2_valor_decorrencia_pipe', 'label': 'Durante 2'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'esfo_DURANTE1_valor_decorrencia_pipe', 'label': 'Durante 1'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'esfo_ANTES2_valor_decorrencia_pipe', 'label': 'Antes 2'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'esfo_ANTES1_valor_decorrencia_pipe', 'label': 'Antes 1'}]},
             ]},

            {'groupBy': {'id': 'esfor_influ',
                         'label': 'Esforço de P&D e Inovação: Influência dos recursos alocados pela FAPESP',
                         'order': 3.2},
             'facetGroup': [
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'esfo_DEPOIS2_GastosPD_fator_redundante', 'label': 'Depois 2'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'esfo_DEPOIS1_GastosPD_fator_redundante', 'label': 'Depois 1'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'esfo_DURANTE2_GastosPD_fator_redundante', 'label': 'Durante 2'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'esfo_DURANTE1_GastosPD_fator_redundante', 'label': 'Durante 1'}]},
             ]},

            {'groupBy': {'id': 'pess', 'label': 'Dados do respondente', 'order': 4},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'pess_escolaridade', 'label': 'Escolaridade'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'pess_experiencia', 'label': 'Experiência no tema (anos)'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'pess_formacao', 'label': 'Formação em gestão (na submissão)'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'pess_formacao_posterior', 'label': 'Formação em gestão (posteriormente)'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'pess_cargo', 'label': 'Cargo (na submissão)'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'pess_cargo_atual', 'label': 'Cargo (atual)'}]},
             ]},

            {'groupBy': {'id': 'resu', 'label': 'Resultados', 'order': 5},
             'facetGroup': [
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'resu_chegou_a_resultados', 'label': 'Resultados alcançados'}]},
             ]},

            {'groupBy': {'id': 'pi', 'label': 'Geração de patentes e PI', 'order': 6},
             'facetGroup': [
                 {'label': 'Influência PIPE - Geração de Patentes', 'render': 'barChart_1',
                  'facets': [{'chave': 'prop_registro_brasil_mu', 'label': 'Patentes'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'prop_registro_brasil_marcas', 'label': 'Marcas'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'prop_registro_brasil_sw', 'label': 'Software'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'prop_registro_brasil_ci', 'label': 'Circuitos Integrados'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'prop_registro_brasil_plantas', 'label': 'Cultivares de plantas'}]},
             ]},

            {'groupBy': {'id': 'parc', 'label': 'Parcerias', 'order': 7},
             'facetGroup': [
                 {'label': '', 'render': '', 'facets': [{'chave': 'parc_parcerias_institutos_universidades',
                                                         'label': 'Parceria com institutos/universidades'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'parc_parcerias_outros_atores', 'label': 'Parceria com outros atores'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'parc_influencia_pipe_inst_univ',
                                                         'label': 'Influência PIPE se parceria com inst/univ'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'parc_influencia_pipe_outros_atores',
                                                         'label': 'Influência PIPE se parceria com outros atores'}]},
             ]},

            {'groupBy': {'id': 'govr', 'label': 'Governança', 'order': 8},
             'facetGroup': [
                 {'label': '', 'render': '', 'facets': [{'chave': 'gove_pdi_explicito', 'label': 'PDI Explicito'}]},
                 {'label': '', 'render': '', 'facets': [
                     {'chave': 'gove_influencia_pipe_pdi_explicito', 'label': 'Influencia PIPE PDI explícito'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'gove_regras_compliance', 'label': 'Regras de compliance'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'gove_modelos_gestao', 'label': 'Modelos de gestão'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'gove_organizacao_pdi', 'label': 'Organização PDI'}]},
                 {'label': '', 'render': '', 'facets': [
                     {'chave': 'gove_influencia_pipe_organizacao_pdi', 'label': 'Influência PIPE Organização PDI'}]},
             ]},

            {'groupBy': {'id': 'aval', 'label': 'Avaliação do programa PIPE', 'order': 9},
             'facetGroup': [
                 {'label': '', 'render': '', 'facets': [{'chave': 'aval_doc_base', 'label': 'Documentação base'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'aval_crit_cand', 'label': 'Critérios da candidatura'}]},
                 {'label': '', 'render': '', 'facets': [
                     {'chave': 'aval_proc_selec', 'label': 'Procedimentos de seleção e informação de resultados'}]},
                 {'label': '', 'render': '', 'facets': [{'chave': 'aval_tempo_selec', 'label': 'Tempo para seleção'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'aval_condi_fin', 'label': 'Condições do financiamento'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'aval_neg_pi', 'label': 'Negociação de Popriedade Intelectual	'}]},
                 {'label': '', 'render': '',
                  'facets': [{'chave': 'aval_valor_apoio', 'label': 'Valor do apoio dado pela FAPESP	'}]},
             ]},

        ],
        'totalizadores': [
            {'label': 'Média de gastos com P&D - Antes 1', 'data_type': 'currency',
             'avg': 'esfo_ANTES1_valor_decorrencia_pipe', 'order': 1, 'docs': {}, 'type': ['main']},
            # {'label':'Média de gastos com P&D - Antes 2' , 'avg':'esfo_ANTES2_valor_decorrencia_pipe', 'order':2, 'docs':{}, 'type':['main']},
            # {'label':'Média de gastos com P&D - Durante 1' , 'avg':'esfo_DURANTE1_valor_decorrencia_pipe', 'order':3, 'docs':{}, 'type':['main']},
            # {'label':'Média de gastos com P&D - Durante 2' , 'avg':'esfo_DURANTE2_valor_decorrencia_pipe', 'order':4, 'docs':{}, 'type':['main']},
            # {'label':'Média de gastos com P&D - Depois 1' , 'avg':'esfo_DEPOIS1_valor_decorrencia_pipe', 'order':5, 'docs':{}, 'type':['main']},
            # {'label':'Média de gastos com P&D - Depois 2' , 'avg':'esfo_DEPOIS2_valor_decorrencia_pipe', 'order':6, 'docs':{}, 'type':['main']},

            {'label': 'Patentes independentes do PIPE', 'sum': 'prop_registro_brasil_mu', 'order': 4, 'docs': {},
             'type': ['main']},
            {'label': 'Patentes decorrentes do PIPE', 'sum': 'prop_registro_pipe_brasil_mu', 'order': 5, 'docs': {},
             'type': ['main']},

            {'label': 'Projeto chegou a resultados', 'facet': {'resu_chegou_a_resultados': ["Sim"]}, 'docs': {},
             'type': ['main'], 'order': 2},
        ],
    },

    'inep_docentes': {
        # 'django_ct':'geral.pesquisador',
        'label': 'INEP - Docentes',
        'omite_secoes': ['refine', 'busca', 'documentos', 'related_collections'],
        # Caso nao queira uma determinada secao no buscador.

        'campo_dinamico_busca': 'cross_collection_inep_docentes',
        # 'id_index_from':'id_pesquisador',
        # 'id_index_to':'django_id',
        'facets_categorias': [
            {'groupBy': {'id': 'sobre', 'label': 'Sobre a pesquisa', 'order': 3},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'ano_vigencia_inep', 'label': 'Ano de vigência do INEP'}]},
             ]},

            {'groupBy': {'id': 'docente', 'label': 'Docente', 'order': 1},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DS_NACIONALIDADE_DOCENTE', 'label': 'Nacionalidade'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'CO_UF_NASCIMENTO', 'label': 'Estado natal'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'CO_MUNICIPIO_NASCIMENTO', 'label': 'Município natal'}]},
                 {'label': '', 'render': 'halfPieChart', 'facets': [{'chave': 'DS_SEXO_DOCENTE', 'label': 'Gênero'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'NU_ANO_DOCENTE_NASC', 'label': 'Ano de nascimento'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DS_COR_RACA_DOCENTE', 'label': 'Cor/Raça'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'CO_ESCOLARIDADE_DOCENTE', 'label': 'Escolaridade'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'IN_DOCENTE_DEFICIENCIA', 'label': 'Deficiência física'}]},
             ]},

            {'groupBy': {'id': 'ies', 'label': 'Instituição de ensino superior', 'order': 2},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'MANT_IES', 'label': 'Mantenedora/IES'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'GEOGRAFICO', 'label': 'Localização'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'Categoria Administrativa'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DS_ORGANIZACAO_ACADEMICA', 'label': 'Organização Acadêmica'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'IN_CAPITAL_IES', 'label': 'IES localizada na capital?'}]},
             ]},

            {'groupBy': {'id': 'regime_trabalho', 'label': 'Condições de trabalho', 'order': 3},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DS_SITUACAO_DOCENTE', 'label': 'Situação do docente'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DS_REGIME_TRABALHO', 'label': 'Regime de trabalho'}]},
                 # {'label':'' , 'render':'municipios', 'facets':[{'chave':'CO_DOCENTE', 'label': 'Verifica duplicacao'}]},

             ]},

            {'groupBy': {'id': 'docente_atuacao', 'label': 'Docente - Atuação', 'order': 4},
             'facetGroup': [
                 {'label': '', 'render': 'halfPieChart', 'facets': [{'chave': 'IN_ATU_EAD', 'label': 'EAD'}]},
                 {'label': '', 'render': 'halfPieChart', 'facets': [{'chave': 'IN_ATU_EXTENSAO', 'label': 'Extensão'}]},
                 {'label': '', 'render': 'halfPieChart', 'facets': [{'chave': 'IN_ATU_GESTAO', 'label': 'Gestão'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'IN_ATU_GRAD_PRESENCIAL', 'label': 'Graduação Presencial'}]},
                 {'label': '', 'render': 'halfPieChart', 'facets': [{'chave': 'IN_ATU_POS_EAD', 'label': 'EAD - Pós'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'IN_ATU_POS_PRESENCIAL', 'label': 'Pós presencial'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'IN_ATU_SEQUENCIAL', 'label': 'Curso sequencial'}]},
                 {'label': '', 'render': 'halfPieChart', 'facets': [{'chave': 'IN_ATU_PESQUISA', 'label': 'Pequisa'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'IN_ATU_GRAD_PRESENCIAL', 'label': 'Graduação Presencial'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'IN_BOLSA_PESQUISA', 'label': 'Possui bolsa de pesquisa'}]},
                 {'label': '', 'render': 'halfPieChart', 'facets': [{'chave': 'IN_SUBSTITUTO', 'label': 'Substituto'}]},
                 {'label': '', 'render': 'halfPieChart', 'facets': [{'chave': 'IN_VISITANTE', 'label': 'Visitante'}]},
                 {'label': '', 'render': 'halfPieChart', 'facets': [
                     {'chave': 'IN_VISITANTE_IFES_VINCULO', 'label': 'Tipo de vínculo do docente visitante à IES'}]},
             ]},
        ],
        'totalizadores': [
            {'label': 'Docentes nascidos no estado de São Paulo', 'facet': {'CO_UF_NASCIMENTO': ["35"]}, 'docs': {},
             'type': ['main'], 'order': 2},
            {'label': 'Número de docentes únicos', 'unique': 'CO_DOCENTE', 'order': 1, 'docs': {}, 'type': ['main']},
            {'label': 'Total de mantenedoras', 'unique': 'CO_MANTENEDORA', 'order': 3, 'docs': {}, 'type': ['main']},
            {'label': 'Municípios com IES', 'unique': 'CO_MUNICIPIO_IES', 'order': 4, 'docs': {}, 'type': ['main']},
        ],
    },

    'inep_alunos': {
        # 'django_ct':'geral.pesquisador',
        'label': 'INEP - Alunos',
        'omite_secoes': ['refine', 'busca', 'documentos', 'related_collections'],
        # Caso nao queira uma determinada secao no buscador.

        'campo_dinamico_busca': 'cross_collection_inep_alunos',
        # 'id_index_from':'id_pesquisador',
        # 'id_index_to':'django_id',
        'facets_categorias': [
            {'groupBy': {'id': 'sobre', 'label': 'Sobre a pesquisa', 'order': 3},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'ano_vigencia_inep', 'label': 'Ano de vigência do INEP'}]},
             ]},

            {'groupBy': {'id': 'aluno', 'label': 'Dados pessoais', 'order': 1},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'NU_IDADE_ALUNO', 'label': 'Idade'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'NU_ANO_ALUNO_NASC', 'label': 'Ano de nascimento'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'DS_COR_RACA_ALUNO', 'label': 'Cor/Raça'}]},
                 {'label': '', 'render': 'halfPieChart', 'facets': [{'chave': 'DS_SEXO_ALUNO', 'label': 'Sexo'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DS_NACIONALIDADE_ALUNO', 'label': 'Nacionalidade'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'CO_MUNICIPIO_NASCIMENTO', 'label': 'Município nascimento'}]},
             ]},

            {'groupBy': {'id': 'inf_acad', 'label': 'Informações do aluno', 'order': 2},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'ANO_INGRESSO', 'label': 'Ano de ingresso'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'DS_NIVEL_ACADEMICO', 'label': 'Nível acadêmico'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DS_GRAU_ACADEMICO', 'label': 'Grau acadêmico'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'IN_ACESSO_PORTAL_CAPES', 'label': 'Acesso ao portal Capes'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'DS_MODALIDADE_ENSINO', 'label': 'Modalidade de ensino'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'QT_CARGA_HORARIA_INTEG', 'label': 'Carga horária'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DS_TURNO_ALUNO', 'label': 'Turno do aluno'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DS_ALUNO_SITUACAO', 'label': 'Situação do aluno'}]},
             ]},

            {'groupBy': {'id': 'ies_aluno', 'label': 'Instituição de ensino superior', 'order': 2},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'MANT_IES', 'label': 'Mantenedora/IES'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'GEOGRAFICO', 'label': 'Localização'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'Categoria Administrativa'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DS_ORGANIZACAO_ACADEMICA', 'label': 'Organização Acadêmica'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'IN_CAPITAL_IES', 'label': 'IES localizada na capital?'}]},
             ]},

            {'groupBy': {'id': 'ocde', 'label': 'OCDE', 'order': 1},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'NO_OCDE', 'label': 'OCDE'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'NO_OCDE_AREA_GERAL', 'label': 'OCDE - Área geral'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'NO_OCDE_AREA_DETALHADA', 'label': 'OCDE - Área detalhada'}]},
             ]},
        ],
        'totalizadores': [
        ],
    },

    'fazenda_sp': {
        'label': 'Fazenda SP - Execução orçamentária',
        'omite_secoes': ['refine', 'busca', 'documentos', 'related_collections'],
        # Caso nao queira uma determinada secao no buscador.
        'campo_dinamico_busca': 'cross_collection_fazenda_sp',
        'facets_categorias': [
            {'groupBy': {'id': 'fonte', 'label': 'Fonte', 'order': 1},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'Fonte_de_Recursos', 'label': 'Fonte de Recursos'}]},
             ]},
            {'groupBy': {'id': 'orgao', 'label': 'Orgão', 'order': 2},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': '_rg_o', 'label': 'Orgão'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'UO', 'label': 'UO'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'Unidade_Gestora', 'label': 'Unidade Gestora'}]},
             ]},
            {'groupBy': {'id': 'funcao', 'label': 'Função', 'order': 3},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'Fun__o', 'label': 'Função'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'Sub_Fun__o', 'label': 'Sub Função'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'Programa', 'label': 'Programa'}]},
             ]},
            {'groupBy': {'id': 'elemento', 'label': 'Elemento', 'order': 4},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'A__o', 'label': 'Ação'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'Funcional_Program_tica', 'label': 'Funcional Programática'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'Elemento', 'label': 'Elemento'}]},
             ]},

            # {'groupBy':{'id':'dotacao', 'label':'Dotação','order':5},
            # 'facetGroup':[
            # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'Dota__o_Inicial', 'label': 'Dotação Inicial'}]},
            # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'Dota__o_Atual', 'label': 'Dotação Atual'}]},
            # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'Empenhado', 'label': 'Empenhado'}]},
            # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'Liquidado', 'label': 'Liquidado'}]},
            # ]},

        ],
        'totalizadores': [
            {'label': 'Dotação Inicial', 'sum': 'Dota__o_Inicial', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 1},
            {'label': 'Dotação Atual', 'sum': 'Dota__o_Atual', 'docs': {}, 'data_type': 'currency', 'type': ['main'],
             'order': 2},
            {'label': 'Empenhado', 'sum': 'Empenhado', 'docs': {}, 'data_type': 'currency', 'type': ['main'],
             'order': 3},
            {'label': 'Liquidado', 'sum': 'Liquidado', 'docs': {}, 'data_type': 'currency', 'type': ['main'],
             'order': 4},
            {'label': 'Pago', 'sum': 'Pago', 'docs': {}, 'data_type': 'currency', 'type': ['main'], 'order': 5},
            {'label': 'Pago_Restos', 'sum': 'Pago_Restos', 'docs': {}, 'data_type': 'currency', 'type': ['main'],
             'order': 6},
        ],
    },

    'rais': {
        # 'django_ct':'geral.pesquisador',
        'label': ' RAIS - RELAÇÃO ANUAL DE INFORMAÇÕES SOCIAIS ',
        'omite_secoes': ['refine', 'busca', 'documentos', 'related_collections'],
        # Caso nao queira uma determinada secao no buscador.

        'campo_dinamico_busca': 'cross_collection_rais',
        'id_index_from': '',
        'id_index_to': '',
        'facets_categorias': [
            {'groupBy': {'id': 'pessoais', 'label': 'Pessoais', 'order': 1},
             'facetGroup': [
                 {'label': 'Idade', 'render': 'barChart_1', 'facets': [{'chave': 'Idade', 'label': 'Idade'}]},
                 {'label': 'Idade', 'render': 'halfPieChart',
                  'facets': [{'chave': 'Ind_Portador_Defic', 'label': 'Ind_Portador_Defic'}]},
                 {'label': 'Idade', 'render': 'barChart_1', 'facets': [{'chave': 'Ra_a_Cor', 'label': 'Raça / Cor'}]},
                 {'label': 'Idade', 'render': 'barChart_1',
                  'facets': [{'chave': 'Faixa_Et_ria', 'label': 'Faixa Etária'}]},
                 {'label': 'Idade', 'render': 'barChart_1',
                  'facets': [{'chave': 'Escolaridade_ap_s_2005', 'label': 'Escolaridade após 2005'}]},
                 {'label': 'Idade', 'render': 'halfPieChart',
                  'facets': [{'chave': 'Sexo_Trabalhador', 'label': 'Sexo'}]},
                 {'label': 'Idade', 'render': 'barChart_1', 'facets': [{'chave': 'Tipo_Defic', 'label': 'Tipo_Defic'}]},
                 {'label': 'Idade', 'render': 'barChart_1',
                  'facets': [{'chave': 'Ano_Chegada_Brasil', 'label': 'Ano de chegada ao Brasil'}]},

             ]},

            {'groupBy': {'id': 'geografico', 'label': 'Geo', 'order': 2},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'Munic_pio', 'label': 'Município'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'Mun_Trab', 'label': 'Mun_Trab'}]},
                 {'label': 'Nacionalidade', 'render': 'barChart_1',
                  'facets': [{'chave': 'Nacionalidade', 'label': 'Nacionalidade'}]},
                 {'label': 'Distritos_SP', 'render': 'barChart_1',
                  'facets': [{'chave': 'Distritos_SP', 'label': 'Distrito SP'}]},
                 {'label': 'Bairros_SP', 'render': 'barChart_1',
                  'facets': [{'chave': 'Bairros_SP', 'label': 'Bairro SP'}]},
             ]},
            {'groupBy': {'id': 'afastamento', 'label': 'Afastamento / Desligamento', 'order': 2},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'Causa_Afastamento_1', 'label': 'Causa Afastamento 1'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'Causa_Afastamento_2', 'label': 'Causa Afastamento 2'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'Causa_Afastamento_3', 'label': 'Causa Afastamento 3'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'Motivo_Desligamento', 'label': 'Motivo Desligamento'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'Qtd_Dias_Afastamento', 'label': 'Qtd_Dias_Afastamento'}]},
             ]},

            {'groupBy': {'id': 'ocupa_cnae', 'label': 'Ocupação / CNAE', 'order': 3},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'CBO_Ocupa__o_2002', 'label': 'CBO_Ocupa__o_2002'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'CNAE_95_Classe', 'label': 'CNAE_95_Classe'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'CNAE_2.0_Classe', 'label': 'CNAE_2.0_Classe'}]}, # Dah erro
             ]},
            {'groupBy': {'id': 'trabalho', 'label': 'Trabalho', 'order': 4},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'Tipo_V_nculo', 'label': 'Tipo_V_nculo'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'IBGE_Subsetor', 'label': 'IBGE_Subsetor'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'Tipo_Estab', 'label': 'Tipo_Estab'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'Tipo_Admiss_o', 'label': 'Tipo_Admiss_o'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'Tipo_Estab', 'label': 'Tipo_Estab'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'Tamanho_Estabelecimento', 'label': 'Tamanho_Estabelecimento'}]},
             ]},
        ],
        'totalizadores': [
            {'label': 'Vl_Remun_Dezembro_Nom', 'sum': 'Vl_Remun_Dezembro_Nom', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 1},
            {'label': 'Vl_Remun_Dezembro__SM_', 'sum': 'Vl_Remun_Dezembro__SM_', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 2},
            {'label': 'Vl_Remun_M_dia_Nom', 'sum': 'Vl_Remun_M_dia_Nom', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 3},
            {'label': 'Vl_Remun_M_dia__SM_', 'sum': 'Vl_Remun_M_dia__SM_', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 4},
            {'label': 'Vl_Rem_Janeiro_CC', 'sum': 'Vl_Rem_Janeiro_CC', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 5},
            {'label': 'Vl_Rem_Fevereiro_CC', 'sum': 'Vl_Rem_Fevereiro_CC', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 6},
            {'label': 'Vl_Rem_Mar_o_CC', 'sum': 'Vl_Rem_Mar_o_CC', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 7},
            {'label': 'Vl_Rem_Abril_CC', 'sum': 'Vl_Rem_Abril_CC', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 8},
            {'label': 'Vl_Rem_Maio_CC', 'sum': 'Vl_Rem_Maio_CC', 'docs': {}, 'data_type': 'currency', 'type': ['main'],
             'order': 9},
            {'label': 'Vl_Rem_Junho_CC', 'sum': 'Vl_Rem_Junho_CC', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 10},
            {'label': 'Vl_Rem_Julho_CC', 'sum': 'Vl_Rem_Julho_CC', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 10},
            {'label': 'Vl_Rem_Agosto_CC', 'sum': 'Vl_Rem_Agosto_CC', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 10},
            {'label': 'Vl_Rem_Setembro_CC', 'sum': 'Vl_Rem_Setembro_CC', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 10},
            {'label': 'Vl_Rem_Outubro_CC', 'sum': 'Vl_Rem_Outubro_CC', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 10},
            {'label': 'Vl_Rem_Novembro_CC', 'sum': 'Vl_Rem_Novembro_CC', 'docs': {}, 'data_type': 'currency',
             'type': ['main'], 'order': 11},
        ],
    },

    'lattes': {
        # Os campos comentados no LATTES eh pq nao sao normalizados.
        'label': 'CNPQ - CV Lattes',
        'omite_secoes': ['refine', 'documentos', 'related_collections'],
        # Caso nao queira uma determinada secao no buscador.

        'campo_dinamico_busca': 'cross_collection_lattes',
        'id_index_from': '',
        'id_index_to': '',
        'facets_categorias': [

            {'groupBy': {'id': 'pessoais', 'label': 'Pessoais', 'order': 1},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [
                     {'chave': 'AREAS-DO-CONHECIMENTO-DE-ATUACAO_FACET', 'label': 'Área do conhecimento (atuação)'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'ATIVIDADES-DE-ENSINO_DISCIPLINAS', 'label': 'Ensino disciplinas'}]},
             ]},

            {'groupBy': {'id': 'graduacao', 'label': 'Graduação', 'order': 2},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'NUM_GRADUACOES', 'label': 'Qt. de Graduações'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'GRADUACAO_NOME-AGENCIA', 'label': 'Agência'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'GRADUACAO_NOME-INSTITUICAO', 'label': 'Instituição'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'GRADUACAO_STATUS-DO-CURSO', 'label': "Graduação status"}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'GRADUACAO_NOME-CURSO', 'label': 'Curso'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'GRADUACAO_ANO-DE-INICIO', 'label': 'Ano Início'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'GRADUACAO_ANO-DE-CONCLUSAO', 'label': 'Ano Conclusão'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'GRADUACAO_FLAG-BOLSA', 'label': 'Graduação com bolsa'}]},
             ]},

            {'groupBy': {'id': 'especializacao', 'label': 'Especialização', 'order': 3},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'NUM_ESPECIALIZACOES', 'label': 'Qt. de Especializações'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'ESPECIALIZACAO_NOME-AGENCIA', 'label': 'Agência'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'ESPECIALIZACAO_NOME-INSTITUICAO', 'label': 'Instituição'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'ESPECIALIZACAO_STATUS-DO-CURSO', 'label': "Especialização status"}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'GRADUACAO_NOME-CURSO', 'label': 'Curso'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'ESPECIALIZACAO_ANO-DE-INICIO', 'label': 'Ano Início'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'ESPECIALIZACAO_ANO-DE-CONCLUSAO', 'label': 'Ano Conclusão'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'ESPECIALIZACAO_FLAG-BOLSA', 'label': 'Especialização com bolsa'}]},
             ]},

            {'groupBy': {'id': 'mestrado', 'label': 'Mestrado', 'order': 4},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'NUM_MESTRADOS', 'label': 'Qt. de Mestrados'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'MESTRADO_STATUS-DO-CURSO', 'label': 'Mestrado status'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'MESTRADO_FLAG-BOLSA', 'label': 'Mestrado com Bolsa'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'MESTRADO_NOME-AGENCIA', 'label': 'Agência'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'MESTRADO_NOME-INSTITUICAO', 'label': 'Instituição'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'MESTRADO_CODIGO-INSTITUICAO', 'label': 'Instituição (código)'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'MESTRADO_ANO-DE-INICIO', 'label': 'Ano Início'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'MESTRADO_ANO-DE-CONCLUSAO', 'label': 'Ano Conclusão'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'MESTRADO_ESPECIALIDADE', 'label': 'Áreas especialidade'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'MESTRADO_AREAS-DO-CONHECIMENTO_FACET', 'label': 'Áreas do conhecimento'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'MESTRADO_NOME-CURSO', 'label': 'Curso'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'MESTRADO_PALAVRAS-CHAVE', 'label': 'Palavras-chave'}]},
             ]},
            {'groupBy': {'id': 'doutorado', 'label': 'Doutorado', 'order': 5},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'NUM_DOUTORADOS', 'label': 'Qt. de Doutorados'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'DOUTORADO_STATUS-DO-CURSO', 'label': 'Doutorado status'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'DOUTORADO_NIVEL', 'label': 'Nível'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DOUTORADO_ANO-DE-INICIO', 'label': 'Ano início'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DOUTORADO_ANO-DE-CONCLUSAO', 'label': 'Ano conclusão'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'DOUTORADO_NOME-INSTITUICAO', 'label': 'Instituição'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'DOUTORADO_NOME-AGENCIA', 'label': 'Agência'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'DOUTORADO_FLAG-BOLSA', 'label': 'Doutorado com bolsa'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'DOUTORADO_PALAVRAS-CHAVE', 'label': 'Palavras chave'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'DOUTORADO_ESPECIALIDADE', 'label': 'Área especialiadde'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'DOUTORADO_AREAS-DO-CONHECIMENTO_FACET', 'label': 'Área do conhecimento'}]},
             ]},
            {'groupBy': {'id': 'pos_doutorado', 'label': 'Pós-doutorado', 'order': 6},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'NUM_POS-DOUTORADOS', 'label': 'Qt. de Pós-doutorado'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'POS-DOUTORADO_STATUS-DO-CURSO', 'label': 'Pós-doutorado Status'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'POS-DOUTORADO_NIVEL', 'label': 'Nível'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'POS-DOUTORADO_ANO-DE-INICIO', 'label': 'Ano início'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'POS-DOUTORADO_ANO-DE-CONCLUSAO', 'label': 'Ano conclusão'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'POS-DOUTORADO_NOME-INSTITUICAO', 'label': 'Instituição'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'POS-DOUTORADO_NOME-AGENCIA', 'label': 'Agência'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'POS-DOUTORADO_FLAG-BOLSA', 'label': 'Pós-doutorado com Bolsa'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'DOUTORADO_PALAVRAS-CHAVE', 'label': 'Palavras chave'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'POS-DOUTORADO_ESPECIALIDADE', 'label': 'Área especialiadde'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'POS-DOUTORADO_AREAS-DO-CONHECIMENTO_FACET', 'label': 'Área do conhecimento'}]},
             ]},
            {'groupBy': {'id': 'livre_docencia', 'label': 'Livre-docência', 'order': 7},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'NUM_LIVRE-DOCENCIAS', 'label': 'Qt. de Livre-docência'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'LIVRE-DOCENCIA_NIVEL', 'label': 'Nível'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'LIVRE-DOCENCIA_CODIGO-INSTITUICAO', 'label': 'Código instituição'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [
                     {'chave': 'LIVRE-DOCENCIA_ANO-DE-OBTENCAO-DO-TITULO', 'label': 'Ano de obtenção do título'}]},
             ]},
            {'groupBy': {'id': 'atuacao_profissional', 'label': 'Atuação Profissional', 'order': 8},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'NUM_ATUACOES-PROFISSIONAIS', 'label': 'Qt. de atuações profissionais'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'ATUACAO-PROFISISONAL_ENQUADRAMENTOS', 'label': 'Enquadramentos'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'ATUACAO-PROFISISONAL_TIPOS-DE-VINCULOS', 'label': 'Tipos de vínculo'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'ATUACAO-PROFISISONAL_INSTITUICOES', 'label': 'Instituições'}]},
             ]},
            {'groupBy': {'id': 'p_e_c_c', 'label': 'Projetos, eventos, conselho, consultoria', 'order': 9},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [
                     {'chave': 'NUM_CONSELHO-COMISSAO-E-CONSULTORIA', 'label': 'Cons., comiss., consult. (Qt)'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'CONSELHO-COMISSAO-E-CONSULTORIA_ESPECIFICACAO', 'label': 'Cons., comiss., consult.'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'NUM_PARTICIPACAO-EM-PROJETO', 'label': 'Projetos (Qt)'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'TRABALHO-EM-EVENTOS_AREAS-DO-CONHECIMENTO_FACET', 'label': 'Áreas do conhecimento relacionadas aos eventos'}]},
                 # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'PREMIOS-TITULOS_FACET', 'label': 'Prêmios'}]},
             ]},

        ],
        'totalizadores': [
        ],
    },

    'wos': {
        'label': 'Web of Science',
        'omite_secoes': ['outros_indicadores', 'busca', 'refine', 'sankey', 'bubblechart'],
        # Caso nao queira uma determinada secao no buscador.

        'campo_dinamico_busca': 'cross_collection_wos',
        'facets_categorias': [
            {'groupBy': {'id': 'categoria', 'label': 'Categoria', 'order': 1},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'research-areas', 'label': 'Áreas de pesquisa'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'web-of-science-categories', 'label': 'Categorias WoS'}]},
             ]},

            {'groupBy': {'id': 'editora_revista', 'label': 'Editora / Revista', 'order': 0},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'journal-iso', 'label': 'Publicação ISO'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'type', 'label': 'Tipo'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'publisher_journal_volume', 'label': 'Editora'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'Year-Month', 'label': 'Ano'}]},
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'language', 'label': 'Língua'}]},
             ]},

            {'groupBy': {'id': 'citacoes', 'label': 'Citações', 'order': 2},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'number-of-cited-references', 'label': 'Referências citadas'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'times-cited', 'label': 'Número de citações'}]},
             ]},
            # Campos buscaveis
            # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'keyword', 'label': 'keyword'}]},
            # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'keyword-plus', 'label': 'keyword-plus'}]},

            # Campos nao usaveis
            # {'label':'' , 'render':'barChart_1', 'facets':[{'chave':'address', 'label': 'address'}]}, desnormalizado - nao usavel
        ],
        'totalizadores': [
        ],
    },

    'enade': {
        # 'django_ct':'geral.pesquisador',
        'label': 'Enade',
        'omite_secoes': ['refine', 'busca', 'documentos', 'related_collections'],
        # Caso nao queira uma determinada secao no buscador.

        'campo_dinamico_busca': 'cross_collection_enade',
        # 'id_index_from':'id_pesquisador',
        # 'id_index_to':'django_id',
        'facets_categorias': [
            {'groupBy': {'id': 'sobre', 'label': 'Sobre a pesquisa', 'order': 1},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'Ano_facet', 'label': 'Ano de pesquisa do ENADE'}]},
             ]},

            {'groupBy': {'id': 'ies', 'label': 'IES', 'order': 2},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'CO_CATEGAD', 'label': 'Categoria administrativa da IES'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'CO_ORGACAD', 'label': 'Organização acadêmica da IES'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'CO_GRUPO', 'label': 'Área de enquadramento do curso no Enade'}]},
                 {'label': '', 'render': 'halfPieChart',
                  'facets': [{'chave': 'CO_MODALIDADE', 'label': 'Modalidade de Ensino'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'GEOGRAFICO_facet', 'label': 'Localização'}]},

             ]},

            {'groupBy': {'id': 'estudante', 'label': 'Dados do estudante', 'order': 1},
             'facetGroup': [
                 {'label': '', 'render': 'barChart_1', 'facets': [{'chave': 'NU_IDADE', 'label': 'Idade'}]},
                 {'label': '', 'render': 'halfPieChart', 'facets': [{'chave': 'TP_SEXO', 'label': 'Sexo'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'ANO_FIM_2G', 'label': 'Ano de termino do Ensino Médio'}]},
                 {'label': '', 'render': 'barChart_1',
                  'facets': [{'chave': 'ANO_IN_GRAD', 'label': 'Ano início da graduação'}]},

             ]},


        ],
        'totalizadores': [
            {'label': 'Total de estudantes', 'facet': {'ID': ["*"]}, 'docs': {}, 'type': ['main'], 'order': 1},

        ],
    },

}

"""
!!! Cuidado com este grafico.
Caso sejam utilizados colunas que retornam campos com valores iguais, como sim/nao, 0/1,
ou qquer outro que tenha nomes iguais, o script entra em loop e dah outoff memory no javascript.
"""
SANKEY_CHART = {
    'inep_docentes': {
        'default_level_1': {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'IES - Categoria Administrativa'},
        'default_level_2': {'value': 'DS_ORGANIZACAO_ACADEMICA', 'label': 'IES - Organização Acadêmica'},
        'default_level_3': {'value': 'NO_REGIAO_IES', 'label': 'IES - Região'},
        'options': [{'value': 'DS_ORGANIZACAO_ACADEMICA', 'label': 'IES - Organização Acadêmica'},
                    {'value': 'SGL_UF_IES', 'label': 'IES - UF'},
                    {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'IES - Categoria Administrativa'},
                    {'value': 'NO_REGIAO_IES', 'label': 'IES - Região'},
                    {'value': 'DS_REGIME_TRABALHO', 'label': 'IES - Regime de trabalho'},
                    {'value': 'IN_BOLSA_PESQUISA', 'label': 'IES - Bolsa pesquisa'},
                    {'value': 'IN_ATU_POS_PRESENCIAL', 'label': 'IES - Pós presencial'},
                    {'value': 'IN_ATU_POS_EAD', 'label': 'IES - Pós EAD'},
                    {'value': 'CO_UF_NASCIMENTO', 'label': 'Docente - UF (código)'},
                    {'value': 'DS_SEXO_DOCENTE', 'label': 'Docente - Sexo'},
                    {'value': 'DS_COR_RACA_DOCENTE', 'label': 'Docente - Cor/Raça'},
                    ],
    },

    'inep_alunos': {
        'default_level_1': {'value': 'NO_OCDE_AREA_GERAL', 'label': 'OCDE - Geral'},
        'default_level_2': {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'IES - Categoria Administrativa'},
        'options': [
            {'value': 'ANO_INGRESSO', 'label': 'Ano de ingresso'},
            {'value': 'DS_TURNO_ALUNO', 'label': 'Turno do aluno'},
            {'value': 'DS_ALUNO_SITUACAO', 'label': 'Situação do aluno'},

            {'value': 'DS_MODALIDADE_ENSINO', 'label': 'Modalidade de ensino'},
            {'value': 'DS_GRAU_ACADEMICO', 'label': 'Grau acadêmico'},
            {'value': 'DS_NIVEL_ACADEMICO', 'label': 'Nível acadêmico'},

            {'value': 'SGL_UF_IES', 'label': 'IES - UF'},
            {'value': 'NO_REGIAO_IES', 'label': 'IES - Região'},
            {'value': 'DS_ORGANIZACAO_ACADEMICA', 'label': 'IES - Organização Acadêmica'},
            {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'IES - Categoria Administrativa'},
            {'value': 'IN_BOLSA_PESQUISA', 'label': 'IES - Bolsa pesquisa'},

            {'value': 'NO_OCDE_AREA_GERAL', 'label': 'OCDE - Geral'},

        ],
    },

    'pesquisa_pipe': {
        'default_level_1': {'value': 'aval_doc_base', 'label': 'Avaliação - Documentos base'},
        'default_level_2': {'value': 'resu_chegou_a_resultados', 'label': 'Resultados alcançados'},
        'options': [
            {'value': 'aval_doc_base', 'label': 'Avaliação - Documentos base'},
            {'value': 'gove_modelos_gestao', 'label': 'Governança - Modelos de gestão'},
            {'value': 'gove_pdi_explicito', 'label': 'Governança - PDI Explícito'},
            {'value': 'pess_escolaridade', 'label': 'Pessoal - Escolaridade'},
            {'value': 'pess_cargo', 'label': 'Pessoal - Cargo'},
            {'value': 'parc_parcerias_institutos_universidades', 'label': 'Parcerias - Institutos/Universidades'},
            {'value': 'parc_parcerias_outros_atores', 'label': 'Parcerias - Outros atores'},
            {'value': 'resu_chegou_a_resultados', 'label': 'Resultados alcançados'},
        ],
    },

    'lattes': {
        'default_level_1': {'value': 'MESTRADO_GRANDE-AREA-DO-CONHECIMENTO'},
        'default_level_2': {'value': 'DOUTORADO_GRANDE-AREA-DO-CONHECIMENTO'},
        'options': [
            # {'value':'GRADUACAO_NOME-CURSO', 'label':'Graduação - Curso'},
            {'value': 'GRADUACAO_ANO-DE-INICIO', 'label': 'Graduação - Ano início'},
            {'value': 'GRADUACAO_ANO-DE-CONCLUSAO', 'label': 'Graduação - Ano conclusão'},
            # {'value':'GRADUACAO_NOME-INSTITUICAO', 'label':'Graduação - Instituição'},
            # {'value':'GRADUACAO_NOME-AGENCIA', 'label':'Graduação - Agência'},
            {'value': 'GRADUACAO_FLAG-BOLSA', 'label': 'Graduação - Bolsa'},
            # {'value':'MESTRADO_NOME-CURSO', 'label':'Mestrado - Curso'},
            {'value': 'MESTRAD_ANO-DE-INICIO', 'label': 'Mestrado - Ano início'},
            {'value': 'MESTRAD_ANO-DE-CONCLUSAO', 'label': 'Mestrado - Ano conclusão'},
            # {'value':'MESTRADO_NOME-INSTITUICAO', 'label':'Mestrado - Instituição'},
            # {'value':'MESTRADO_NOME-AGENCIA', 'label':'Mestrado - Agência'},
            {'value': 'MESTRADO_GRANDE-AREA-DO-CONHECIMENTO', 'label': 'Mestrado - Área do conhecimento'},
            {'value': 'MESTRADO_FLAG-BOLSA', 'label': 'Mestrado - Bolsa'},
            # {'value':'DOUTORADO_NOME-CURSO', 'label':'Doutorado - Curso'},
            {'value': 'DOUTORADO_ANO-DE-INICIO', 'label': 'Doutorado - Ano Início'},
            {'value': 'DOUTORADO_ANO-DE-CONCLUSAO', 'label': 'Doutorado - Ano conclusão'},
            # {'value':'DOUTORADO_NOME-INSTITUICAO', 'label':'Doutorado - Instituição'},
            # {'value':'DOUTORADO_NOME-AGENCIA', 'label':'Doutorado - Agência'},
            {'value': 'DOUTORADO_FLAG-BOLSA', 'label': 'Doutorado - Bolsa'},
            {'value': 'DOUTORADO_GRANDE-AREA-DO-CONHECIMENTO', 'label': 'Doutorado - Área do conhecimento'},
        ],
    },

    'fazenda_sp': {
        'default_level_1': {'value': 'Fonte_de_Recursos', 'label': 'Fonte de recursos'},
        'default_level_2': {'value': 'Fun__o', 'label': 'Função'},
        'options': [
            {'value': 'Fonte_de_Recursos', 'label': 'Fonte de recursos'},
            {'value': 'UO', 'label': 'UO'},
            {'value': '_rg_o', 'label': 'Orgão'},
            {'value': 'Unidade_Gestora', 'label': 'Unidade Gestora'},
            {'value': 'Fun__o', 'label': 'Função'},
            {'value': 'Sub_Fun__o', 'label': 'Sub Função'},
            {'value': 'Programa', 'label': 'Programa'},
            {'value': 'A__o', 'label': 'Ação'},
            {'value': 'Funcional_Program_tica', 'label': 'Funcional Programática'},
            {'value': 'Elemento', 'label': 'Elemento'}, ],
    },

    'rais': {
        'default_level_1': {'value': 'Escolaridade_ap_s_2005', 'label': 'Escolaridade_ap_s_2005'},
        'default_level_2': {'value': 'Sexo_Trabalhador', 'label': 'Sexo'},
        'options': [
            {'value': 'Sexo_Trabalhador', 'label': 'Sexo'},
            {'value': 'Idade', 'label': 'Idade'},
            {'value': 'Munic_pio', 'label': 'Município'},
            {'value': 'Mun_Trab', 'label': 'Município de Trabalho'},
            {'value': 'Nacionalidade', 'label': 'Nacionalidade'},
            {'value': 'Distritos_SP', 'label': 'Distrito SP'},
            {'value': 'Idade', 'label': 'Idade'},
            {'value': 'Ind_Portador_Defic', 'label': 'Ind_Portador_Defic'},
            {'value': 'Ra_a_Cor', 'label': 'Raça / Cor'},
            {'value': 'Faixa_Et_ria', 'label': 'Faixa Etária'},
            {'value': 'Escolaridade_ap_s_2005', 'label': 'Escolaridade após 2005'},
            {'value': 'Tipo_Defic', 'label': 'Tipo_Defic'},
            {'value': 'Ano_Chegada_Brasil', 'label': 'Ano de chegada ao Brasil'}
        ],
    },

    'graph_auxilios': {
        'default_level_1': {'value': 'data_inicio_ano_exact', 'label': 'Ano de início'},
        'default_level_2': {'value': 'situacao', 'label': 'Situação'},
        'options': [
            {'value': 'situacao', 'label': 'Situação'},
            {'value': 'data_inicio_ano_exact', 'label': 'Ano de início'},
            {'value': 'bolsas_pt', 'label': 'Bolsa'},
            {'value': 'auxilio_pesquisa_pt', 'label': 'Auxílio a Pesquisa'},
            # {'value':'area_pt', 'label':'Área do conhecimento'},
            # {'value':'convenio_exact', 'label':'Convênio'},
            {'value': 'tipo_convenio_exact', 'label': 'Tipo de convênio'},
            {'value': 'pais_convenio_exact', 'label': 'País de convênio'},
        ]
    },

    'enade': {
        'default_level_1': {'value': 'CO_CATEGAD', 'label': 'IES - Categoria Administrativa'},
        'default_level_2': {'value': 'CO_ORGACAD', 'label': 'IES - Organização Acadêmica'},
        'default_level_3': {'value': 'GEOGRAFICO_facet', 'label': 'ENADE - Região'},
        'options': [{'value': 'CO_ORGACAD', 'label': 'IES - Organização Acadêmica'},
                    {'value': 'UF_CURSO', 'label': 'Curso - UF'},
                    {'value': 'CO_CATEGAD', 'label': 'IES - Categoria Administrativa'},
                    {'value': 'GEOGRAFICO_facet', 'label': 'ENADE - Região'},
                    {'value': 'Ano_facet', 'label': 'Ano Pesquisa - ENADE'},
                    {'value': 'TP_SEXO', 'label': 'Sexo'},
                    {'value': 'Cor_Raca', 'label': 'Cor/Raça'},
                    {'value': 'Estado_Civil', 'label': 'Estado Civil'},
                    {'value': 'Renda_familiar', 'label': 'Renda familiar'},
                    ],

    },
}

PIVOT_TABLE = {
    'inep_docentes': {
        'default_level_1': {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'IES - Categoria Administrativa'},
        'default_level_2': {'value': 'DS_ORGANIZACAO_ACADEMICA', 'label': 'IES - Organização Acadêmica'},
        'default_level_3': {'value': 'NO_REGIAO_IES', 'label': 'IES - Região'},
        'options': [{'value': 'DS_ORGANIZACAO_ACADEMICA', 'label': 'IES - Organização Acadêmica'},
                    {'value': 'SGL_UF_IES', 'label': 'IES - UF'},
                    {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'IES - Categoria Administrativa'},
                    {'value': 'NO_REGIAO_IES', 'label': 'IES - Região'},
                    {'value': 'DS_REGIME_TRABALHO', 'label': 'IES - Regime de trabalho'},
                    {'value': 'IN_BOLSA_PESQUISA', 'label': 'IES - Bolsa pesquisa'},
                    {'value': 'IN_ATU_POS_PRESENCIAL', 'label': 'IES - Pós presencial'},
                    {'value': 'IN_ATU_POS_EAD', 'label': 'IES - Pós EAD'},
                    {'value': 'CO_UF_NASCIMENTO', 'label': 'Docente - UF (código)'},
                    {'value': 'DS_SEXO_DOCENTE', 'label': 'Docente - Sexo'},
                    {'value': 'DS_COR_RACA_DOCENTE', 'label': 'Docente - Cor/Raça'},
                    ],
    },
    'inep_alunos': {
        'default_level_1': {'value': 'NO_OCDE_AREA_GERAL', 'label': 'OCDE - Geral'},
        'default_level_2': {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'IES - Categoria Administrativa'},
        'options': [
            {'value': 'ANO_INGRESSO', 'label': 'Ano de ingresso'},
            {'value': 'DS_TURNO_ALUNO', 'label': 'Turno do aluno'},
            {'value': 'DS_ALUNO_SITUACAO', 'label': 'Situação do aluno'},

            {'value': 'DS_MODALIDADE_ENSINO', 'label': 'Modalidade de ensino'},
            {'value': 'DS_GRAU_ACADEMICO', 'label': 'Grau acadêmico'},
            {'value': 'DS_NIVEL_ACADEMICO', 'label': 'Nível acadêmico'},

            {'value': 'SGL_UF_IES', 'label': 'IES - UF'},
            {'value': 'NO_REGIAO_IES', 'label': 'IES - Região'},
            {'value': 'DS_ORGANIZACAO_ACADEMICA', 'label': 'IES - Organização Acadêmica'},
            {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'IES - Categoria Administrativa'},
            {'value': 'IN_BOLSA_PESQUISA', 'label': 'IES - Bolsa pesquisa'},

            {'value': 'NO_OCDE_AREA_GERAL', 'label': 'OCDE - Geral'},

        ],
    },

    'pesquisa_pipe': {
        'default_level_1': {'value': 'aval_doc_base', 'label': 'Avaliação - Documentos base'},
        'default_level_2': {'value': 'resu_chegou_a_resultados', 'label': 'Resultados alcançados'},
        'options': [
            {'value': 'aval_doc_base', 'label': 'Avaliação - Documentos base'},
            {'value': 'gove_modelos_gestao', 'label': 'Governança - Modelos de gestão'},
            {'value': 'gove_pdi_explicito', 'label': 'Governança - PDI Explícito'},
            {'value': 'pess_escolaridade', 'label': 'Pessoal - Escolaridade'},
            {'value': 'pess_cargo', 'label': 'Pessoal - Cargo'},
            {'value': 'parc_parcerias_institutos_universidades', 'label': 'Parcerias - Institutos/Universidades'},
            {'value': 'parc_parcerias_outros_atores', 'label': 'Parcerias - Outros atores'},
            {'value': 'resu_chegou_a_resultados', 'label': 'Resultados alcançados'},
        ],
    },

    'lattes': {
        'default_level_1': {'value': 'MESTRADO_GRANDE-AREA-DO-CONHECIMENTO'},
        'default_level_2': {'value': 'DOUTORADO_GRANDE-AREA-DO-CONHECIMENTO'},
        'options': [
            # {'value':'GRADUACAO_NOME-CURSO', 'label':'Graduação - Curso'},
            {'value': 'GRADUACAO_ANO-DE-INICIO', 'label': 'Graduação - Ano início'},
            {'value': 'GRADUACAO_ANO-DE-CONCLUSAO', 'label': 'Graduação - Ano conclusão'},
            # {'value':'GRADUACAO_NOME-INSTITUICAO', 'label':'Graduação - Instituição'},
            # {'value':'GRADUACAO_NOME-AGENCIA', 'label':'Graduação - Agência'},
            {'value': 'GRADUACAO_FLAG-BOLSA', 'label': 'Graduação - Bolsa'},
            # {'value':'MESTRADO_NOME-CURSO', 'label':'Mestrado - Curso'},
            {'value': 'MESTRAD_ANO-DE-INICIO', 'label': 'Mestrado - Ano início'},
            {'value': 'MESTRAD_ANO-DE-CONCLUSAO', 'label': 'Mestrado - Ano conclusão'},
            # {'value':'MESTRADO_NOME-INSTITUICAO', 'label':'Mestrado - Instituição'},
            # {'value':'MESTRADO_NOME-AGENCIA', 'label':'Mestrado - Agência'},
            {'value': 'MESTRADO_GRANDE-AREA-DO-CONHECIMENTO', 'label': 'Mestrado - Área do conhecimento'},
            {'value': 'MESTRADO_FLAG-BOLSA', 'label': 'Mestrado - Bolsa'},
            # {'value':'DOUTORADO_NOME-CURSO', 'label':'Doutorado - Curso'},
            {'value': 'DOUTORADO_ANO-DE-INICIO', 'label': 'Doutorado - Ano Início'},
            {'value': 'DOUTORADO_ANO-DE-CONCLUSAO', 'label': 'Doutorado - Ano conclusão'},
            # {'value':'DOUTORADO_NOME-INSTITUICAO', 'label':'Doutorado - Instituição'},
            # {'value':'DOUTORADO_NOME-AGENCIA', 'label':'Doutorado - Agência'},
            {'value': 'DOUTORADO_FLAG-BOLSA', 'label': 'Doutorado - Bolsa'},
            {'value': 'DOUTORADO_GRANDE-AREA-DO-CONHECIMENTO', 'label': 'Doutorado - Área do conhecimento'},
        ],
    },

    'fazenda_sp': {
        'default_level_1': {'value': 'Fonte_de_Recursos', 'label': 'Fonte de recursos'},
        'default_level_2': {'value': 'Fun__o', 'label': 'Função'},
        'options': [
            {'value': 'Fonte_de_Recursos', 'label': 'Fonte de recursos'},
            {'value': 'UO', 'label': 'UO'},
            {'value': '_rg_o', 'label': 'Orgão'},
            {'value': 'Unidade_Gestora', 'label': 'Unidade Gestora'},
            {'value': 'Fun__o', 'label': 'Função'},
            {'value': 'Sub_Fun__o', 'label': 'Sub Função'},
            {'value': 'Programa', 'label': 'Programa'},
            {'value': 'A__o', 'label': 'Ação'},
            {'value': 'Funcional_Program_tica', 'label': 'Funcional Programática'},
            {'value': 'Elemento', 'label': 'Elemento'}, ],
    },

    'rais': {
        'default_level_1': {'value': 'Escolaridade_ap_s_2005', 'label': 'Escolaridade_ap_s_2005'},
        'default_level_2': {'value': 'Sexo_Trabalhador', 'label': 'Sexo'},
        'options': [
            {'value': 'Sexo_Trabalhador', 'label': 'Sexo'},
            {'value': 'Idade', 'label': 'Idade'},
            {'value': 'Munic_pio', 'label': 'Município'},
            {'value': 'Mun_Trab', 'label': 'Município de Trabalho'},
            {'value': 'Nacionalidade', 'label': 'Nacionalidade'},
            {'value': 'Distritos_SP', 'label': 'Distrito SP'},
            {'value': 'Idade', 'label': 'Idade'},
            {'value': 'Ind_Portador_Defic', 'label': 'Ind_Portador_Defic'},
            {'value': 'Ra_a_Cor', 'label': 'Raça / Cor'},
            {'value': 'Faixa_Et_ria', 'label': 'Faixa Etária'},
            {'value': 'Escolaridade_ap_s_2005', 'label': 'Escolaridade após 2005'},
            {'value': 'Tipo_Defic', 'label': 'Tipo_Defic'},
            {'value': 'Ano_Chegada_Brasil', 'label': 'Ano de chegada ao Brasil'}
        ],
    },

    'graph_auxilios': {
        'default_level_1': {'value': 'data_inicio_ano_exact', 'label': 'Ano de início'},
        'default_level_2': {'value': 'situacao', 'label': 'Situação'},
        'options': [
            {'value': 'situacao', 'label': 'Situação'},
            {'value': 'data_inicio_ano_exact', 'label': 'Ano de início'},
            {'value': 'bolsas_pt', 'label': 'Bolsa'},
            {'value': 'auxilio_pesquisa_pt', 'label': 'Auxílio a Pesquisa'},
            # {'value':'area_pt', 'label':'Área do conhecimento'},
            # {'value':'convenio_exact', 'label':'Convênio'},
            {'value': 'tipo_convenio_exact', 'label': 'Tipo de convênio'},
            {'value': 'pais_convenio_exact', 'label': 'País de convênio'},
        ]
    },

    'enade': {
        'default_level_1': {'value': 'CO_CATEGAD', 'label': 'IES - Categoria Administrativa'},
        'default_level_2': {'value': 'CO_ORGACAD', 'label': 'IES - Organização Acadêmica'},
        'default_level_3': {'value': 'GEOGRAFICO_facet', 'label': 'ENADE - Região'},
        'options': [{'value': 'CO_ORGACAD', 'label': 'IES - Organização Acadêmica'},
                    {'value': 'UF_CURSO', 'label': 'Curso - UF'},
                    {'value': 'CO_CATEGAD', 'label': 'IES - Categoria Administrativa'},
                    {'value': 'GEOGRAFICO_facet', 'label': 'ENADE - Região'},
                    {'value': 'Ano_facet', 'label': 'Ano Pesquisa - ENADE'},
                    {'value': 'TP_SEXO', 'label': 'Sexo'},
                    {'value': 'Cor_Raca', 'label': 'Cor/Raça'},
                    {'value': 'Estado_Civil', 'label': 'Estado Civil'},
                    {'value': 'Renda_familiar', 'label': 'Renda familiar'},
                    ],

    },

}

BUBBLE_CHART = {
    'inep_docentes': {
        'default_level_1': {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'IES - Categoria Administrativa'},
        'default_level_2': {'value': 'DS_ORGANIZACAO_ACADEMICA', 'label': 'IES - Organização Acadêmica'},
        'default_level_3': {'value': 'NO_REGIAO_IES', 'label': 'IES - Região'},
        'options': [{'value': 'DS_ORGANIZACAO_ACADEMICA', 'label': 'IES - Organização Acadêmica'},
                    {'value': 'SGL_UF_IES', 'label': 'IES - UF'},
                    {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'IES - Categoria Administrativa'},
                    {'value': 'NO_REGIAO_IES', 'label': 'IES - Região'},
                    {'value': 'DS_REGIME_TRABALHO', 'label': 'IES - Regime de trabalho'},
                    {'value': 'IN_BOLSA_PESQUISA', 'label': 'IES - Bolsa pesquisa'},
                    {'value': 'IN_ATU_POS_PRESENCIAL', 'label': 'IES - Pós presencial'},
                    {'value': 'IN_ATU_POS_EAD', 'label': 'IES - Pós EAD'},
                    {'value': 'CO_UF_NASCIMENTO', 'label': 'Docente - UF (código)'},
                    {'value': 'DS_SEXO_DOCENTE', 'label': 'Docente - Sexo'},
                    {'value': 'DS_COR_RACA_DOCENTE', 'label': 'Docente - Cor/Raça'},
                    ],
    },
    'inep_alunos': {
        'default_level_1': {'value': 'NO_OCDE_AREA_GERAL', 'label': 'OCDE - Geral'},
        'default_level_2': {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'IES - Categoria Administrativa'},
        'options': [
            {'value': 'ANO_INGRESSO', 'label': 'Ano de ingresso'},
            {'value': 'DS_TURNO_ALUNO', 'label': 'Turno do aluno'},
            {'value': 'DS_ALUNO_SITUACAO', 'label': 'Situação do aluno'},

            {'value': 'DS_MODALIDADE_ENSINO', 'label': 'Modalidade de ensino'},
            {'value': 'DS_GRAU_ACADEMICO', 'label': 'Grau acadêmico'},
            {'value': 'DS_NIVEL_ACADEMICO', 'label': 'Nível acadêmico'},

            {'value': 'SGL_UF_IES', 'label': 'IES - UF'},
            {'value': 'NO_REGIAO_IES', 'label': 'IES - Região'},
            {'value': 'DS_ORGANIZACAO_ACADEMICA', 'label': 'IES - Organização Acadêmica'},
            {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'IES - Categoria Administrativa'},
            {'value': 'IN_BOLSA_PESQUISA', 'label': 'IES - Bolsa pesquisa'},
            {'value': 'NO_OCDE_AREA_GERAL', 'label': 'OCDE - Geral'},
        ],
    },
    'fazenda_sp': {
        'default_level_1': {'value': 'Fonte_de_Recursos', 'label': 'Fonte de recursos'},
        'default_level_2': {'value': 'Fun__o', 'label': 'Função'},
        'options': [
            {'value': 'Fonte_de_Recursos', 'label': 'Fonte de recursos'},
            {'value': 'UO', 'label': 'UO'},
            {'value': '_rg_o', 'label': 'Orgão'},
            {'value': 'Unidade_Gestora', 'label': 'Unidade Gestora'},
            {'value': 'Fun__o', 'label': 'Função'},
            {'value': 'Sub_Fun__o', 'label': 'Sub Função'},
            {'value': 'Programa', 'label': 'Programa'},
            {'value': 'A__o', 'label': 'Ação'},
            {'value': 'Funcional_Program_tica', 'label': 'Funcional Programática'},
            {'value': 'Elemento', 'label': 'Elemento'}, ],
    },
    'rais': {
        'default_level_1': {'value': 'Escolaridade_ap_s_2005', 'label': 'Escolaridade_ap_s_2005'},
        'default_level_2': {'value': 'Sexo_Trabalhador', 'label': 'Sexo'},
        'options': [
            {'value': 'Sexo_Trabalhador', 'label': 'Sexo'},
            {'value': 'Idade', 'label': 'Idade'},
            {'value': 'Munic_pio', 'label': 'Município'},
            {'value': 'Mun_Trab', 'label': 'Município de Trabalho'},
            {'value': 'Nacionalidade', 'label': 'Nacionalidade'},
            {'value': 'Distritos_SP', 'label': 'Distrito SP'},
            {'value': 'Idade', 'label': 'Idade'},
            {'value': 'Ind_Portador_Defic', 'label': 'Ind_Portador_Defic'},
            {'value': 'Ra_a_Cor', 'label': 'Raça / Cor'},
            {'value': 'Faixa_Et_ria', 'label': 'Faixa Etária'},
            {'value': 'Escolaridade_ap_s_2005', 'label': 'Escolaridade após 2005'},
            {'value': 'Tipo_Defic', 'label': 'Tipo_Defic'},
            {'value': 'Ano_Chegada_Brasil', 'label': 'Ano de chegada ao Brasil'}
        ],
    },
    'graph_auxilios': {
        'default_level_1': {'value': 'data_inicio_ano_exact', 'label': 'Ano de início'},
        'default_level_2': {'value': 'area_pt', 'label': 'Área do conhecimento'},
        'options': [
            {'value': 'situacao', 'label': 'Situação'},
            {'value': 'data_inicio_ano_exact', 'label': 'Ano de início'},
            {'value': 'bolsas_pt', 'label': 'Bolsa'},
            {'value': 'auxilio_pesquisa_pt', 'label': 'Auxílio a Pesquisa'},
            {'value': 'area_pt', 'label': 'Área do conhecimento'},
            {'value': 'convenio_exact', 'label': 'Convênio'},
            {'value': 'tipo_convenio_exact', 'label': 'Tipo de convênio'},
            {'value': 'pais_convenio_exact', 'label': 'País de convênio'},
        ]
    },

    'lattes': {
        'default_level_1': {'value': 'DOUTORADO_GRANDE-AREA-DO-CONHECIMENTO', 'label': ''},
        'default_level_2': {'value': 'DOUTORADO_FLAG-BOLSA', 'label': ''},
        'options': [
            {'value': 'GRADUACAO_ANO-DE-INICIO', 'label': 'Graduação - Ano início'},
            {'value': 'GRADUACAO_ANO-DE-CONCLUSAO', 'label': 'Graduação - Ano conclusão'},
            # {'value':'GRADUACAO_NOME-AGENCIA', 'label':'Graduação - Instituição'},
            {'value': 'GRADUACAO_FLAG-BOLSA', 'label': 'Graduação - Bolsa'},
            {'value': 'MESTRADO_ANO-DE-INICIO', 'label': 'Mestrado - Ano início'},
            {'value': 'MESTRADO_ANO-DE-CONCLUSAO', 'label': 'Mestrado - Ano conclusão'},
            # {'value':'MESTRADO_NOME-AGENCIA', 'label':'Mestrado - Instituição'},
            {'value': 'MESTRADO_FLAG-BOLSA', 'label': 'Mestrado - Bolsa'},
            {'value': 'MESTRADO_GRANDE-AREA-DO-CONHECIMENTO', 'label': 'Mestrado - Área do conhecimento'},
            {'value': 'DOUTORADO_ANO-DE-INICIO', 'label': 'Doutorado - Ano Início'},
            {'value': 'DOUTORADO_ANO-DE-CONCLUSAO', 'label': 'Doutorado - Ano conclusão'},
            # {'value':'DOUTORADO_NOME-AGENCIA', 'label':'Doutorado - Instituição'},
            {'value': 'DOUTORADO_FLAG-BOLSA', 'label': 'Doutorado - Bolsa'},
            {'value': 'DOUTORADO_GRANDE-AREA-DO-CONHECIMENTO', 'label': 'Doutorado - Área do conhecimento'},
        ],
    },

    'enade': {
        'default_level_1': {'value': 'CO_CATEGAD', 'label': 'IES - Categoria Administrativa'},
        'default_level_2': {'value': 'CO_ORGACAD', 'label': 'IES - Organização Acadêmica'},
        'default_level_3': {'value': 'GEOGRAFICO_facet', 'label': 'ENADE - Região'},
        'options': [{'value': 'CO_ORGACAD', 'label': 'IES - Organização Acadêmica'},
                    {'value': 'UF_CURSO', 'label': 'Curso - UF'},
                    {'value': 'CO_CATEGAD', 'label': 'IES - Categoria Administrativa'},
                    {'value': 'GEOGRAFICO_facet', 'label': 'ENADE - Região'},
                    {'value': 'Ano_facet', 'label': 'Ano Pesquisa - ENADE'},
                    {'value': 'TP_SEXO', 'label': 'Sexo'},
                    {'value': 'Cor_Raca', 'label': 'Cor/Raça'},
                    {'value': 'Estado_Civil', 'label': 'Estado Civil'},
                    {'value': 'Renda_familiar', 'label': 'Renda familiar'},
                    ],

    },
}

"""
Dicts to configure Multilevel Charts.
'<collection>':{
    'default_level_1':'',
    'default_level_2':'',
    'y_axis':[
        {'value':'', 'label':''}
    ],
    'y_stratification':[
        {'value':'', 'label':''}
    ],
}
"""
MULTILEVEL_BARCHART_1 = {
    'graph_auxilios': {
        'default_level_1': 'area_pt',
        'default_level_2': 'ano_exact',
        'y_axis': [
            {'value': 'situacao', 'label': 'Situação'},
            {'value': 'bolsas_pt', 'label': 'Bolsas'},
            {'value': 'auxilio_pesquisa_pt', 'label': 'Auxílios'},
            {'value': 'area_pt', 'label': 'Área do conhecimento'},
            {'value': 'entidade_exact', 'label': 'Instituição'},
            {'value': 'programa_tema_pt', 'label': 'Programa Tema'},
            {'value': 'programa_aplicacao_pt', 'label': 'Programa Aplicação'},
            {'value': 'programa_percepcao_pt', 'label': 'Programa Percepção'},
            {'value': 'programa_infra_pt', 'label': 'Programa Infra'},
            {'value': 'tipo_convenio_exact', 'label': 'Tipo Convênio'},
            {'value': 'convenio_exact', 'label': 'Convênio/Acordo'},
            {'value': 'pais_convenio_exact', 'label': 'País convênio'},
            {'value': 'pais_colaboracao_exact', 'label': 'Colaboração no país'},
            {'value': 'cidade_colaboracao_exact', 'label': 'Colaboração na cidade'},
            {'value': 'cidade_exact', 'label': 'Cidade'},
            {'value': 'ano_exact', 'label': 'Ano'}
        ],
        'y_stratification': [
            {'value': 'situacao', 'label': 'Situação'},
            {'value': 'bolsas_pt', 'label': 'Bolsas'},
            {'value': 'auxilio_pesquisa_pt', 'label': 'Auxílios'},
            {'value': 'area_pt', 'label': 'Área do conhecimento'},
            {'value': 'entidade_exact', 'label': 'Instituição'},
            {'value': 'programa_tema_pt', 'label': 'Programa Tema'},
            {'value': 'programa_aplicacao_pt', 'label': 'Programa Aplicação'},
            {'value': 'programa_percepcao_pt', 'label': 'Programa Percepção'},
            {'value': 'programa_infra_pt', 'label': 'Programa Infra'},
            {'value': 'tipo_convenio_exact', 'label': 'Tipo Convênio'},
            {'value': 'convenio_exact', 'label': 'Convênio/Acordo'},
            {'value': 'pais_convenio_exact', 'label': 'País convênio'},
            {'value': 'pais_colaboracao_exact', 'label': 'Colaboração no país'},
            {'value': 'cidade_colaboracao_exact', 'label': 'Colaboração na cidade'},
            {'value': 'cidade_exact', 'label': 'Cidade'},
            {'value': 'ano_exact', 'label': 'Ano'}
        ]
    },

    'bv_memoria': {
        'default_level_1': 'ano_publicacao',
        'default_level_2': 'ano_publicacao',
        'y_axis': [
            {'value': 'ano_publicacao', 'label': 'Ano de publicacao'},
        ],
        'y_stratification': [
            {'value': 'area_conhecimento', 'label': 'Área do conhecimento'},
            {'value': 'ano_publicacao', 'label': 'Ano de publicacao'},
        ],
    },

    'wos': {
        'default_level_2': 'times-cited',
        'default_level_1': 'language',
        'y_axis': [
            {'value': 'times-cited', 'label': 'Número de citações'},
            {'value': 'number-of-cited-references', 'label': 'Número de referências citadas'},
            {'value': 'publisher_journal_volume', 'label': 'publisher_journal_volume'},
            {'value': 'research-areas', 'label': 'research-areas'},

        ],
        'y_stratification': [
            {'value': 'language', 'label': 'Língua'},
        ],
    },

    'rais': {
        'default_level_1': 'Ra_a_Cor',
        'default_level_2': 'Escolaridade_ap_s_2005',
        'y_axis': [
            {'value': 'Sexo_Trabalhador', 'label': 'Sexo'},
            {'value': 'Idade', 'label': 'Idade'},
            {'value': 'Ra_a_Cor', 'label': 'Raça / Cor'},
            {'value': 'Munic_pio', 'label': 'Município'},
            {'value': 'Mun_Trab', 'label': 'Município de Trabalho'},
            {'value': 'Distritos_SP', 'label': 'Distrito SP'},
            {'value': 'Idade', 'label': 'Idade'},
            {'value': 'Faixa_Et_ria', 'label': 'Faixa Etária'},
            {'value': 'Escolaridade_ap_s_2005', 'label': 'Escolaridade após 2005'},
            {'value': 'Tipo_Defic', 'label': 'Tipo_Defic'},
            {'value': 'Ano_Chegada_Brasil', 'label': 'Ano de chegada ao Brasil'}
        ],
        'y_stratification': [
            {'value': 'Sexo_Trabalhador', 'label': 'Sexo'},
            {'value': 'Idade', 'label': 'Idade'},
            {'value': 'Nacionalidade', 'label': 'Nacionalidade'},
            {'value': 'Idade', 'label': 'Idade'},
            {'value': 'Ind_Portador_Defic', 'label': 'Ind_Portador_Defic'},
            {'value': 'Ra_a_Cor', 'label': 'Raça / Cor'},
            {'value': 'Escolaridade_ap_s_2005', 'label': 'Escolaridade após 2005'},
            {'value': 'Tipo_Defic', 'label': 'Tipo_Defic'},
        ],
    },

    'fazenda_sp': {
        'default_level_1': 'Fun__o',
        'default_level_2': 'Fonte_de_Recursos',
        'y_axis': [
            {'value': 'Fonte_de_Recursos', 'label': 'Fonte de recursos'},
            {'value': 'UO', 'label': 'UO'},
            {'value': '_rg_o', 'label': 'Orgão'},
            {'value': 'Unidade_Gestora', 'label': 'Unidade Gestora'},
            {'value': 'Fun__o', 'label': 'Função'},
            {'value': 'Sub_Fun__o', 'label': 'Sub Função'},
            {'value': 'Programa', 'label': 'Programa'},
            {'value': 'A__o', 'label': 'Ação'},
            {'value': 'Funcional_Program_tica', 'label': 'Funcional Programática'},
            {'value': 'Elemento', 'label': 'Elemento'},
            # {'value':'Dota__o_Atual', 'label': 'Dotação Atual'},
            # {'value':'Empenhado', 'label': 'Empenhado'},
            # {'value':'Liquidado', 'label': 'Liquidado'},

        ],
        'y_stratification': [
            {'value': 'Fonte_de_Recursos', 'label': 'Fonte de recursos'},
            {'value': 'UO', 'label': 'UO'},
            {'value': '_rg_o', 'label': 'Orgão'},
            {'value': 'Unidade_Gestora', 'label': 'Unidade Gestora'},
            {'value': 'Fun__o', 'label': 'Função'},
            {'value': 'Sub_Fun__o', 'label': 'Sub Função'},
            {'value': 'Programa', 'label': 'Programa'},
            {'value': 'A__o', 'label': 'Ação'},
            {'value': 'Funcional_Program_tica', 'label': 'Funcional Programática'},
            {'value': 'Elemento', 'label': 'Elemento'},
            # {'value':'Dota__o_Inicial', 'label': 'Dotação Inicial'},
            # {'value':'Dota__o_Atual', 'label': 'Dotação Atual'},
            # {'value':'Empenhado', 'label': 'Empenhado'},
            # {'value':'Liquidado', 'label': 'Liquidado'},
        ],
    },

    #
    'pesquisa_pipe': {
        'default_level_1': 'socio_f_aport_ANTES1_ApFinEmp_valor',
        'default_level_2': 'pess_escolaridade',
        'y_axis': [
            {'value': 'pess_escolaridade', 'label': 'Escolaridade'},
            {'value': 'pess_formacao', 'label': 'Formacao Gestao'},
            {'value': 'resu_chegou_a_resultados', 'label': 'Resultados alcançados'},
            {'value': 'esfo_ANTES1_valor_decorrencia_pipe', 'label': 'esfo_ANTES1_valor_decorrencia_pipe - Antes 1'},
            {'value': 'esfo_ANTES2_valor_decorrencia_pipe', 'label': 'esfo_ANTES2_valor_decorrencia_pipe - Antes 2'},
            {'value': 'esfo_DURANTE1_valor_decorrencia_pipe',
             'label': 'esfo_DURANTE1_valor_decorrencia_pipe - Durante 1'},
            {'value': 'esfo_DURANTE2_valor_decorrencia_pipe',
             'label': 'esfo_DURANTE2_valor_decorrencia_pipe - Durante 2'},
            {'value': 'esfo_DEPOIS1_valor_decorrencia_pipe',
             'label': 'esfo_DEPOIS1_valor_decorrencia_pipeo - Depois 1'},
            {'value': 'esfo_DEPOIS2_valor_decorrencia_pipe', 'label': 'esfo_DEPOIS2_valor_decorrencia_pipe - Depois 2'},
        ],
        'y_stratification': [
            {'value': 'pess_escolaridade', 'label': 'Escolaridade'},
            {'value': 'pess_formacao', 'label': 'Formacao Gestao'},
            {'value': 'socio_f_aport_ANTES1_ApFinEmp_valor', 'label': 'Aporte financeiro - Antes 1'},
            {'value': 'socio_f_aport_ANTES1_ApFinEmp_valor', 'label': 'Aporte financeiro - Antes 2'},
            {'value': 'socio_f_aport_DURANTE1_ApFinEmp_valor', 'label': 'Aporte financeiro - Durante 1'},
            {'value': 'socio_f_aport_DURANTE2_ApFinEmp_valor', 'label': 'Aporte financeiro - Durante 2'},
            {'value': 'socio_f_aport_DEPOIS1_ApFinEmp_valor', 'label': 'Aporte financeiro - Depois 1'},
            {'value': 'socio_f_aport_DEPOIS2_ApFinEmp_valor', 'label': 'Aporte financeiro - Depois 2'},

            {'value': 'iden_participacao_capital_estrangeiro', 'label': 'Participação de capital estrangeiro'},
            {'value': 'resu_chegou_a_resultados', 'label': 'Resultados alcançados'},
        ],
    },

    'inep_docentes': {
        'default_level_1': 'DS_ORGANIZACAO_ACADEMICA',
        'default_level_2': 'ano_vigencia_inep',
        'y_axis': [
            {'value': 'ano_vigencia_inep', 'label': 'Ano da pesquisa'},
            {'value': 'NO_MANTENEDORA', 'label': 'Mantenedora'},
            {'value': 'SGL_UF_IES', 'label': 'Estado da sede administrativa'},
            {'value': 'NO_REGIAO_IES', 'label': 'Região da sede administrativa'},
            {'value': 'DS_CATEGORIA_ADMINISTRATIVA', 'label': 'Categoria administrativa'},

        ],
        'y_stratification': [
            {'value': 'DS_ORGANIZACAO_ACADEMICA', 'label': 'Organização acadêmica'},
            {'value': 'DS_NACIONALIDADE_DOCENTE', 'label': 'Nacionalidade'},
            {'value': 'CO_UF_NASCIMENTO', 'label': 'Estado natal'},
            {'value': 'DS_SEXO_DOCENTE', 'label': 'Sexo'},
            {'value': 'DS_COR_RACA_DOCENTE', 'label': 'Cor/Raça'},
            {'value': 'DS_NACIONALIDADE_DOCENTE', 'label': 'Nacionalidade'},
            {'value': 'CO_ESCOLARIDADE_DOCENTE', 'label': 'Escolaridade'},
            {'value': 'IN_DOCENTE_DEFICIENCIA', 'label': 'Deficiência física'},
            {'value': 'DS_REGIME_TRABALHO', 'label': 'Regime de trabalho'},
        ],
    },

    'inep_alunos': {
        'default_level_1': 'DS_TURNO_ALUNO',
        'default_level_2': 'ano_vigencia_inep',
        'y_axis': [
            {'value': 'ano_vigencia_inep', 'label': 'Ano da pesquisa'},
            {'value': 'NO_MANTENEDORA', 'label': 'Mantenedora'},
            {'value': 'SGL_UF_IES', 'label': 'Estado da sede administrativa'},
            {'value': 'NO_REGIAO_IES', 'label': 'Região da sede administrativa'},

        ],
        'y_stratification': [
            {'value': 'ANO_INGRESSO', 'label': 'Ano de ingresso'},
            {'value': 'DS_NIVEL_ACADEMICO', 'label': 'Nível acadêmico'},
            {'value': 'DS_GRAU_ACADEMICO', 'label': 'Grau acadêmico'},
            {'value': 'IN_ACESSO_PORTAL_CAPES', 'label': 'Acesso ao portal Capes'},
            {'value': 'DS_MODALIDADE_ENSINO', 'label': 'Modalidade de ensino'},
            {'value': 'QT_CARGA_HORARIA_INTEG', 'label': 'Carga horária'},
            {'value': 'DS_TURNO_ALUNO', 'label': 'Turno'},
            {'value': 'DS_ALUNO_SITUACAO', 'label': 'Situação do aluno'},

        ],
    },

    'bv_empresas': {
        'default_level_1': 'municipio_cpd',
        'default_level_2': 'ano_primeiro_processo',
        'y_axis': [
            {'value': 'ano_primeiro_processo', 'label': 'Entrada no Programa PIPE'},
            {'value': 'lista_cnae', 'label': 'CNAE'},
            {'value': 'municipio_cpd', 'label': 'Municipio'},

        ],
        'y_stratification': [
            {'value': 'lista_cnae', 'label': 'CNAE'},
            {'value': 'municipio_cpd', 'label': 'Municipio'},
        ],
    },

    'bv_pesquisadores': {
        'default_level_1': 'sexo',
        'default_level_2': 'quantidade_processos',
        'y_axis': [
            {'value': 'nacionalidade', 'label': 'Nacionalidade'},
            {'value': 'instituicao_afiliacao_exact', 'label': 'Instituição de afiliação'},
            {'value': 'quantidade_processos', 'label': 'Quantidade de processos'},
        ],
        'y_stratification': [
            {'value': 'nacionalidade', 'label': 'Nacionalidade'},
            {'value': 'quantidade_processos', 'label': 'Quantidade de processos'},
            {'value': 'sexo', 'label': 'Gênero'},
        ],
    },

    'memoria_autoria': {
        'default_level_1': 'autor_exact',
        'default_level_2': 'pais_list_exact',
        'y_axis': [
            {'value': 'autor_exact', 'label': 'Autor'},
            {'value': 'instituicao_list_exact', 'label': 'Instituição'},
        ],
        'y_stratification': [
            {'value': 'pais_list_exact', 'label': 'País'},
            {'value': 'instituicao_list_exact', 'label': 'Instituição'},
        ],
    },

    'lattes': {
        'default_level_1': 'GRADUACAO_FLAG-BOLSA',
        'default_level_2': 'GRADUACAO_ANO-DE-INICIO',
        'y_axis': [
            {'value': 'GRADUACAO_ANO-DE-INICIO', 'label': 'Graduação - Ano início'},
            {'value': 'GRADUACAO_ANO-DE-CONCLUSAO', 'label': 'Graduação - Ano conclusão'},
            # {'value':'GRADUACAO_NOME-AGENCIA', 'label':'Graduação - Instituição'},
            {'value': 'MESTRADO_ANO-DE-INICIO', 'label': 'Mestrado - Ano início'},
            {'value': 'MESTRADO_ANO-DE-CONCLUSAO', 'label': 'Mestrado - Ano conclusão'},
            # {'value':'MESTRADO_NOME-AGENCIA', 'label':'Mestrado - Instituição'},
            {'value': 'MESTRADO_GRANDE-AREA-DO-CONHECIMENTO', 'label': 'Mestrado - Área do conhecimento'},
            {'value': 'DOUTORADO_ANO-DE-INICIO', 'label': 'Doutorado - Ano Início'},
            {'value': 'DOUTORADO_ANO-DE-CONCLUSAO', 'label': 'Doutorado - Ano conclusão'},
            # {'value':'DOUTORADO_NOME-AGENCIA', 'label':'Doutorado - Instituição'},
            {'value': 'DOUTORADO_GRANDE-AREA-DO-CONHECIMENTO', 'label': 'Doutorado - Área do conhecimento'},
        ],
        'y_stratification': [
            # {'value':'GRADUACAO_NOME-AGENCIA', 'label':'Graduação - Agência'},
            {'value': 'GRADUACAO_FLAG-BOLSA', 'label': 'Graduação - Bolsa'},
            # {'value':'MESTRADO_NOME-AGENCIA', 'label':'Mestrado - Agência'},
            {'value': 'MESTRADO_FLAG-BOLSA', 'label': 'Mestrado - Bolsa'},
            # {'value':'DOUTORADO_NOME-AGENCIA', 'label':'Doutorado - Agência'},
            {'value': 'DOUTORADO_FLAG-BOLSA', 'label': 'Doutorado - Bolsa'},
        ],
    },

    'enade': {
        'default_level_1': 'CO_CATEGAD',
        'default_level_2': 'NU_ANO',
        'y_axis': [
            {'value': 'CO_CATEGAD', 'label': 'Categoria Administrativa IES'},
            {'value': 'NU_ANO', 'label': 'Ano da pesquisa'},
            {'value': 'GEOGRAFICO_facet', 'label': 'Região da pesquisa'},
            {'value': 'ANO_FIM_2G_facet', 'label': 'Ano fim do 2° grau'},
            {'value': 'ANO_IN_GRAD_facet', 'label': 'Ano fim da graduação'},
            {'value': 'Renda_familiar', 'label': 'Renda Familiar'},

        ],
        'y_stratification': [
            {'value': 'CO_ORGACAD', 'label': 'Categoria da organização acadêmica'},
            {'value': 'CO_GRUPO', 'label': 'Área de enquadramento do curso no Enade'},
            {'value': 'TP_SEXO', 'label': 'Sexo'},
            {'value': 'Estado_Civil', 'label': 'Estado Civil'},
            {'value': 'Cor_Raca', 'label': 'Cor/Raça'},
            {'value': 'Renda_familiar', 'label': 'Renda Familiar'},

        ],
    },
}

"""
Nodes relashionships

The fields "one" and "many" set on the dict bellow are used on the
following fields to search on Solr:
'fl':'numero_processo, projetos_pai_np, id',
'sort':'numero_processo asc',
'cartesianProduct':'projetos_pai_np',
'fq':'projetos_pai_np:*',
'join':{
    'hashJoin':'numero_processo=projetos_pai_np',
},
"""

EDGES = {
    'graph_auxilios': {
        'collection': 'graph_auxilios',
        'vertices': {
            'graph_auxilios': {
                'collection': 'graph_auxilios',
                'relationship_type': 'one_to_many',
                'one': 'numero_processo',
                'many': 'projetos_pai_np',
                'label': 'Projetos Vinculados (Auxílios e Bolsas)'
            },
            'bv_memoria': {
                'collection': 'bv_memoria',
                'relationship_type': 'one_to_many',
                'one': 'numero_processo',
                'many': 'numero_processos',
                'label': 'Publicações Científicas'
            },
            'bv_empresas': {
                'collection': 'bv_empresas',
                'relationship_type': 'one_to_many',
                'one': 'numero_processo',
                'many': 'numero_processos',
                'label': 'Empresas do PIPE'
            },
            'bv_pesquisadores': {
                'collection': 'bv_pesquisadores',
                'relationship_type': 'many_to_one',
                'one': 'django_id',
                'many': 'id_pesquisador',
                'label': 'Pesquisadores (responsável e beneficiário)'
            },
        },

    },

    # Estah definido, mas nao estah configurado corretamente.
    # Eh soh uma copia do edge de graph_auxilios, mas sem configurar.

    'bv_memoria': {
        'collection': 'bv_memoria',
        # 'fl':'numero_processo',
        # 'sort':'numero_processo asc',
        'vertices': {
            'memoria_autoria': {
                'collection': 'memoria_autoria',
                'relationship_type': 'many_to_one',
                'one': 'django_id',
                'many': 'id_autorias',
                'label': 'Autorias de Publicações Científicas'
            },
        },
    },
    'memoria_autoria': {
        'collection': 'bv_memoria',
        # 'sort':'numero_processo asc',
        'vertices': {
        },
    },
    'enade': {
        'collection': 'enade',
        # 'sort':'numero_processo asc',
        'vertices': {
        },
    },

    'rais': {
        'collection': 'rais',
        # 'sort':'numero_processo asc',
        'vertices': {
        },
    },
    'fazenda_sp': {
        'collection': 'fazenda_sp',
        # 'sort':'numero_processo asc',
        'vertices': {
        },
    },

    'pesquisa_pipe': {
        'collection': 'pesquisa_pipe',
        # 'sort':'numero_processo asc',
        'vertices': {
            'graph_auxilios': {
                'collection': 'graph_auxilios',
                'relationship_type': 'many_to_one',
                'one': 'numero_processo',
                'many': 'numero_processo',
                'label': 'Processos (Auxilios e Bolsas)'
            },
        },

    },
    'bv_empresas': {
        'collection': 'bv_empresas',
        # 'fl':'razao_social',
        # 'sort':'razao_social asc',
        'vertices': {
            'graph_auxilios': {
                'collection': 'graph_auxilios',
                'relationship_type': 'many_to_one',
                'one': 'numero_processo',
                'many': 'numero_processos',
                'label': 'Processos (Auxilios e Bolsas)'
            },
        },

    },
    'bv_pesquisadores': {
        'collection': 'bv_pesquisadores',
        # 'fl':'django_id',
        # 'sort':'django_id asc',
        'vertices': {
            'graph_auxilios': {
                'collection': 'graph_auxilios',
                'relationship_type': 'one_to_many',
                'one': 'django_id',
                'many': 'id_pesquisador',
                'label': 'Projetos (Auxílios e Bolsas)'
            },
            'lattes': {
                'collection': 'lattes',
                'relationship_type': 'one_to_many',
                'one': 'django_id',
                'many': 'ID',
                'label': 'Lattes'
            },
        },
    },

    'inep_docentes': {
        'collection': 'inep_docentes',
        # 'sort':'numero_processo asc',
        'vertices': {
        },
    },

    'inep_alunos': {
        'collection': 'inep_alunos',
        'vertices': {
        },
    },
    'lattes': {
        'collection': 'lattes',
        # 'sort':'numero_processo asc',
        'vertices': {
        },
    },

    'wos': {
        'collection': 'wos',
        'vertices': {
        },
    },

}

print(generate_edges(BV_GRAPH))
