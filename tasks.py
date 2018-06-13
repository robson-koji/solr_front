# -*- coding: utf-8 -*-

import csv
import requests
import os
import pandas
from solrfront.celery import app

from solrfront import settings

from django.core.mail import send_mail
from django.utils.translation import ugettext as _

import uuid


@app.task
def add(x, y):
    # send_mail('teste', 'teste', 'cdi2@fapesp.br', ['hconzatti@fapesp.br'])
    return x + y


@app.task
def update_atomico(url, collection2, campo_dinamico_busca, hash_querybuilder):
    """
    Faz update atomico da collection solicitada
    Recebe uma lista e manda de uma vez para o Solr, que cuida fazer o update
    no documento, criando ou excluindo o campo enviando no "jsons_ids".
    """


    def monta_json_para_update(campo, operador):
        """
        :param valor_campo: utilizado para criar ou excluir campo dinamico no Solr
        :type valor_campo: Tipo string. Valores aceitos sao 'true' e vazio
        """
        # Executa o request no Solr e recupera o json.
        related_collection_json =  requests.get(url).json()

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
                    campo:{operador:hash_querybuilder}
                })
        return json_ids

    # Indexa atomicamente (cria campos dinamicos nos documentos enviados em jsons_ids)
    json_ids = monta_json_para_update(campo_dinamico_busca, 'add')
    update_url = 'http://192.168.0.212/solr/' + collection2 + '/update?commit=true'


    response = requests.post(update_url, json=json_ids)

    # import pdb; pdb.set_trace()
    if not response.status_code == 200:
        raise Exception('HTTP CODE ', response.status_code)


@app.task
def makeCsv(data_list, nome, email, para, msg, fields):


    # Check last element of the list of objects to ensure read all documents.
    if not 'EOF' in data_list[-1]:
        pass
    else:
        del data_list[-1] # Remove EOF element.


        # Para isso funcionar, os outros elementos nao podem ter mais chaves que o inicial.
        if fields:
            keys = fields
        else:
            keys = data_list[0].keys()

        rel_path = os.path.relpath(settings.EXPORTACAO_CSV_PATH, settings.MEDIA_ROOT)

        # gera nome do arquivo usando uuid
        arquivo_csv = str(uuid.uuid4())+'.csv'

        url_csv = os.path.join(settings.MEDIA_URL, rel_path, arquivo_csv)

        abspath_arquivo_csv = os.path.join(settings.EXPORTACAO_CSV_PATH, arquivo_csv)

        csv.register_dialect('excel-export', delimiter=';', quoting=csv.QUOTE_NONE, escapechar='\\')

        with open(abspath_arquivo_csv, 'wb') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys, dialect='excel-export')
            dict_writer.writeheader()
            for data_dict in data_list:
                # import pdb; pdb.set_trace()
                dict_writer.writerow(data_dict)


        # send mail
        assunto = u'Biblioteca Virtual da FAPESP - Exportação em Excel (CSV)'
        corpo = nome + u' (' + email + u') ' +u'enviou um arquivo em Excel (CSV) com os resultados de sua pesquisa'+u'.\n\n'

        corpo += u'Clique no link para baixar o arquivo em Excel (CSV)'+u':\n' + url_csv + u'\n\n'+u'O arquivo ficará disponível por 02 dias'+u'.\n\n'
        if msg:
            corpo += u'Comentários'+u': ' + msg + u'\n\n'
        corpo += u'Biblioteca Virtual da FAPESP'+u'\nwww.bv.fapesp.br'
        corpo = corpo.encode('utf-8')


        send_mail(assunto, corpo, 'cdi2@fapesp.br', [para])

@app.task
def makeData(data_list, nome, email, para, msg, fields, formato):

    data_frame = pandas.DataFrame(data_list)
    #ordena colunas conforme sequencia definida no conf
    data_frame.drop(columns=['EOF', 'RESPONSE_TIME'], inplace=True)

    data_frame = data_frame.reindex(columns=fields)
    # gera nome do arquivo usando uuid
    arquivo_name = str(uuid.uuid4())

    rel_path = os.path.relpath(settings.EXPORTACAO_CSV_PATH, settings.MEDIA_ROOT)

    if formato == 'json':
        arquivo_name += '.json'
        data_frame.to_json( os.path.join(settings.EXPORTACAO_CSV_PATH, arquivo_name) )
    elif formato == 'csv':
        arquivo_name += '.csv'
        data_frame.to_csv( os.path.join(settings.EXPORTACAO_CSV_PATH, arquivo_name) , index = False)
    elif formato  == 'excel':
        arquivo_name += '.xls'
        data_frame.to_excel( os.path.join(settings.EXPORTACAO_CSV_PATH, arquivo_name),index = False )



    url_file = os.path.join(settings.MEDIA_URL,rel_path, arquivo_name)
    abspath_arquivo = os.path.join(settings.EXPORTACAO_CSV_PATH, arquivo_name)
    # send mail
    assunto = u'Biblioteca Virtual da FAPESP - Exportação em Excel (CSV)'
    corpo = nome + u' (' + email + u') ' +u'enviou um arquivo em Excel (CSV) com os resultados de sua pesquisa'+u'.\n\n'

    corpo += u'Clique no link para baixar o arquivo em Excel (CSV)'+u':\n' + url_file + u'\n\n'+u'O arquivo ficará disponível por 02 dias'+u'.\n\n'
    if msg:
        corpo += u'Comentários'+u': ' + msg + u'\n\n'
    corpo += u'Biblioteca Virtual da FAPESP'+u'\nwww.bv.fapesp.br'
    corpo = corpo.encode('utf-8')


    send_mail(assunto, corpo, 'cdi2@fapesp.br', [para])
