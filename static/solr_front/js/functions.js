/**
 * @file Funções da aplicação
 *
 * #### Existem 4 chamadas ajax
 *
 * - 1 para carregar o autocomplete do querybuilder.
 *
 * - 1 para a busca principal
 *
 * - 1 para a caixa de pesquisa
 *
 * - 1 para o grafico multifacet
 *
 * @module solr_front::functions
 *
 */

/**
 * Funcao principal de renderizacao da pagina.
 * @param {JSON} data - Json contendo facets
 */
function montaTotal(data) {

    var resultado_number = '<h3 class="title_secondary">Encontramos </h3> ' +
        '<div class="results">' +
        ' <p> ' + data['response']['numFound'].toLocaleString() + '<span> documentos em </span>' + collection_label +
        '</div>'
    // limpa resposta anterior se houver
    $('#resultado_number').html('')
    $('#resultado_number').append(resultado_number);

    var g = new GroupComponent()
    g.add(new DropdownFormComponentExec({
        'id': 'node',
        // usando interface padrão info_icon
        // 'click_interface': '<button>Interface</button>',
        'fields': [
            // pk deve corresponder ao field do vertice
            {
                'id': 'title',
                'pk': 'title',
                'label': 'Titulo',
                'type': 'text',
                'mode': 'inline',
                'initial_data': vertice['title'],
                'url_ajax': 'node_edit'
            },

            {
                'id': 'description',
                'pk': 'description',
                'label': 'Descrição',
                'type': 'textarea',
                'mode': 'inline',
                'initial_data': vertice['description'],
                'url_ajax': 'node_edit'
            },
        ],
    }, 'resultado_number'))

    g.renderExec()

    $('#resultado_number').css('display', '-webkit-box')

    $('#titulo').editable();
    $('#descricao').editable();
    // inicializa popover
    // $('[data-toggle="popover"]').popover();

}

var from_ajax = {}//variavel de escopo global para armazenar dados do ajax e manter em memoria

/**
 *
 * Faz a principal chamada Ajax no servidor.
 * Qdo essa fnc eh chamada ela pode receber dados estaticos na inicializacao
 * e carregar todos projetos e bolsas. Ainda pode receber estaticos para teste.
 *
 * Se nao receber dados estaticos, a funcao recupera no Querybuilder a busca realizada
 * e faz request no servidor.
 *
 * No sucesso chama a montagem da pagina atraves de funcoes especificas, comecando
 * pelo esqueleto e incluindo os demais elementos.
 * Os respectivos elements sao realizados outros  ajax para recuperar os dados
 * da cx de pesquisa e para o grafico interativo.
 *
 * @param {String} busca_realizada_str - String de busca realizada no queryBuilder
 *
 *
 */
function getData(busca_realizada_str) {

    busca_realizada = define_busca(busca_realizada_str);

    if (!$.isEmptyObject(busca_realizada)) {
        var url = home_sf_rurl + bv_collection + '/' + id_collection + '/'
        var url_back = url + 'params/'

        $.ajax({
            url: url,
            type: 'post',
            dataType: 'json',
            data: JSON.stringify(getBuscaRealizada({})),

            headers: {
                "cache-control": "no-cache",
                'X-Requested-With': 'XMLHttpRequest',
                "Content-Type": "application/json; charset=utf-8",
                "Accept": "application/json",
                'X-CSRFToken': csrf, //a varive  l csrf provem da pagina html
                'csrfmiddlewaretoken': csrf
            },

            success: function (data) {

                if (data['status'] == 409 || data['status'] == 500) {
                    $('#loader_screen').hide()
                    if (data['log']) {
                        console.log('Erro de indexação: ' + data['log'])
                    }
                    error_409_getdata(data, url_back);
                    return;
                }
                else {
                    var loader = document.getElementById('loader_screen')

                    hiden_exec(loader, function () {
                        // variavel global usada para reconstruir facets fora do getData
                        from_ajax['hierarquia'] = data['facet_counts']['hierarquico']
                        constroiComponentFacetsButtons(from_ajax['hierarquia'])
                    });
                    montaTotal(data)

                    $('.modal-backdrop').remove()

                    getTotalizadores()
                    collectionsRelacionadas()

                    if (omite_secoes.indexOf('stackedbarchart') === -1) {
                        recuperaGraficoDuplo(busca_realizada)
                    }
                    if (omite_secoes.indexOf('sankey') === -1) {
                        recuperaSankeyChart(busca_realizada)
                    }
                    if (omite_secoes.indexOf('pivot_table') === -1) {
                        recuperaPivotTable(busca_realizada)
                    }
                    if (omite_secoes.indexOf('bubblechart') === -1) {
                        recuperaBubbleChart(busca_realizada)
                    }
                    if (omite_secoes.indexOf('wordcloud') === -1) {
                        recuperaWordCloudChart(busca_realizada)
                    }
                    if (omite_secoes.indexOf('boxplot') === -1) {
                        recuperaBoxPlotChart(busca_realizada)
                    }
                    if (omite_secoes.indexOf('gather_nodes') === -1) {
                      gatherNodes(busca_realizada)

                      // Graficos somente para a BV. Criar uma configuracao no
                      recuperaGroupedBarChart_BV(busca_realizada)
                      recuperaBarChartFinanceiro_BV(busca_realizada)
                    }



                    $(".group_half_pie_chart").empty()
                    geraCharts(data.facet_counts.hierarquico)



                    //pega e apresenta documentos apartir da pagina 1
                    paginator(1)


                }
            },

        });

    }
}

/*
* Consulta endpoint no server para verificar task sendo
* processada utilizando o id da task do celery
*
* !! necessario implementar função de sucesso !!
*
*/
function consulta_pedido(id) {

    var url = home_sf_rurl + 'consulta_pedido/'

    $.ajax({
        url: url,
        type: 'get',
        dataType: 'json',
        data: {'id': id},
        headers: {
            "cache-control": "no-cache",
            'X-Requested-With': 'XMLHttpRequest',
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            'X-CSRFToken': csrf, //a varive  l csrf provem da pagina html
            'csrfmiddlewaretoken': csrf
        },
        success: function (data) {
            alert(data.status)
        },

    });
}

/*
* Altera visibilidade de elemento aplicando um callback,
* renderizando a visibilidade no dom antes de executar função de callback
*/
function hiden_exec(element, callback) {
    element.style.display = 'none'

    if (callback && typeof(callback) === "function") {
        // maneira encontrada para renderizar dom antes de executar callback
        setTimeout(callback, 1)


    }
}

/*
* Adiciona facets ao clicar em um facet; elemento <li>
* Parece que nao estah usando!!!

*/
function clickFacet(elemento) {
    var parent = $(elemento).parent().attr('valor');
    var valor = $(elemento).attr('valor');

    // Se jah existe a chave no json, appenda na lista caso o elemento
    // ainda nao exista na lista.
    if (selectedFacets['filtro'][chave].hasOwnProperty(parent)) {
        if (!$.inArray(valor, selectedFacets['filtro'][parent]) > -1) {
            selectedFacets['filtro'][parent].push(valor)
        }
    }
    // Se nao existe a chave no json, cria a chave e inicializa com uma lista
    // e respectivo elemento na lista.
    else {
        selectedFacets['filtro'][parent] = [valor]
    }
    // Chama funcao que faz chamada Ajax no servidor.
    getData()

}

/**
 * Define dados estaticos para uma busca de todas as bolsas e auxilios.
 * Utilizado na carga inicial da pagina.
 */
function getInitialSearch(collection) {

    // var result = '{"' + collection + '":{"query":null,"ordem":0,"collection":"' + collection + '","selected_facets":{}}}'
    // //debugger

    var result = vertice


    if (result.hasOwnProperty('body_json')) {
        //necessario pois a view é dependente que a chave da collection esteja acessivel no primeiro nivel
        return result['body_json']

    } else {

        return result
    }
    //getData(result)
}


/**
* Recupera dados agregados de collections relacionadas
*/
function collectionsRelacionadas(){

  if (typeof busca_realizada_str === 'undefined'){ busca_realizada = getBuscaRealizada() }
  else{ busca_realizada = JSON.parse(busca_realizada_str) }

  var url =  home_sf_rurl + bv_collection + '/' + id_collection + '/relacionadas/';


  var html_funil = function(data){
    count = data['count']
    related_content = data['related_content']

    var htmls = ''
    for (collection in count){

      if (count[collection]['col1']['value'] <= 0){continue}
      var funil_url = '<p><a href="' + home_sf_rurl + bv_collection + '/' + id_collection  + '/funil/'  + collection + '/' + count[collection]['col2']['parent_hash_querybuilder'] + '"' + ">Clique aqui para analisar " + count[collection]['col2']['value'] + ' ' + count[collection]['col2']['label'] +"</a></p>"

      // Main session for related collections
      htmls += '<div style="padding-top:40px">' +
        '<h2 class="title_primary">' +
          count[collection]['col1']['value'] + ' ' +  collection_label + ' -> ' +  count[collection]['col2']['value'] + ' ' + count[collection]['col2']['label'] +
        '</h2>' +
        funil_url

      // Display content of related collections
      var contents = related_content[collection];

      /*
      for (content in contents['facet']){
        var existe = 0;
        var related_content_html = '<div class="col-md-11 has-col"><div class="content_section__header">';

        related_content_html += '<h3 class="title_secondary">' + contents['facet'][content]['label'] + '</h3>';
        for (doc in contents['facet'][content]['docs']){
          if (jQuery.isEmptyObject(contents['facet'][content]['docs'][doc])){continue}
          doc = contents['facet'][content]['docs'][doc]
          related_content_html += '<p><a href ="' + doc["url"] + '">' +  doc["text"] + '</a></p>';
          if (doc["text"] !== ''){ existe = 1}
        }
        related_content_html += '</div></div>';
        if (existe){ // print only if one document has text.
          htmls += related_content_html;
        }
      }
      */
      htmls += '</div><hr>';
    }
    return htmls
  }

  $('#loader_resultado_number').show()

  $('#cr_content').hide()
  $('#cr_content').empty()


  $.ajax({
       url: url,
       type: 'post',
       dataType: 'json',

       headers: {
          "cache-control": "no-cache",
          'X-Requested-With': 'XMLHttpRequest',
          "Content-Type" : "application/json; charset=utf-8",
          "Accept" : "application/json",
          'X-CSRFToken': csrf, //a varivel csrf provem da pagina html
          'csrfmiddlewaretoken': csrf
        },

       success: function (data) {
         /*
         data retorna um objeto de collections.
         Cada collection tem um dicionario de totalizadores (conteudos)
         */
         $('.modal-backdrop').remove()



         var html = ''
         for (var d in data) {
           if (Object.keys(data[d]).length === 0 && data[d].constructor === Object){ continue }
            html = html_funil(data)
          }
          if (html == ''){
            html = '<div class="alert alert-warning" role="alert">' +
                    'Não existem dados de outras collections que se relacionam com esta busca.<div>'
          }
          $('#cr_content').show()
          $('#cr_content').append(html)
         $('#loader_resultado_number').hide()
       },
       error: function (xhr, ajaxOptions, thrownError) {
           if(xhr.status==403) {
              console.log(JSON.stringify(xhr) )
           }
         },
       data: JSON.stringify(busca_realizada)
   });

}


/**
 * Mostra as ultimas 20 publicacoes.
 */
function apresentaPublicacaoes(docs) {
    pub_relacionadas_20 = ''


    for (var i = 0; i < docs.length; i++) {
        pub_relacionadas_20 += '<p>' + docs[i]['referencia'] + '</p>'

        // console.log(docs[i]['referencia'])
    }
    $('#pub_relacionadas_20').empty()
    $('#pub_relacionadas_20').append(pub_relacionadas_20);
}


/**
 * Gera blocos totalizadores no front
 */
function getTotalizadores() {
    busca_realizada = getBuscaRealizada()
    // debugger;

    var url = home_sf_rurl + bv_collection + '/' + id_collection + '/totalizadores/';

    $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',

        headers: {
            "cache-control": "no-cache",
            'X-Requested-With': 'XMLHttpRequest',
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            'X-CSRFToken': csrf, //a varivel csrf provem da pagina html
            'csrfmiddlewaretoken': csrf
        },

        success: function (data) {
            // console.log('Success - Totalizadores da propria collection')
            // console.log(data)
            $('.modal-backdrop').remove()

            // constroiComponentDocumentos( data['facet'] )

            // faz join dos objetos e armazena novo objeto na variavel

            var obj = $.extend(data['unique'])
            obj = $.extend(obj, data['sum'])
            obj = $.extend(obj, data['avg'])
            obj = $.extend(obj, data['facet'])
            obj = $.extend(obj, data['median'])

            // renderiza objeto caso existir dados nele
            constroiComponentTotalizadores(obj)


        },
        error: function (xhr, ajaxOptions, thrownError) {
            if (xhr.status == 403) {
                console.log(JSON.stringify(xhr))
            }
        },
        data: JSON.stringify(busca_realizada)
    });
}


/**
* Use this object to controll ajax sent life time
* If an ajax already has been fired, cancel it before make a new one.
**/
var xhr = {'gatherNodes':null};






/**
 * Retrieve data from the same collection. Graph strtucture
 */
function gatherNodes() {
    busca_realizada = getBuscaRealizada()
    var url = home_sf_rurl + bv_collection + '/' + id_collection + '/gather_nodes/' + bv_collection + '/' ;
    $('#outcome_table').empty()
    $('#loader_linked').show()

    if( xhr['gatherNodes'] != null ) {
            xhr['gatherNodes'].abort();
            xhr['gatherNodes'] = null;
    }


    xhr['gatherNodes'] = $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',

        headers: {
            "cache-control": "no-cache",
            'X-Requested-With': 'XMLHttpRequest',
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            'X-CSRFToken': csrf, //a varivel csrf provem da pagina html
            'csrfmiddlewaretoken': csrf
        },

        success: function (data) {
            $('.modal-backdrop').remove()
            constroiComponentTotalizadores(data)
            $('#loader_linked').hide()
        },
        error: function (xhr, ajaxOptions, thrownError) {
            if (xhr.status == 403) {
                console.log(JSON.stringify(xhr))
            }
        },
        data: JSON.stringify(busca_realizada)
    });
}

/**
 * Monta os Select fields do grafico Sankey
 */
function criaSelectSankeyChart(button) {

    // Armazena os valores que jah foram utlziados para nao repetir.
    selects_vals = []
    selects = $(".sankey_options")
        .map(function () {
            selects_vals.push($(this).val())
        })
    selects_vals.splice(-1, 1)

    // Recupera o numero de selects para criar o proximo
    var numItems = $('.sankey_options').length - 1
    numItems += 1
    var sankeyNivel = 'nivel_' + numItems

    // Cria div antes do botao, para que os selects fiquem "ordenados"
    var button = $(button)

    // Cria o select
    var sel = '<select class="sankey_options" id="' + sankeyNivel + '">'
    var sel = $(sel)
    $(sel).append($("<option>").attr('value', '').text('Selecione uma dimensão'));
    $(sankey_chart_options['options']).each(function () {
        if (!selects_vals.includes(this.value)) {
            $(sel).append($("<option>").attr('value', this.value).text(decodeURI(this.label)));
        }
    });

    // Cria div "alert" que acondiciona o select, para poder excluir.
    var dismiss_html = '<a href="#" class="close" data-dismiss="alert" aria-label="close" title="close">×</a>'
    var div = $('<div class="alert alert-success alert-auto">').insertBefore(button);
    $(div).append(dismiss_html);

    // Adiciona o select a div.
    $(div).append($(sel));

}


/**
 * Monta os Select fields da tabela pivo
 */
function criaSelectPivotTable(button) {

    // Armazena os valores que jah foram utlziados para nao repetir.
    selects_vals = []
    selects = $(".pivot_options")
        .map(function () {
            selects_vals.push($(this).val())
        })
    selects_vals.splice(-1, 1)

    // Recupera o numero de selects para criar o proximo
    var numItems = $('.pivot_options').length - 1
    numItems += 1
    var pivotNivel = 'nivel_' + numItems

    // Cria div antes do botao, para que os selects fiquem "ordenados"
    var button = $(button)

    // Cria o select
    var sel = '<select class="pivot_options" id="' + pivotNivel + '">'
    var sel = $(sel)
    $(sel).append($("<option>").attr('value', '').text('Selecione uma dimensão'));
    $(pivot_table_options['options']).each(function () {
        if (!selects_vals.includes(this.value)) {
            $(sel).append($("<option>").attr('value', this.value).text(decodeURI(this.label)));
        }
    });

    // Cria div "alert" que acondiciona o select, para poder excluir.
    var dismiss_html = '<a href="#" class="close" data-dismiss="alert" aria-label="close" title="close">×</a>'
    var div = $('<div class="alert alert-success alert-auto">').insertBefore(button);
    $(div).append(dismiss_html);

    // Adiciona o select a div.
    $(div).append($(sel));

}


/**
 * Realiza busca vazia
 */
function getFakeData() {
    var busca_realizada = '{"graph_auxilios":{"query":{"condition":"AND","rules":[{"id":"area","field":"area","type":"string","operator":"equal","value":"Geologia"}],"valid":true},"ordem":0,,"selected_facets":{}}}'
    getData(busca_realizada)
}

/**
 * gera variavel de busca utilizada na função GetData
 */
function define_busca(busca_realizada_str) {

    if (typeof busca_realizada_str === 'undefined') {
        var busca_realizada = getBuscaRealizada()
    } else {
        var busca_realizada = JSON.parse(busca_realizada_str)
    }

    return busca_realizada

}

/**
 * gera componentes de blocos com totais
 */
function constroiComponentTotalizadores(obj) {

    var g = new GroupComponent()


    for (facet in obj) {
        facet = obj[facet]

        if (typeof facet['type'] != 'undefined') {

            if (contains(facet['type'], 'main')) {


                if (facet['data_type'] == "currency") {
                    facet['numFound'] = Number(facet['numFound']).toLocaleString("pt-BR", {
                        style: "currency",
                        currency: "BRL"
                    });
                }
                else {
                    facet['numFound'] = Number(facet['numFound']).toLocaleString(undefined, {maximumFractionDigits: 1})
                }


                g.add(new TotaisComponent({
                        'total': facet['numFound'],
                        'label': facet['label']
                    },
                    'main')
                );

            }
            if (contains(facet['type'], 'secondary')) {
                g.add(new TotaisComponent({
                        'total': facet['numFound'],
                        'label': facet['label']
                    },
                    'secondary')
                );
            }
        }
    }

    g.renderAll(clean = true)

    if ('outcome_type' in obj && obj['outcome_type'] == 'table'){
      var g_table = new GroupComponent()

      g_table.add(new TableComponent(obj,
          'outcome_table')
      );
      g_table.renderAll(clean = true)
    }


}

/**
 * gera componente com blocos de totais de docuemntos relacionados
 */
function constroiComponentTotalizadoresRelacionados(obj) {

    var g = new GroupComponent()


    for (facet in obj) {
        facet = obj[facet]
        g.add(new TotaisComponent({
                'total': facet['numFound'],
                'label': facet['label']
            },
            'totais_rel')
        );
    }


    g.renderAll(clean = true)


}

/**
 * gera componente que contem links de auxilios e bolsas
 * listados e categorizados
 */
function constroiComponentDocumentos(obj) {
    var g = new GroupComponent()

    for (facet in obj) {
        facet = obj[facet]
        if (facet['type'].indexOf('doc') > -1) {
            var links = []
            //gera lista de url
            for (key in facet['docs']) {
                var doc = facet['docs'][key]
                if (doc.text) {
                    links.push({'url': doc.url, 'titulo': doc.text})
                }
            }

            //split titulo para separar situacao do label
            var situacao = facet['label'].split('-')[1]
            var titulo = facet['label'].split('-')[0]

            var colunas = 6;
            if ('colunas' in facet) {
                colunas = facet['colunas']
            }

            //split titulo para separar situacao do label
            var situacao = facet['label'].split('-')[1]
            var titulo = facet['label'].split('-')[0]

            g.add(new DocsComponent({
                    'total': facet['numFound'],
                    'colunas': colunas,
                    'label': titulo,
                    'links': links,
                    'situacao': situacao
                }
                , 'documentos'));
        }
    }
    g.renderAll(clean = true)
}
