


# Introdução
Este sistema é um portal web, genericamente chamado de Solr Front, ou ainda de Buscador Analítico. O Solr Front/Buscador é uma ferramenta de análise de dados multipropósito, onde  dados de quaisquer natureza podem ser carregados, visualizados e analisados.

Para que uma base de dados possa ser analisada no sistema, é necessário realziar dois processos:
* ETL (extração, transformação e carga)
* Configuração da coleção de dados.

Estes dois processos serão descritos ao longo neste documento.

## Nomenclatura
Este sistema é genericamente chamado de Buscador Analítico ou ainda de Solr Front.
Buscador Analítico porque o objetivo é realizar buscas e efetuar análises em bases de dados de grandes volumes.
Solr Front porque o backend do sistema utiliza o sistema Solr, e agrega uma camada de front-end para o mesmo. Solr é um mecanismo de buscas utilizado em aplicações críticas de grande porte

As denominações utilizadas neste documento, Coleção de dados e Collection se referem a bases de dados genéricas. Uma Collection é uma base de dados carregada no Buscador Analítico.

## Sistema/subsistema
O sistema Solr Front / Buscador Analítico é uma aplicação web com dois subsistemas envolvidos, que serão descritos mais abaixo.

Além do subsistema web, há um outro subsistema de carga de dados, genericamente chamado de ETL, do inglês Extract Transform Load (Extração Transformação Carregamento). Como o Solr Front é basicamente um sistema de busca e análise de dados, a maneira como os dados são organizados é fundamental, e essa organização se dá através dos processos de ETL.

## Subsistema Solr Front
A arquitetura deste sistema envolve a utilização de 4 grandes componentes:
### Solr Search Engine
Solr é uma plataforma de pesquisa de código aberto , escrita em Java, do projeto Apache Lucene. Seus principais recursos incluem pesquisa de texto completo, indexação em tempo real, clustering dinâmico, integração de banco de dados como NoSQL e gerenciamento de documentos ricos (HTML, Word, PDF). - Origem: Wikipédia, a enciclopédia livre.
### Front end Javascript
A camada de apresentação, que é a interface que o usuário efetivamente acessa, utiliza Javascript e alguns frameworks como Jquery, d3js etc, para montar a página HTML, filtros, componente de busca, gráficos etc.
### Python/Django
A aplicação web Python/Django atua como um middleware entre as requisições do front end e o Solr Front.
Um banco de dados relacional é utilizado para armazenar algumas consultas no buscador, para controle de atualização de dados.
É previsto o desenvolvimento de um componente de colaboração, onde um usuário cadastrado no sistema possa compartilhar as suas buscas, publicamente, ou com outros usuários cadastrados.
