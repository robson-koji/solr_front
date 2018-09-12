/**
 * @file Funções de proposito geral, idependentes da aplicação
 * @module solr_front::utils
 */

/**
 * Função separa string nas virgulas
 * @param {String} val - Frase para tratar
 * @return {Array} - Array com as palavras divididas na virgula
 */
function split(val) {
    return val.split(/,\s*/);
}

/**
 * Função extrai ultimo termo do texto
 * @param {String} term - Texto para extração
 * @return {String} - Retorna ultima palavra
 */
function extractLast(term) {
    return split(term).pop();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
}

/**
 * Função  verifica se texto esta contido em outro
 * @param {String} value - Texto onde será efetuado a busca
 * @param {String} searchFor - Texto que será buscado
 * @return {Boll}  - Retorna Verdadeiro ou falso
 */
function contains(value, searchFor) {
    var v = (value || '').toString().toLowerCase();
    var v2 = searchFor;
    if (v2) {
        v2 = v2.toLowerCase();
    }
    return v.indexOf(v2) > -1;
}

/**
 * Função embaralha um array
 * @param {Array} array - Array que tera seu conteudo embaralhado
 * @return {Array} - O Array embralhado
 */

function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }

    return array;
}

/* função jquery para ordenar elementos */
function getSortMethod() {

    var _args = [].slice.call(arguments);

    return function (a, b) {

        for (var i = 0; i < _args.length; i++) {

            var x = Object.keys(_args)[i]

            var index = _args[x].substring(1)
            var ax = a[index];
            var bx = b[index];

            var cx;

            ax = typeof ax == "string" ? ax.toLowerCase() : ax / 1;
            bx = typeof bx == "string" ? bx.toLowerCase() : bx / 1;

            if (_args[x].substring(0, 1) == "-") {
                cx = ax;
                ax = bx;
                bx = cx;
            }
            if (ax != bx) {
                return RemoveEspecialCharMask(ax) < RemoveEspecialCharMask(bx) ? -1 : 1;
            }

        }
    }
}

Array.prototype.sortBy = function () {

    //tratamento criado porque o boxsplot gera erro ao tentar utilizar um objeto não array em um Array
    try {
        var lista = this.sort(getSortMethod.apply(null, arguments));
        return lista
    }
    catch (err) {
        return this
    }

}


//remove strings de array baseado em regex
function removeMatching(originalArray, regex) {
    var j = 0;
    while (j < originalArray.length) {
        // /elimina espaços em branco e pipes para melhor funcionamento do regex
        var chave = originalArray[j]

        if (regex.test(chave)) {
            originalArray.splice(j, 1);
        }
        else {
            // debugger
            j++;
        }
    }
    return originalArray;
}

function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

/* Remove caracters acentuados e especiais da string no navegador IE (mais lento )*/
function RemoveEspecialCharMask(especialChar) {
    if (typeof especialChar == "string") {

        especialChar = especialChar.replace(/[áàãâä]/i, 'a');
        especialChar = especialChar.replace(/[éèêë]/i, 'e');
        especialChar = especialChar.replace(/[íìîï]/i, 'i');
        especialChar = especialChar.replace(/[óòõôö]/i, 'o');
        especialChar = especialChar.replace(/[úùûü]/i, 'u');
        especialChar = especialChar.replace(/[ç]/i, 'c');
        especialChar = especialChar.replace(/[^a-z0-9]/i, '_');
        especialChar = especialChar.replace(/_+/, '_');

    }
    return especialChar;

}


$.fn.ordenaElementByAtribute = function (element, atribute) {

    var ordenado = $(this).find(element).sort(function (a, b) {

        var an = a.getAttribute(atribute),
            bn = b.getAttribute(atribute);

        if (an > bn) {
            return 1;
        }

        if (an < bn) {
            return -1;
        }
        return 0;

    })

    $(this).find(element).detach()
    $(this).append(ordenado)

}

/**
 * @param {String} HTML representing a single element
 * @return {Element}
 */
function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;

    if (typeof template.content != 'undefined') {

        return template.content.firstElementChild;
    } else {
        return template.children[0]
    }
}


function GetBrowserInfo() {
    var isOpera = !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;

    var isFirefox = typeof InstallTrigger !== 'undefined';   // Firefox 1.0+
    var isSafari = Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0;

    var isChrome = !!window.chrome && !isOpera;              // Chrome 1+
    var isIE = /*@cc_on!@*/false || !!document.documentMode;   // At least IE6

    if (isOpera) {
        return 1;
    }
    else if (isFirefox) {
        return 2;
    }
    else if (isChrome) {
        return 3;
    }
    else if (isSafari) {
        return 4;
    }
    else if (isIE) {
        return 5;
    }
    else {
        return 0;
    }
}

//Funcao para deletar item especifico do array selectedFacets_wc
function deletar_word(keytodel, wordtodel) {
    if (selectedFacets_wc[keytodel].length == 1) {
        delete selectedFacets_wc[keytodel];
        delete selectedFacets[keytodel];
        $('.word_ls').remove();
        getData();
        return

    }
    if (selectedFacets_wc[keytodel].length > 1) {
        for (var i = 0; i < selectedFacets_wc[keytodel].length; i++) {

            if (selectedFacets_wc[keytodel][i] === wordtodel) {
                if (selectedFacets_wc[keytodel].length > 1) {
                    selectedFacets_wc[keytodel].splice(i, 1);
                    //selectedFacets[keytodel].splice(i, 1);
                    $('.word_ls').remove();
                    getData();
                    return
                }

            }
        }


    }

}

// Função recupera documentos do solr especificando a pagina
function paginator(page, sorting, rows){
  $('.ajax-docs-loaders').show()
  $('#documentos').html('')
  pesquisa = getBuscaRealizada({})
  pesquisa[bv_collection]['page'] = page
  if(typeof sorting != undefined){
    pesquisa[bv_collection]['sort'] = sorting
  }
  if(typeof rows != undefined){
    pesquisa[bv_collection]['rows'] = rows
  }

  $.ajax({
    type: "POST",
    url: home_sf_rurl + bv_collection + '/' + id_collection +"/docs_widget/",
    data: JSON.stringify(pesquisa),
    success: function(data){
         $('#documentos').html(data['resultado']);
         $('#documentos').change();
        $('.ajax-docs-loaders').hide()
    },
    dataType: 'json',                                                                                                                                                                                               headers: {
              "cache-control": "no-cache",
              'X-Requested-With': 'XMLHttpRequest',
              "Content-Type": "application/json; charset=utf-8",
              "Accept": "application/json",
              'X-CSRFToken': csrf //a varivel csrf provem da pagina html
          },
  });
}
