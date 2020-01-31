/*
Este custom deve chamar bv_d3.js.
O arquivo ../bv_d3.js deve ser renomeado para buscador_d3.js, porque eh generico.
*/






function recuperaGroupedBarChart_BV(busca_realizada_str) {
  // Recupera os valores da busca.
  if (typeof busca_realizada_str != 'string') {
      var result_cp_gd = getBuscaRealizada({});
  }
  else {
      var result_cp_gd = JSON.parse(busca_realizada_str)
  }

  result_cp_gd[bv_collection]['grafico'] = 'groupedbar';
  result_cp_gd[bv_collection]['csrfmiddlewaretoken'] = $('[name="csrfmiddlewaretoken"]').val();
  // result_cp_gd[bv_collection]['query'] = '*:*';

  $.ajax({
    url: "/pt/data_graphics/",
    method:'POST',
    dataType:"json",
    // data: {result_cp_gd:result_cp_gd, grafico:'groupedbar', csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val()},
    data: JSON.stringify(result_cp_gd),
    success: function(resultado){
      // console.log(resultado)
      // debugger;
      var data = resultado['format_compatible']
      var dict_elemens = [1,2]
      var getSvgObj = getSvgObj_GB()
      getSvgObj.selectAll("*").remove();
      groupedbar(getSvgObj, data, dict_elemens)
    }
  })
}





/**
 * Recupera o grafo dos dados de projetos da BV, para montar o grafico barchart financeiro.
 */

function recuperaBarChartFinanceiro_BV(busca_realizada_str) {
 // Recupera os valores da busca.
 if (typeof busca_realizada_str != 'string') {
     var result_cp_gd = getBuscaRealizada({});
 }
 else {
     var result_cp_gd = JSON.parse(busca_realizada_str)
 }

 result_cp_gd[bv_collection]['grafico'] = 'barchart_financeiro';
 result_cp_gd[bv_collection]['csrfmiddlewaretoken'] = $('[name="csrfmiddlewaretoken"]').val();
 // result_cp_gd[bv_collection]['query'] = '*:*';


   $.ajax({
     url: "/pt/data_graphics/",
     method:'POST',
     dataType:"json",
     // data: {result_cp_gd:result_cp_gd, grafico:'groupedbar', csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val()},
     data: JSON.stringify(result_cp_gd),
     success: function(resultado){
       // console.log(resultado)
       var getSvgObj = getSvgObj_BF()
       getSvgObj.selectAll("*").remove();
       drawBarChartFinanceiro(getSvgObj, resultado)
     }
   })
}
