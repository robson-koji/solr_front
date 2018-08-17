========================
Instalação do Solr Front
========================

Abaixo estão documentados os procedimentos para instalação do Sistema BV.
Esta etapa leva em consideração que os :ref:`softwares pré-requisitos <pre-requisitos>`
já foram instalados.


Preparação do Ambiente Virtual
==============================

Os módulos que o Sistema da BV faz uso, assim como o próprio interpretador Python, ficarão
disponíveis para o projeto do Sistema da BV através de um ambiente virtual, que deve ser criado com
o comando abaixo::

	mkvirtualenv bv


Com o Ambiente Virtual criado, é necessário informar ao sistema que devemos trabalhar no escopo do
projeto BV. Dessa forma, execute o comando::

	workon bv


Em seguida, uma vez dentro da pasta do Sistema BV, executar o comando abaixo para instalar os módulos
Python que o projeto faz uso::

	pip install -r requirements.txt


Configuração do Sistema BV
==========================

O arquivo de configuração do projeto está localizado em ``bv/settings.py``. Abaixo estão detalhadas
as constantes que precisam ser adequadas de acordo com o servidor do projeto.

* ADMINS_
* ALLOWED_HOSTS_
* DEFAULT_FROM_EMAIL_
* PROJECT_PATH (caminho no servidor para a pasta do Projeto)
* PUBLIC_URL (URL do domínio onde ficarão hosperados os arquivos estáticos)
* STATIC_ROOT_
* STATIC_URL_
* MEDIA_ROOT_
* MEDIA_URL_
* DATABASES_
* HAYSTACK_CONNECTIONS_


Configuração do uWSGI
=====================

O pacote do Sistema da BV vem com um template do arquivo .ini de configuração
do uWSGI, localizado em ``bv/bv_uwsgi.ini``, para ser usado no uWSGI.
É necessário mudar os caminhos das seguintes constantes, de acordo com a
estrutura do servidor adotado.

* chdir_
* wsgi-file_
* home_
* touch-reload_
* socket_

Após a edição das constantes acima, sugere-se criar uma pasta chamada ``uwsgi`` no mesmo
nível que a do Sistema BV, e dentro dela criar outra chamada ``vassals``.
Uma vez dentro de ``vassals``, crie um link simbólico, com o comando ``ln -s``,
para o arquivo ``bv/bv/bv_uwsgi.ini``.

Finalmente, o comando para executar o uWSGI é ``nohup uwsgi --emperor /path/to/uwsgi/vassals &``.
Troque ``/path/to`` pelo caminho real no servidor.


Configuração do Nginx
=====================

O pacote do Sistema da BV já vem com um template do arquivo .conf de configuração
do Nginx, localizado em ``bv/nginx/bv.conf``, para ser usado no Nginx.
É necessário configurar as seguintes constantes, de acordo com a
estrutura do servidor adotado.

* server_name_
* access_log_
* error_log_
* location_
	* include_
* upstream
	* server_

Após a edição das constantes acima, o arquivo acima poderá ser copiado (ou linkado) para
o diretório com os arquivos de configuração do Nginx ``nginx/conf.d``.
O caminho deste diretório em uma instalação padrão do Nginx é ``/etc/nginx/conf.d/``.
Reinicie o Nginx após a cópia do arquivo.


.. _ADMINS: https://docs.djangoproject.com/en/stable/ref/settings/#admins
.. _ALLOWED_HOSTS: https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
.. _DEFAULT_FROM_EMAIL: https://docs.djangoproject.com/en/stable/ref/settings/#default-from-email
.. _STATIC_ROOT: https://docs.djangoproject.com/en/stable/ref/settings/#static-root
.. _STATIC_URL: https://docs.djangoproject.com/en/stable/ref/settings/#static-url
.. _MEDIA_ROOT: https://docs.djangoproject.com/en/stable/ref/settings/#media-root
.. _MEDIA_URL: https://docs.djangoproject.com/en/stable/ref/settings/#media-url
.. _DATABASES: https://docs.djangoproject.com/en/stable/ref/settings/#databases
.. _HAYSTACK_CONNECTIONS: http://django-haystack.readthedocs.org/en/latest/settings.html#haystack-connections

.. _chdir: http://uwsgi-docs.readthedocs.org/en/latest/Options.html#chdir
.. _wsgi-file: http://uwsgi-docs.readthedocs.org/en/latest/Options.html#wsgi-file-file
.. _home: http://uwsgi-docs.readthedocs.org/en/latest/Options.html#home-virtualenv-venv-pyhome
.. _touch-reload: http://uwsgi-docs.readthedocs.org/en/latest/Options.html#touch-reload
.. _socket: http://uwsgi-docs.readthedocs.org/en/latest/Options.html#socket-uwsgi-socket

.. _server_name: http://nginx.org/en/docs/http/ngx_http_core_module.html#server_name
.. _access_log: http://nginx.org/en/docs/http/ngx_http_log_module.html#access_log
.. _error_log: http://nginx.org/en/docs/ngx_core_module.html#error_log
.. _location: http://nginx.org/en/docs/http/ngx_http_core_module.html#location
.. _include: http://nginx.org/en/docs/ngx_core_module.html#include
.. _server: http://nginx.org/en/docs/http/ngx_http_core_module.html#server
