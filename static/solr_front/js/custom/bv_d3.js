/*
Este custom deve chamar bv_d3.js.
O arquivo ../bv_d3.js deve ser renomeado para buscador_d3.js, porque eh generico.
*/






/**
 * Recupera o grafo dos dados de projetos da BV, para montar o grafico barchart financeiro.
 */
function gatherNodesChart() {
    busca_realizada = getBuscaRealizada()
    busca_realizada['temporal_facet'] = 'data_inicio_ano'

    var url = home_sf_rurl + bv_collection + '/' + id_collection + '/gather_nodes/' + bv_collection + '/' ;

    if( xhr['gatherNodesChart'] != null ) {
            xhr['gatherNodesChart'].abort();
            xhr['gatherNodesChart'] = null;
    }


    xhr['gatherNodesChart'] = $.ajax({
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
          drawBarChartFinanceiro(data)
        },
        error: function (xhr, ajaxOptions, thrownError) {
            if (xhr.status == 403) {
                console.log(JSON.stringify(xhr))
            }
        },
        data: JSON.stringify(busca_realizada)
    });
}
