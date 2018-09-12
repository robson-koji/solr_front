/**
 * @file Funções especializadas nos facets
 *
 * @module solr_front::bv_facet
 */


/**
 * Armazena os facets selecionados, durante a navegacao.
 * A lista de facets eh fundamental para o funcionamento do mecanismo de busca,
 * porque ele diz quais sao os facets selecionados e que sao usados na filtragem do Solr.
 *
 * Este objeto eh manipulado atraves dos eventos no main.js para inclusao,
 * exclusao de facets.
 * Ele tambem eh acessado no bv_facets.js, apenas para mostrar as "tags" dos
 * facets que estao selecionados.
 *
 * Este objeto eh incluido no Json montado pelo Querybuilder, que eh chamado a cada
 * request feito para o servidor.
 * @var {Object}
 */
var selectedFacets = {};
var selectedFacets_wc = {};
var selectedFacets_filtro = {};

/**
 * Limpa textos exemplo 00; 04; que veem no inicio da chave dos campos
 * @param {String} label - Texto para ser normalizado
 */
function limpaLabelSolr(label) {
    if (label[2] == ';') {
        return label.slice(3, label.length);
    } else {
        return label;
    }
}

/**
 * Funcao recursiva para montagem do html dos facets
 * @param {Array} item - Lista de um determinado grupo de facets
 * @param {String} chave - Identificação do grupo no html do facet
 * @param {String} label - Texto do grupo usado na construção do html
 * @param {String} key_prefix - Utilizado para incluir prefixo na recursividade
 */
function geraDropdownfacets(item, chave, label, key_prefix) {

    if (!key_prefix) {
        key_prefix = ''
    }

    var ul = document.createElement('ul');
    for (key in item) {
        // Codigo nao executa se key for atributo count
        // Inclui tags no div
        incluiTags(key, chave, label, selectedFacets, key_prefix);

        var li = document.createElement('li');

        if (key != 'count') {
            var a = document.createElement('a');
            var selected_facet = '';
            var content = limpaLabelSolr(key) + ' (' + item[key]['count'] + ')';

            a.className = 'dropdown-item facet_a';
            a.setAttribute('href', '#');
            a.style.fontSize = '10px';

            a.setAttribute('valor', key_prefix + key)
            a.innerHTML = content;

            li.className = 'dropdown';
            li.setAttribute('valor', chave);
            li.appendChild(a);

            if (item[key].count) {
                // se existir atributo count no elemento função é chamada recursivamente e popula li
                var sub_li = geraDropdownfacets(item[key], chave, label, key_prefix + key + '|');
                if (sub_li) {
                    li.appendChild(sub_li);
                }
                ul.appendChild(li);
            }
        }
    }
    if (ul.childNodes.length) {
        return ul
    }
    else {
        return false
    }
}


/**
 * A tag do facet serve para poder visualizar o facet selecionado, e para exclui-lo.
 * Verifica se à o elemento do json no dict selectedFacets, se houver, cria a tag.
 * @param {String} keys - Identificação do grupo de facet
 * @param {String} chave - Identificação na lista de facets
 * @param {String} label - Titulo do grupo
 * @param {Array} selectedFacets - Lista de facets
 * @param {String} key_prefix - Inclui prefixo na identificação, *usado na recursividade*
 */
function incluiTags(key, chave, label, selectedFacets, key_prefix) {
    if (!key_prefix) {
        key_prefix = ''
    }

    key_orig = key;
    key = key_prefix + key;

    // Verifica se hah o indice no Json.
    if (selectedFacets.hasOwnProperty(chave)) {
        var array_exist = selectedFacets[chave]
    }

    if (array_exist && ($.inArray(key, selectedFacets[chave]) > -1)) {
        console.log('executou incluitags');
        selected_facet = ' selected_facet';

        var tag = document.createElement('span');
        var span = document.createElement('span');
        var a = document.createElement('a');
        var icon = document.createElement('i');

        $(span).append(decodeURIComponent(escape(limpaLabelSolr(label))) + ' : ' + limpaLabelSolr(key_orig));

        $(icon).attr('chave', chave)
            .attr("value", key)
            .attr('class', "remove remove_tag glyphicon glyphicon-remove-sign glyphicon-white");

        $(a).append(icon);

        $(tag).attr('class', "tag label label-info")
            .append(span)
            .append(a);

        $('#filtros_aplicados').show()

        $('#resultado_facets_header').append(tag);
    }
}


/**
 * Função processa facets e inclui html no sidebar
 * @param {JSON} json - Json contendo Facets retornados do Solr
 * @return {HTML} - retorna tag li
 */
function apresentaFacets(json) {
    // Acordeons dos facets
    var li = document.createElement('span');

    var refaz_json_data = function (i) {
        var chave = i['chave'];
        var label = i['label'];
        var item = json[chave];
        return geraDropdownfacets(item, chave, label);
    }

    /*
    Itera o Json recebido do server.
    Cada chave do Json eh uma categoria, e os valores sao os facets de cada categoria.
    */
    $.each(facetsCategorias, function (idx_a, categoria) {
        title = decodeURIComponent(escape(categoria['label']))
        body = ''

        var a = document.createElement('a');
        var sub_li = document.createElement('li');

        a.setAttribute('href', '#');
        a.setAttribute('data-toggle', 'dropdown');
        a.className = "dropdown-toggle";
        a.innerHTML = '<p class="titulo_facets">' + title + '</p>';
        a.setAttribute('aria-expanded', "false");
        sub_li.appendChild(a)

        $.each(categoria['facets'], function (idx_b, facet) {
            var ul = document.createElement('ul');
            var p = document.createElement('p');

            ul.setAttribute('valor', facet['chave']);
            ul.setAttribute('role', "menu");
            ul.setAttribute('aria-expanded', "false");

            p.style.color = 'white';
            p.style.paddingLeft = "10px";
            p.innerHTML = decodeURIComponent(escape(facet['label']));
            ul.className = "dropdown-menu";
            p.className = "titulo_facets";
            ul.appendChild(p)

            var y = refaz_json_data(facet);
            if (y) {
                ul.appendChild(y)
            }
            sub_li.appendChild(ul)
        });

        var script = document.createElement('script');
        script.innerHTML = "$('.dropdown-toggle').dropdown();";
        li.appendChild(sub_li);
        li.appendChild(script);
    });
    $('#body-sidebar').append(li);
    // return li;
}


/* envia variavel selectedFacets para formato do componente de facets, usado para construir interface nas recargas de pagina*/
function selectedFacetsToSelection() {
    var selecionados = []
    for (var i = 0; i < Object.keys(selectedFacets).length; i++) {
        var parent = Object.keys(selectedFacets)[i]
        var valor = selectedFacets[Object.keys(selectedFacets)[i]]
        for (var j = 0; j < valor.length; j++) {
            selecionados.push(parent + ':' + valor[j])
        }
    }
    // console.log('selecionados')
    // console.log(selecionados)
    return selecionados
}


// adciona elemento unitario em selected facets
function addElementInSelectedFacets(chave, valor) {
    if (typeof selectedFacets[chave] != 'undefined' && $.inArray(valor, selectedFacets[chave]) == -1) {
        selectedFacets[chave].push(valor)
    } else if (typeof selectedFacets[chave] == 'undefined') {
        selectedFacets[chave] = [valor]
    }
}


/* Extrai objeto contendo hierarquia do facet subdividida*/

/*dependente dos niveis retornados do servidor */
function extractHierarchyFacetString(string) {
    var paiMaster = string.split(':')[0] || null
    var filhos = string.split(':')[1] || null

    if (filhos != null) {
        if (paiMaster == filhos) {
            var obj = {root: paiMaster, pai: null, filho: null, neto: null}
        }

        var pai = filhos.split('|')[0] || null
        var filho = filhos.split('|')[1] || null
        var neto = filhos.split('|')[2] || null

        if (neto != null) {
            var obj = {root: paiMaster, pai: pai, filho: filho, neto: neto}
            return obj

        }
        else if (filho != null) {
            var obj = {root: paiMaster, pai: pai, filho: filho, neto: null}
            return obj
        } else {
            var obj = {root: paiMaster, pai: pai, filho: null, neto: null}
            return obj
        }
    } else {
        var obj = {root: paiMaster, pai: null, item: null, neto: null}
        return obj
    }
}


// algoritimo limpa filhos quando pai se encontra em selectedfacets
function cleanSelectedFacets() {
    $.extend(selectedFacets, selectedFacets_wc);
    $.extend(selectedFacets, selectedFacets_filtro);
    var aux = jQuery.extend(true, {}, selectedFacets);

    for (var key in aux) {
        var facet = aux[key]
        if (facet.indexOf('*') >= 0) {
            delete aux[key]
            aux[key] = ['*']
        } else {
            for (var i = 0; i < facet.length; i++) {
                //necessario eliminar espaços vazios e pipe para regex funcionar corretamente sem interrupção
                // necessario escapar todos os parenteses, pois regex nao funciona com eles
                var regex = new RegExp('^' + escapeRegExp(facet[i]) + '\\|')
                // debugger
                aux[key] = removeMatching(aux[key], regex)
                // debugger
            }
        }
    }
    return aux
}


// adciona elemento unitario em selected facets
function removeElementInSelectedFacets(chave, valor) {
    if ($.inArray(valor, selectedFacets[chave]) !== -1) {
        var busca = selectedFacets[chave].indexOf(valor)
        if (busca >= 0) {
            // console.log('existe na lista')
            selectedFacets[chave].splice(busca, 1);

            //deleta chave caso lista estiver vazia
            if (selectedFacets[chave].length == 0) {
                delete selectedFacets[chave]
            }
        }
    }
}


/* envia seleção de facets para variavel global selectedFacets*/
function selectionToSelectedFacets(selecionados) {
    for (var i = 0; i < selecionados.length; i++) {
        var parent = selecionados[i].split(':')[0]
        var valor = selecionados[i].split(':')[1]

        // não permite duplicação de itens
        if (!$.inArray(valor, selectedFacets[parent])) {
            selectedFacets[parent].push(valor)
        } else {
            selectedFacets[parent] = [valor]
        }
    }
}

/* pega todos itens selecionados no facet e retorna em um array*/
function getFacetsSelection() {
    var lista = []
    for (var i = 0; i < $('div[id^=tree_]').length; i++) {
        console.log($($('div[id^=tree_]')[i]).treeview('getChecked'))
        var selections = $($('div[id^=tree_]')[i]).treeview('getChecked')
        lista = lista.concat(treeviewToFacets(selections))
    }
    return lista
}


/* Converte lista de objetos treeview em lista simples de chaves para facet*/
function treeviewToFacets(lista) {
    var listaOut = []
    for (var i = 0; i < lista.length; i++) {
        console.log(lista[i].tag[0])
        listaOut.push(lista[i].tag[0])
    }
    return listaOut
}


function order_facet(element, order_list) {
    $(element).removeClass('btn-default').addClass("btn-success")
    colore_botao = $(element).attr('id')
    constroiComponentFacetsButtons(from_ajax['hierarquia'], ordem = order_list)
}

function reset_order_facet() {
    colore_botao = undefined
    constroiComponentFacetsButtons(from_ajax['hierarquia'])
}

/**
 *  Constroi componentes de facets apartir de um json passado no parametro
 */
function constroiComponentFacetsButtons(obj) {

    if (typeof colore_botao != 'undefined') {
        // se filtro já existir recupera a ordenação passando o paramentro no construtor de facets
        var data_ordem = $('#' + colore_botao).data()
        var ordem = data_ordem.order

    } else {
        var ordem = false
    }
    var g = new GroupComponent()
    ordem = ordem ? ordem : false
    if (obj) {

        for (var i = 0; i < Object.keys(obj).length; i++) {

            var it = obj[Object.keys(obj)[i]]
            var ob = makeDataComponentFacet(it, it.facets)
            select = selectedFacetsToSelection()
            g.add(new FacetComponentExec([ob, select], 'facets', ordem))
        }


        g.renderExec(clean = true, 'groupBy.order')

    }
}

/**
 *  Constroi objeto usado no componente para facets
 */
function makeDataComponentFacet(item, lista_itens) {
    if (typeof item != 'undefined') {
        var obj = {}
        obj['label'] = item.label
        obj['id'] = item.chave
        obj['groupBy'] = item.groupBy
        obj['count'] = item.count
        obj['order'] = item.order

        if (typeof lista_itens != 'undefined') {
            var itens = lista_itens || []
            for (it in itens) {
                if (typeof obj['itens'] == 'undefined') {
                    obj['itens'] = []
                }
                var subitem = itens[it]
                obj['itens'].push(makeDataComponentFacet(subitem, subitem.facets))
            }
        }
        return obj
    }
    return true
}

/**
 * Remove todos os facets da chave especificada
 */
function removeAllElementSelectedFacets(chave) {
    delete selectedFacets[chave]
}
