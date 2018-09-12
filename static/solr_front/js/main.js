/*********************************************************************

Script principal de execução

***********************************************************************/
/** @module solr_front::main */




//
// $(document).ready(function(){
//     $("#extratificacao_legend_label").click(function(){
//         $("#modalExtratificacao").modal();
//     });
// });

/**
* Recebe eventos de clique para solicitar uma filtratem, que chama o servidor.
* Recebe evento de selecao de um facet, que tb executa uma chamada no servidor
*/
$(document).ready(function(){

    //inicia loader screen - .show() - apresenta elemento correspondent
    $('#loader_screen').show()


    /*
    * Nao estah funcionado.
    * Verificar a diferenca entre funil (subcollection) e uma
    * collection principal para apresentar diferentes msgs.
    */
    var url = $(location).attr('href');
    var parts = url.split("/");
    var last_part = parts[parts.length-2];

    if (last_part === 'params'){
      $('#status_message').append('Os dados estão sendo indexados pelo sistema a uma taxa de aproximadamente 15.000 registros por minuto. Por favor aguarde...')
    }
    else{
      $('#status_message').append('Carregando...')
    }




    $('#select_home').change(function() { //jQuery Change Function

        var opval = $(this).val(); //Get value from select element
        if  (opval == "inicial"){return;}


        $('#select_home').val("inicial");
        if(opval=="modal_navigation_tree"){ //Compare it and if true
            $('#modal_navigation_tree').modal("show"); //Open Modal
        }else if(opval=="exp_csv"){ //Compare it and if true
            $('#exp_csv').modal("show"); //Open Modal
            $('#send_report').show()

        }
        else{
          window.location.href = opval;
        }

    });


    // Manipula evento do clique no botao Submit
    $('button#btn-get').on('click', function(){
      getData();
    });
    $('button#btn-clr').on('click', function(){
      getData();
    });

    // Manipula eventos de clic nos botoes de ordenacao do stackedbarchart
    $('button#ordena_barchart_y_axis').on('click', function(){
      drawStackChart(json_d3_glb, false, 'asc', null, null);
    });
    $('button#ordena_barchart_y_axis-rev').on('click', function(){
      drawStackChart(json_d3_glb, false, 'desc', null, null);
    });
    $('button#ordena_barchart_qt').on('click', function(){
      drawStackChart(json_d3_glb, false, null, 'asc', null);
    });
    $('button#ordena_barchart_qt-rev').on('click', function(){
      drawStackChart(json_d3_glb, false, null, 'desc', null);
    });
    $('button#ordena_barchart_anterior').on('click', function(){
      drawStackChart(json_d3_glb, false, null, null, null, 'prev');
    });
    $('button#ordena_barchart_proximo').on('click', function(){
      drawStackChart(json_d3_glb, false, null, null, null, 'next');
    });
    $('a#normaliza_pct_abs').on('click', function(){
      drawStackChart(json_d3_glb, false, null, null, true);
    });






    // Para montagem do graficos stacked bar ao clicar nos radio buttons.
    $("#eixo_y input:radio").click(function() {
      recuperaGraficoDuplo()
    });
    $("#eixo_x input:radio").click(function() {
      recuperaGraficoDuplo()
    });

    // Grafico Sankey. Mudanca dos selects
    $(document).on('change', '.sankey_options', function(){
      recuperaSankeyChart()
    })  ;

    // Pivot Table. Mudanca dos selects
    $(document).on('change', '.pivot_options', function(){
      recuperaPivotTable()
    })  ;

    // Grafico Wordcloud. Mudanca dos selects
    $(document).on('change', '.wordcloud_options', function(){
      recuperaWordCloudChart()
    })  ;


    // Grafico Bubble. Mudanca dos selects
    $(document).on('change', '.bubble_options', function(){
      recuperaBubbleChart()
    })  ;
    // Grafico Boxplot. Mudanca dos selects
    $(document).on('change', '.boxplot_options', function(){
      recuperaBoxPlotChart()
    })  ;

    // Grafico Bubble. Mudanca dos selects
    $(document).on('change', '.bubble_range', function(){
      var slider_min = document.getElementById("bubble_range_min");
      var slider_max = document.getElementById("bubble_range_max");

      $("#bubble_min_value").text(slider_min.value);
      $("#bubble_max_value").text(slider_max.value);

      drawBubbleChart(bubble_data, parseInt(slider_min.value), parseInt(slider_max.value))
    })  ;



    // Limpa o Json de facets que envia para o servidor.
    $('#limpar_facets').click(function(){
      // console.log('limpar_facets')
      selectedFacets = {}
      selectedFacets_wc = {}
      getData()
      $('#filtros_aplicados').hide()
    });


    // Remove facets das tags, ao clicar no x
    $(document).on('click', '.remove_tag', function(){
      ul_value = $(this).attr('chave')
      li_value = $(this).attr('value')

      // Remove o elemento clicado do array do Json, cuja chave eh a categoria
      selectedFacets[ul_value] = $.grep( selectedFacets[ul_value], function( value ) {
         return value != li_value;
      });
      // Chama funcao que faz chamada Ajax no servidor.
      getData()
    });



    /**
    * Adiciona facets ao clicar em um facet; elemento <li>
    */
    $(document).on('click', '.facet_a', function(){

        var parent = $(this).parent().attr('valor');
        var valor = $(this).attr('valor');

        // Se jah existe a chave no json, appenda na lista caso o elemento
        // ainda nao exista na lista.
        if(selectedFacets.hasOwnProperty(parent)){
          if (!$.inArray(valor, selectedFacets[parent]) > -1){
            selectedFacets[parent].push(valor)
          }
        }
        // Se nao existe a chave no json, cria a chave e inicializa com uma lista
        // e respectivo elemento na lista.
        else{
          selectedFacets[parent] = [valor]
        }
        // Chama funcao que faz chamada Ajax no servidor.
        getData()
    });


    /**
    * Monta o layer lateral do facet. Eh isso???
    *
    */
    var trigger = $('.hamburger'),
      overlay = $('.overlay'),
      isClosed = false;

    trigger.click(function () {
      hamburger_cross();
    });

    function hamburger_cross() {

      if (isClosed == true) {
        overlay.hide();
        trigger.removeClass('is-open');
        trigger.addClass('is-closed');
        isClosed = false;
      } else {
        overlay.show();
        trigger.removeClass('is-closed');
        trigger.addClass('is-open');
        isClosed = true;
      }
    }
    $('[data-toggle="offcanvas"]').click(function () {
          $('#wrapper').toggleClass('toggled');
    });
});


/**
* Monta o Querybuilder e chama uma busca inicial
*
*/
$(window).load(function(){
  if( typeof querybuilder_config == 'undefined'){

    querybuilder_config = {}
  }
  var collection_opt = generate_options(querybuilder_config)
  // debugger;


  query = getInitialSearch(bv_collection);
  // debugger;
  if( typeof query[bv_collection] != 'undefined'){

    selectedFacets = query[bv_collection]['selected_facets_col1']
  }


  //verifica se configuração da collections foi definida
  if( Object.keys(collection_opt).length ){
    //show querybuilder
    $('#facet_block').addClass('col-md-8')
    $('#querybuilder_content').show()

    geraRoot('builder_dinamic', collection_opt, query);

  }

  // stringify necessario, pois dentro da função ocorre um parser
  getData( JSON.stringify(query) )

});






/**
* Daqui para abaixo, funcoes e chamadas de funcoes auxiliares
*/


/**
 *
* Inicializa visualizador JSON
* @var {Object}
*/
var jsonPrettyPrint = {
     replacer: function(match, pIndent, pKey, pVal, pEnd) {
        var key = '<span class=json-key>';
        var val = '<span class=json-value>';
        var str = '<span class=json-string>';
        var r = pIndent || '';
        if (pKey)
           r = r + key + pKey.replace(/[": ]/g, '') + '</span>: ';
        if (pVal)
           r = r + (pVal[0] == '"' ? str : val) + pVal + '</span>';
        return r + (pEnd || '');
        },
     toHtml: function(obj) {
        var jsonLine = /^( *)("[\w]+": )?("[^"]*"|[\w.+-]*)?([,[{])?$/mg;
        return JSON.stringify(obj, null, 3)
           .replace(/&/g, '&amp;').replace(/\\"/g, '&quot;')
           .replace(/</g, '&lt;').replace(/>/g, '&gt;')
           .replace(jsonLine, jsonPrettyPrint.replacer);
        }
     };




// remove segundo bloco querybuilder
// geraRoot('builder_dinamic_2', instituicao_sede_opt);


$(document).ready(function(){
  $('.dropdown-toggle').dropdown()
});









/*
http://interactjs.io/
Utilizado para a legenda do grafico multinivel.
Soh funcionou fazendo um merge dos codigos de
resizing e dragging
*/

interact('.resize-legend')
.resizable({
  // resize from all edges and corners
  edges: { left: true, right: true, bottom: true, top: true },

  // keep the edges inside the parent
  restrictEdges: {
    outer: 'parent',
    endOnly: true,
  },

  // minimum size
  restrictSize: {
    min: { width: 100, height: 50 },
  },

  inertia: true,
})
.on('resizemove', function (event) {
  var target = event.target,
      x = (parseFloat(target.getAttribute('data-x')) || 0),
      y = (parseFloat(target.getAttribute('data-y')) || 0);

  // update the element's style
  target.style.width  = event.rect.width + 'px';
  target.style.height = event.rect.height + 'px';

  // translate when resizing from top or left edges
  x += event.deltaRect.left;
  y += event.deltaRect.top;

  target.style.webkitTransform = target.style.transform =
      'translate(' + x + 'px,' + y + 'px)';

  target.setAttribute('data-x', x);
  target.setAttribute('data-y', y);
  // target.textContent = Math.round(event.rect.width) + '\u00D7' + Math.round(event.rect.height);

  // Ao mover, redesenha o SVG da legenda.
  // drawStackChart(json_d3, true);

})
.draggable({
  // enable inertial throwing
  inertia: true,
  // keep the element within the area of it's parent
  restrict: {
    restriction: "parent",
    endOnly: true,
    elementRect: { top: 0, left: 0, bottom: 1, right: 1 }
  },
  // enable autoScroll
  autoScroll: true,

  // call this function on every dragmove event
  onmove: dragMoveListener,
  // call this function on every dragend event
  onend: function (event) {
    var textEl = event.target.querySelector('p');

    textEl && (textEl.textContent =
      'moved a distance of '
      + (Math.sqrt(Math.pow(event.pageX - event.x0, 2) +
                   Math.pow(event.pageY - event.y0, 2) | 0))
          .toFixed(2) + 'px');
  }
});



function dragMoveListener (event) {
  var target = event.target,
      // keep the dragged position in the data-x/data-y attributes
      x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx,
      y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

  // translate the element
  target.style.webkitTransform =
  target.style.transform =
    'translate(' + x + 'px, ' + y + 'px)';

  // update the posiion attributes
  target.setAttribute('data-x', x);
  target.setAttribute('data-y', y);
}

// this is used later in the resizing and gesture demos
window.dragMoveListener = dragMoveListener;
