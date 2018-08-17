# Infraestrutura


## Solr
### Criar collection (shards, réplicas, solrconfig.xml)
#### Campos dinâmicos
É possível escolher a criação de campos dinâmicos quando os mesmos seguirem um regra de tipagem igual, ou compatível. Por exemplo, quando não for necessário utilizar tipo numérico, que é mais eficiente em termos de busca, e o mesmo puder ser definido como tipo string para ser compatível com outros campos dinâmicos.
Campos a serem facetados não podem ser definidos dinamicamente. (ver abaixo)

Exemplo “dynamicField”

  <dynamicField name="GRADUACAO*" type="string" multiValued="true" indexed="true" stored="true"/>

### Verificar separador dos campos de facet
Os campos a serem facetados devem ser separados pelo caracter “|” no arquivo que será carregado no Solr.
Os mesmos deverão ser do tipo “descendant_path” como no exemplo abaixo:

Exemplo “fieldType”

    <fieldType name="descendent_path" class="solr.TextField">
      <analyzer type="index">
        <tokenizer class="solr.PathHierarchyTokenizerFactory" delimiter="|" />
      </analyzer>
      <analyzer type="query">
        <tokenizer class="solr.KeywordTokenizerFactory" />
      </analyzer>
    </fieldType>

Exemplo “descendent_path”

  <field name="GRADUACAO_AREAS-DO-CONHECIMENTO_FACET" multiValued="true" type="descendent_path"/>



### Campos para busca
Campo apresentado na busca avançada do sistema.
Do ponto de vista do usuário, ele escolhe o campo onde será efetuada uma busca, como nos exemplos abaixo, do Lattes e de Projetos da BV respectivamente.


#### Descrição do caso de uso

1. Usuário escolhe um campo para busca.
2. Usuário começa a digitar
3. Sistema retorna lista de facets, montanto uma “lista autocomplete”
4. Usuário seleciona um item apresentado no autocomplete.
5. Sistema realiza busca no campo buscável com o valor selecionado no autocomplete.

#### Descrição técnica
Tecnicamente dois campos são indexados com tipos diferentes, sendo que um deles é utilizado para a busca e outro é utilizado para a apresentação no autocomplete.
Essa implementação pode ser feita como descrito nos exemplos abaixo:

Campo original, que é apresentado no autocomplete:

 <field name="ATIVIDADES-DE-ENSINO_DISCIPLINAS" type="strings"/>

Definir um tipo que será utilizado como campo de busca:

 <fieldType name="text_busca" class="solr.TextField" sortMissingLast="true" positionIncrementGap="100">
      <analyzer type="index">
        <tokenizer class="solr.StandardTokenizerFactory"/>
        <filter class="solr.SynonymFilterFactory" synonyms="synonyms.txt" ignoreCase="true" expand="true"/>
        <filter class="solr.StopFilterFactory" ignoreCase="true" words="lang/stopwords_pt.txt" format="snowball" />
        <filter class="solr.WordDelimiterFilterFactory" generateWordParts="1" generateNumberParts="1" catenateWords="1" catenateNumbers="1" catenateAll="0"/>
        <filter class="solr.ASCIIFoldingFilterFactory"/>
        <filter class="solr.LowerCaseFilterFactory"/>
        <filter class="solr.EdgeNGramFilterFactory" minGramSize="1" maxGramSize="18"/>
        <filter class="solr.PortugueseLightStemFilterFactory"/>
        <filter class="solr.RemoveDuplicatesTokenFilterFactory"/>
      </analyzer>
      <analyzer type="query">
        <tokenizer class="solr.StandardTokenizerFactory"/>
        <filter class="solr.SynonymFilterFactory" synonyms="synonyms.txt" ignoreCase="true" expand="true"/>
        <filter class="solr.StopFilterFactory" ignoreCase="true" words="lang/stopwords_pt.txt" format="snowball" />
        <filter class="solr.WordDelimiterFilterFactory" generateWordParts="1" generateNumberParts="1" catenateWords="0" catenateNumbers="0" catenateAll="0"/>
        <filter class="solr.ASCIIFoldingFilterFactory"/>
        <filter class="solr.LowerCaseFilterFactory"/>
        <filter class="solr.PortugueseLightStemFilterFactory"/>
        <filter class="solr.RemoveDuplicatesTokenFilterFactory"/>
      </analyzer>
    </fieldType>

Definir um campo dinâmico que possa ser utilizado em todos os campos de busca.

  <dynamicField name="*_busca" type="text_busca" multiValued="true" indexed="true" stored="true"/>

Fazer uma cópia do campo original, para o campo buscável

  <copyField source="ATIVIDADES-DE-ENSINO_DISCIPLINAS" dest="ATIVIDADES-DE-ENSINO_DISCIPLINAS_busca"/>

Existe também a possibilidade de apenas atribuir ao campo que se deseja buscar, o type=text, como no exemplo a seguir:

	<field name="abstract" type="text"/>

E adicionar ao conf da collection os parametros do QueryBuilder, conforme exemplo abaixo:

  {
            "get_from_solr_field": "abstract",
            "label": "Resumo",
            "operators": ["equal", "not_equal"],
            "input": "autocomplete",
            "solr_params": {
              "q" : "*:*",
              "fl" : "*",
              "rows": "20",
              "field": "abstract",
              "facet_field" : "abstract"

             } ,
            "type": "string"
          }



### Campos para nuvem de palavras
Definir o campo original que será copiado para gerar nuvem de palavras, pois não é possível copiar um campo que não existe.


Criar o campo que será utilzado para gerar nuvem de palavras

  <field name="campo_nuvem_palavras" type="text_gen_stopword"  multiValued="true" indexed="true" stored="true"/>

Copiar o campo que será utilizado na nuvem de palavras:

  <copyField source="original" dest=”campo_nuvem_palavras"/>

Definir o tipo do campo que é utilizado na nuvem de palavras:

  <fieldType name="text_gen_stopword" class="solr.TextField" positionIncrementGap="100">
      <analyzer type="index">
        <tokenizer class="solr.StandardTokenizerFactory"/>
        <filter class="solr.StopFilterFactory" ignoreCase="true" words="stopwords.txt" />
        <filter class="solr.LowerCaseFilterFactory"/>
      </analyzer>
      <analyzer type="query">
        <tokenizer class="solr.StandardTokenizerFactory"/>
        <filter class="solr.StopFilterFactory" ignoreCase="true" words="stopwords.txt" />
        <filter class="solr.LowerCaseFilterFactory"/>
      </analyzer>
</fieldType>

### Campos para exportação
Todos os campos que serão exportados devem ser definidos com docValues=true no schema.







Front-end
Componentes

Facet
Transformação na view dos dados utilizados no facet no front-end

Exemplos do formato do dado facetado recebido do Solr:
(Pdb) solr_json['facets']['AREAS-DO-CONHECIMENTO-DE-ATUACAO_FACET']['buckets'][0]
{u'count': 10232, u'val': u'CIENCIAS_BIOLOGICAS'}

Exemplos do formato do dado facetado enviado para o fron-end:
(Pdb) solr_json['facet_counts']['hierarquico']['AREAS-DO-CONHECIMENTO-DE-ATUACAO_FACET']['facets']['LINGUISTICA_LETRAS_E_ARTES']['facets']['Artes']['facets']['Artes']
{'chave': u'LINGUISTICA_LETRAS_E_ARTES|Artes|Artes', 'count': 11, 'facets': {}, 'label': 'Artes'}


(Pdb) solr_json['facet_counts']['hierarquico']['DOUTORADO_AREAS-DO-CONHECIMENTO_FACET']
{'count': 5, 'facets': {u'ENGENHARIAS': {'chave': u'ENGENHARIAS', 'count': 2, 'facets': {u'Engenharia de Materiais e Metal\xfargica': {'chave': u'ENGENHARIASEngenharia de Materiais e Metal\xfargica', 'count': 1, 'facets': {u'Materiais N\xe3o-Met\xe1licos': {'chave': u'ENGENHARIAS|Engenharia de Materiais e Metal\xfargica|Materiais N\xe3o-Met\xe1licos', 'count': 1, 'facets': {}, 'label': 'Materiais N\xc3\xa3oMet\xc3\xa1licos'}}, 'label': 'Engenharia de Materiais e Metal\xc3\xbargica'}, u'Engenharia Aeroespacial': {'chave': u'ENGENHARIASEngenharia Aeroespacial', 'count': 1, 'facets': {u'Materiais e Processos para Engenharia Aeron\xe1utica e Aeroespacial': {'chave': u'ENGENHARIAS|Engenharia Aeroespacial|Materiais e Processos para Engenharia Aeron\xe1utica e Aeroespacial', 'count': 1, 'facets': {}, 'label': 'Materiais e Processos para Engenharia Aeron\xc3\xa1utica e Aeroespacial'}}, 'label': 'Engenharia Aeroespacial'}, u'N\xe3o identificado': {'chave': u'ENGENHARIASN\xe3o identificado', 'count': 1, 'facets': {u'Materiais El\xe9tricos': {'chave': u'ENGENHARIAS|N\xe3o identificado|Materiais El\xe9tricos', 'count': 1, 'facets': {}, 'label': 'Materiais El\xc3\xa9tricos'}}, 'label': 'N\xc3\xa3o identificado'}}, 'label': 'ENGENHARIAS'}, u'OUTROS': {'chave': u'OUTROS', 'count': 1, 'facets': {u'Microeletr\xf4nica': {'chave': u'OUTROSMicroeletr\xf4nica', 'count': 1, 'facets': {u'Dispositivos': {'chave': u'OUTROS|Microeletr\xf4nica|Dispositivos', 'count': 1, 'facets': {}, 'label': 'Dispositivos'}}, 'label': 'Microeletr\xc3\xb4nica'}}, 'label': 'OUTROS'}, u'CIENCIAS_EXATAS_E_DA_TERRA': {'chave': u'CIENCIAS_EXATAS_E_DA_TERRA', 'count': 2, 'facets': {u'N\xe3o identificado': {'chave': u'CIENCIAS_EXATAS_E_DA_TERRAN\xe3o identificado', 'count': 2, 'facets': {u'F\xedsica da Mat\xe9ria Condensada': {'chave': u'CIENCIAS_EXATAS_E_DA_TERRA|N\xe3o identificado|F\xedsica da Mat\xe9ria Condensada', 'count': 2, 'facets': {}, 'label': 'F\xc3\xadsica da Mat\xc3\xa9ria Condensada'}}, 'label': 'N\xc3\xa3o identificado'}}, 'label': 'CIENCIAS_EXATAS_E_DA_TERRA'}}, 'groupBy': {'order': 5, 'id': 'doutorado', 'label': 'Doutorado'}, 'chave': 'DOUTORADO_AREAS-DO-CONHECIMENTO_FACET', 'label': '\xc3\x81rea do conhecimento', 'order': 5}








Collections relacionadas
A estrutura de Grafo do buscador permite que collections sejam relacionadas através de campos com valores comuns. Desta maneira elas podem ser trabalhandas em conjunto no sistema.
conf.py
As collections se relacionam através de campos determinados no dicionário  EDGES do arquivo conf.py.

Tomo como exemplo abaixo que Col4 é um subconjunto de Col 1.



Para implementar o uso das collections relacionadas no sistema, dois processos principais foram estabelecidos e serão descritos abaixo, sendo eles a “Contabilização da quantidade dos objetos relacionas” e o processo de apresentação de “Sub-collections”.


Contabilização da quantidade dos objetos relacionados
Este processo de contabilização existe para apresentar o “join” das collections relacionadas, como no exemplo abaixo:



Quando a página de uma collection do buscador é carregada, um Ajax chama a view RelatedCollection que recupera todas as collections relacionadas a collection em questão, para montar a apresentação conforme indicado acima.

views.py
A view utilizada neste processo é a RelatedCollections, que faz as verificações dos relacionamentos citados acima, e a função get_or_create_related_collection_db é quem efetivamente contabiliza, e armazena as informações de contabilização.
As quantidades de cada relacionamento são “cacheadas” em banco de dados para que o processo de contabilização das quantidades dos relacionamentos não precise ser executado sempre.



Sub-collection
A quantidade dos registros que fazerm parte de um relacionamento entre duas collections é apresentada no exemplo da figura abaixo, conforme já explicado anterioremente.

O link abaixo direciona para o subconjunto da collection B que faz interseção com a Collection A.



Para que seja possível acessar o subconjunto da collection B que faz intersecção com a collection A, é necessário indexar os registros da collection B com um marcador dessa intersecção. O subconjunto da collection B é o que chamamos de sub-collection.

Portanto ao clicar no link acima, a view AddVerticeView é acessada para cuidar do processo de reinidexação.
