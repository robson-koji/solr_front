.. _pre-requisitos:

==============
Pré-Requisitos
==============

Abaixo estão documentados os pré-requisitos para o servidor, assim como
dicas e observações sobre os aplicativos. Esta configuração foi testada
em ambiente Linux, em ambientes Microsoft Windows ajustes adicionais
podem ser necessários.


Software
========

Os pré-requisitos de software para o funcionamento do sistema BV-FAPESP são:

* Python 2.7
    * `PIP 1.5+`_
    * `Virtualenv 1.11+`_
    * `Virtualenvwrapper 4.2+`_
* MySQL 5.5
* `Nginx 1.4+ e uWSGI 2.0+`_ ou `Apache 2.2+ e mod_wsgi 3.4+`_ (Servidor Web)
* `Apache Solr 4.6+`_ (Servidor de Pesquisa)


Servidor Web
============

Como solução de Servidor Web, em teste controlado foi identificado que a
solução Nginx + uWSGI possui um desempenho superior ao Apache + mod_wsgi.
Comparado ao Apache + mod_wsgi, o Nginx + uWSGI reduziu em 50%, em média,
o tempo de entrega de páginas aos usuários. Além disso, a carga de
processamento e memória do servidor foram reduzidas, a pesar do tráfego
de acesso não ter reduzido.


Servidor de Pesquisa
====================

Uma opção de publicação do servidor de pesquisa é fazer uso da imagem da
Máquina Virtual ou do Instalador disponível no site Bitnami_, para facilitar
no trabalho de instalação.


.. _Nginx 1.4+ e uWSGI 2.0+: https://uwsgi.readthedocs.org/en/latest/tutorials/Django_and_nginx.html
.. _Apache 2.2+ e mod_wsgi 3.4+: https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/modwsgi/
.. _Apache Solr 4.6+: https://lucene.apache.org/solr/
.. _Bitnami: http://bitnami.com/stack/solr
.. _PIP 1.5+: http://www.pip-installer.org/en/latest/installing.html
.. _Virtualenv 1.11+: https://pypi.python.org/pypi/virtualenv
.. _Virtualenvwrapper 4.2+: https://pypi.python.org/pypi/virtualenvwrapper
