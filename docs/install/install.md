

# Instalação
Este sistema é uma aplicação open source Django, que pode ser clonada do repositório … diretamente em um projeto Django.
A instalação via PIP ainda não foi disponibilizada.

## Modos
O sistema pode ser utilizado em dois modos, “Collections desacopladas” e “Collections Relacionadas”, conforme descrito abaixo. Para o primeiro modo, há uma lista de requisitos mínimos, e uma lista de requisitos opcionais para segundo modo.

### Collections desacopladas
Com os requisitos mínimos instalados é possível executar a aplicação com as Collections em modo “collections desacopladas”.
Este modo é executado por padrão caso os requisitos opcionais não forem configurados no sistema (settings_sf.py/local_settings.py).

No modo “Collections desacopladas” as Collections configuradas no sistema só podem ser analisadas unitariamente, sem que se estabeleça nenhum tipo de relacionamento entre as mesmas.
#### Requisitos mínimos:
* Solr Cloud
* Python
* Django
* Banco de dados relacional


### Collections relacionadas
Os requisitos opcionais são necessários para a execução do sistema com as Collections em modo “collections conectadas”.

Caso você esteja instalando o sistema pela primeira vez, você pode pular essa parte e deixar a instalação em modo padrão de “Collections desacopladas”.

No modo “Collections relacionadas”, pode-se analisar as Collections configuradas no sistema e o relacionamento entre elas, através de mecanismos de “Join” de collections. Além da instalação dos requisitos opcionais, é necessário configurar as collections para que as mesmas possuam campos comuns de relacionamentos entre elas.
Este modo foi desenvolvido pensando em utilizar uma funcionalidade do Solr para operar em modo de computação paralela. Porém essa funcionalidade ainda possui problemas na versão Solr 6.6.2, sem previsão de finalização destas funcionalidades.
Mais especificamente, as funcionalidades de computação paralela utilizam o mecanismo de Streaming Expressions.
Todavia, o modo “Collections relacionadas” funciona relativamente bem, com o relacionamento de collections de alguns milhões de dados.

#### Requisitos opcionais:
* Celery
* RabbitMQ

## Estrutura de dados
O buscador trabalhar com estruturas de dados diversas, em diferentes camadas do sistema.
Segue abaixo a definição de cada uma delas.
### Grafo
A estrutura de grafos é definida no arquivo conf.py, e determina o relacionamento entre as  diferentes collections. Uma collection pode estar relacionada a zero ou mais collections.
### Árvore
Ao criar uma pesquisa uma estrutura de árvore é inicializada. Essa estrutura é armazenada na sessão Django do usuário.
Essa estrutura é controlada na view em alguns pontos da aplicação.
A classe NavigateCollection oferece os métodos de manipulação da árvore de navegação.
O Grafo define como as differentes collections se relacionam.
Uma pesquisa é formada pela navegação entre as diferentes collections, e essa pesquisa é que forma a árvore de navegação.
### Vértice
Um vértice da árvore é um nó da árvore de navegação. Esse objeto está na árvore de navegação, na sessão do usuário no Django.
