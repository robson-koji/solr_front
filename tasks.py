# -*- coding: utf-8 -*-

import requests
import logging
import pandas
import uuid
import csv
import os
import tempfile
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from solr_front import settings_sf

from django.conf import settings
# from bv.celery import app
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def add(x, y):
    return x + y


@shared_task
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
        related_collection_json = requests.get(url).json()

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
                    'id': doc['id'],
                    campo: {operador: hash_querybuilder}
                })
        return json_ids

    # Indexa atomicamente (cria campos dinamicos nos documentos enviados em jsons_ids)
    json_ids = monta_json_para_update(campo_dinamico_busca, 'add')
    update_url = settings_sf.SOLR_URL + collection2 + '/update?commit=true'

    response = requests.post(update_url, json=json_ids)

    # import pdb; pdb.set_trace()
    if not response.status_code == 200:
        raise Exception('HTTP CODE ', response.status_code)


@shared_task
def makeCsv(se, collection, nome, email, para, msg, column_names=''):
    """ This function is used when a pre-indexed report field exists """

    # Get data on Solr.
    se = se.replace('%', '%25')
    solr_url = settings_sf.SOLR_URL + collection + '/stream?expr=' + se
    response = requests.get(solr_url)
    data_list = response.json()['result-set']['docs']

    if not 'EOF' in data_list[-1]:
        raise exception
    else:
        del data_list[-1]

    if not response.status_code == 200:
        logger.error("---------------------------\n")
        logger.error(
            "Solr HTTP Response ERROR: %s ( %s ). Method: %s" % (
            response.status_code, response.reason, "tasks.py makeCsv"))
        logger.error("For HTTP 400 Solr log used to tell what is wrong with the request.")
        logger.error("Solr URL Error: %s \n" % (solr_url))
        logger.error("---------------------------\n")

    if '"EXCEPTION":' in response.content:
        logger.error("---------------------------\n")
        logger.error(
            "Solr HTTP Response ERROR: %s. Method: %s" % (response.content, "tasks.py makeCsv"))
        logger.error("For HTTP 400 Solr log used to tell what is wrong with the request.")
        logger.error("Solr URL Error: %s \n" % (solr_url))
        logger.error("---------------------------\n")

    # Handle filesystem to store csv file and write de file
    rel_path = os.path.relpath(settings_sf.DOWNLOAD_FILES)
    arquivo_csv = str(uuid.uuid4()) + '.csv'
    abspath_arquivo_csv = os.path.join(settings_sf.DOWNLOAD_FILES, arquivo_csv)
    url_csv = os.path.join(settings_sf.DOWNLOAD_FILES_URL, arquivo_csv)
    with open(abspath_arquivo_csv, 'w+') as csv_file:
        csv_file.write(u'\ufeff'.encode('utf8'))
        if column_names:
            csv_file.write(";".join(cn.encode('utf-8') for cn in column_names) + '\n')
        for dl in data_list:
            # import pdb; pdb.set_trace()
            csv_file.write(dl['csv'].encode('utf-8'))
            csv_file.write('\n')

    # Assembly and send email.
    assunto = u'Exportação em Excel (CSV)'
    corpo = nome + u' (' + email + u') ' + u'enviou um arquivo em Excel (CSV) com os resultados de sua pesquisa' + u'.\n\n'
    corpo += u'Clique no link para baixar o arquivo em Excel (CSV)' + u':\n' + url_csv + u'\n\n' + u'O arquivo ficará disponível por 02 dias' + u'.\n\n'
    if msg:
        corpo += u'Comentários' + u': ' + msg + u'\n\n'
    corpo = corpo.encode('utf-8')
    send_mail(assunto, corpo, settings_sf.MAIL_SENDER, [para])


@shared_task
def makeData(data_list, nome, email, para, msg, fields, formato, column_names):
    # import pdb;pdb.set_trace()
    arquivo_name = str(uuid.uuid4())
    if isinstance(data_list, list) or isinstance(data_list, dict):
        data_frame = pandas.DataFrame(data_list)
        # ordena colunas conforme sequencia definida no conf
        try:
            data_frame.drop(columns=['EOF', 'RESPONSE_TIME'], inplace=True, errors='ignore')
        except:
            pass
        # data_frame = data_frame.reindex(columns=fields)

        # gera nome do arquivo usando uuid

        rel_path = os.path.relpath(settings_sf.DOWNLOAD_FILES)
        if not column_names:
            column_names = list(data_frame.columns)

        if formato == 'json':
            arquivo_name += '.json'
            data_frame.to_json(os.path.join(settings_sf.DOWNLOAD_FILES, arquivo_name))
        elif formato == 'csv':
            arquivo_name += '.csv'
            data_frame.to_csv(os.path.join(settings_sf.DOWNLOAD_FILES, arquivo_name), sep=';', encoding='utf-8-sig',
                              index=False)  # ,columns=fields, )
        elif formato == 'excel':
            arquivo_name += '.xls'
            data_frame.to_excel(os.path.join(settings_sf.DOWNLOAD_FILES, arquivo_name), index=False)
    else:
        try:
            import ijson
            parser = ijson.items(open(data_list.name, 'rb'), 'result-set.docs.item')
            # parser = ijson.parse(open(data_list.name,'rb'))
            c = 0
            arquivo_name += '.csv'
            with open(os.path.join(settings_sf.DOWNLOAD_FILES, arquivo_name), 'wb') as output_file:
                print 'Criando CSV %s em: %s' % (arquivo_name, settings_sf.DOWNLOAD_FILES)

                output_file.write(u'\ufeff'.encode('utf8'))
                for i in parser:
                    dic_linha = dict(i)
                    if c == 0:
                        keys = fields
                        dict_writer = csv.DictWriter(output_file, keys, extrasaction='ignore', delimiter=';')
                        dict_writer.writeheader()

                    if 'EOF' not in dic_linha.keys():
                        dic_linha_f = {}
                        for k, v in dic_linha.items():
                            # import pdb; pdb.set_trace()
                            if isinstance(dic_linha[k], list):
                                dic_linha_f[k] = '|'.join(v).encode('utf8')
                            else:
                                dic_linha_f[k] = ''.join([str(v)]).encode('utf8')
                        dict_writer.writerow(dic_linha_f)

                    c += 1

        except Exception as exc:
            raise exc

        try:
            os.remove(data_list)
        except:
            pass

    url_file = os.path.join(settings_sf.DOWNLOAD_FILES_URL, arquivo_name)
    abspath_arquivo = os.path.join(settings_sf.DOWNLOAD_FILES, arquivo_name)
    # send mail
    assunto = u'Exportação em Excel (CSV)'
    corpo = nome + u' (' + email + u') ' + u'enviou um arquivo em Excel (CSV) com os resultados de sua pesquisa' + u'.\n\n'

    corpo += u'Clique no link para baixar o arquivo em Excel (CSV)' + u':\n' + url_file + u'\n\n' + u'O arquivo ficará disponível por 02 dias' + u'.\n\n'
    if msg:
        corpo += u'Comentários' + u': ' + msg + u'\n\n'
    corpo += u'TESTE'
    corpo = corpo.encode('utf-8')

    send_mail(assunto, corpo, settings_sf.MAIL_SENDER, [para])
