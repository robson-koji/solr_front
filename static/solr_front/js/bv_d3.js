data/**
* @file Funções para geração de graficos usando D3.js
* @module solr_front::bv_d3
*/




var bubble_data = 0

function recuperaBubbleChart(busca_realizada_str){
  // Recupera os valores da busca.
  if (typeof busca_realizada_str != 'string'){
    var result_cp_gd = getBuscaRealizada({});
  }
  else{
    var result_cp_gd = JSON.parse(busca_realizada_str)
  }

  var json_levels_list = []
  selects = $(".bubble_options")
    .map(function() {
      obj = {}
      obj[this.id] = $(this).val()
      json_levels_list.push(obj)

  })
  // json_levels_list.splice(-1,1) // O ultimo eh o botao. Exclui.
  result_cp_gd[bv_collection]['json_levels_list'] = json_levels_list;


  // debugger;

  $.ajax({
    url: '/pt/buscador/bv/' + bv_collection + '/' + id_collection + '/multidimensional_chart/bubble/',
    type: 'post',
    dataType: 'json',
    headers: {
       "cache-control": "no-cache",
       'X-Requested-With': 'XMLHttpRequest',
       "Content-Type" : "application/json; charset=utf-8",
       "Accept" : "application/json",
       'X-CSRFToken': csrf //a varivel csrf provem da pagina html
     },
     data: JSON.stringify(result_cp_gd),
     success: function(data){
       // console.log(data)
       // debugger;

       bubble_data = data.result;
       drawBubbleChart(data.result, 7, 75)
     }
   });
}






// var nodes = []
// var link = []

function recuperaSankeyChart(busca_realizada_str){
  // Recupera os valores da busca.
  if (typeof busca_realizada_str != 'string'){
    var result_cp_gd = getBuscaRealizada({});
  }
  else{
    var result_cp_gd = JSON.parse(busca_realizada_str)
  }

  //
  var json_levels_list = []
  selects = $(".sankey_options")
    .map(function() {
      obj = {}
      obj[this.id] = $(this).val()
      json_levels_list.push(obj)

  })
  json_levels_list.splice(-1,1) // O ultimo eh o botao. Exclui.
  result_cp_gd[bv_collection]['json_levels_list'] = json_levels_list;

  $.ajax({
    url: '/pt/buscador/bv/' + bv_collection + '/' + id_collection + '/multidimensional_chart/sankey/',
    type: 'post',
    dataType: 'json',
    headers: {
       "cache-control": "no-cache",
       'X-Requested-With': 'XMLHttpRequest',
       "Content-Type" : "application/json; charset=utf-8",
       "Accept" : "application/json",
       'X-CSRFToken': csrf //a varivel csrf provem da pagina html
     },
     data: JSON.stringify(result_cp_gd),
     success: function(data){
       // console.log(data)
       drawSankeyChart(data)
  
     }
   });

}

function recuperaPivotTable(busca_realizada_str){
  // Recupera os valores da busca.
  if (typeof busca_realizada_str != 'string'){
    var result_cp_gd = getBuscaRealizada({});
  }
  else{
    var result_cp_gd = JSON.parse(busca_realizada_str)
  }

  //
  var json_levels_list = []
  selects = $(".pivot_options")
    .map(function() {
      obj = {}
      obj[this.id] = $(this).val()
      json_levels_list.push(obj)

  })
  json_levels_list.splice(-1,1) // O ultimo eh o botao. Exclui.
  result_cp_gd[bv_collection]['json_levels_list'] = json_levels_list;

  $.ajax({
    url: '/pt/buscador/bv/' + bv_collection + '/' + id_collection + '/multidimensional_table/pivot_table/',
    type: 'post',
    dataType: 'json',
    headers: {
       "cache-control": "no-cache",
       'X-Requested-With': 'XMLHttpRequest',
       "Content-Type" : "application/json; charset=utf-8",
       "Accept" : "application/json",
       'X-CSRFToken': csrf //a varivel csrf provem da pagina html
     },
     data: JSON.stringify(result_cp_gd),
     success: function(data){
       //usando temporariamente os dados na tabela
       drawPivotTable(data)
     }
   });

}

/**
* Recebe a string da busca do queryBuilder
* Verifica os parametros de facet selecionados no radio button
* Chama Ajax para recuperar grafico multifacet
* Monta Grafico multifacet
* @param {String} busca_realizada_str - Busca realizada no queryBuilder
*/

// Variavel global, acessada pelo div resizeble da legenda.
var json_d3_glb = [];
var extratificacao_legend_label = '';
var elemento_legend_label = '';

function recuperaGraficoDuplo(busca_realizada_str){
  // Recupera os valores da busca.
  if (typeof busca_realizada_str != 'string'){
    var result_cp_gd = getBuscaRealizada({});
  }
  else{
    var result_cp_gd = JSON.parse(busca_realizada_str)
  }


  // Procura no contexto global o valor dos radio buttons dos graficos
  // barchart empilhado.
  var nivel_1 = $('input[name=rb_eixo_x]:checked').attr('value');
  var nivel_2 = $('input[name=rb_eixo_y]:checked').attr('value');

  // Se nao encontrar os radios, configura manualmente.
  if (! nivel_1){
    nivel_1 = default_level_1
  }
  if (! nivel_2){
    nivel_2 = default_level_2
  }


  extratificacao_legend_label = $("label[for= " +  nivel_1 + "]")[0]['innerText']
  elemento_legend_label = $("label[for= " +  nivel_2 + "]")[0]['innerText']
  $('#facet_multiplo').html('')
  $('#extratificacao_legend_label').html('')
  $('#elemento_legend_label').html('')
  $('#extratificacao_legend_label').append( '<i class="fa fa-check"></i> ' + extratificacao_legend_label)
  $('#elemento_legend_label').append( '<i class="fa fa-check"></i> ' + elemento_legend_label )
  $('#facet_multiplo').append('<div class="resize-legend"></div>')

  // Monta o Json com os valores especificos dos radio buttons do
  // grafico de barras facet multidimensional.
  var json_facet = {nivel_1:{
                  'type':'terms',
                  'field':nivel_1, // var nivel_1 = 'bolsas_pt';
                  'limit':100,
                  'facet':{nivel_2:{
                                'type':'terms',
                                'field':nivel_2, // var nivel_2 = 'ano_exact';
                                'limit':100}}
                }
  };

  result_cp_gd[bv_collection]['json_facet'] = json_facet;

  // debugger;

  /*
  * data - recebe todos os dados do grafico dubplo
  * nivel_1 - O valor sao todos os elementos estratificados,
  * trazendo uma "lista (dict)" da qt de elementos por item do eixo y
  */
  function json_solr_2_d3(data){
    json_d3 = [];

    $.each(data, function(nivel_1, elemen_1){
      if ( nivel_1 == 'count'){
        return true
      }
      var nivel_1 = nivel_1
      // console.log(elemen_1)
      var max_length = 0
      var todos_nivel_2 = {}
      $.each(elemen_1.buckets, function( nivel_2, elemen_2){
        var dict = {};
        dict['name'] = elemen_2.val
        dict['data'] = []
          // console.log(elemen_1.count)

        if ( contains(elemen_2.val.toString(),"|")){
          return true
        }
        // console.log(elemen_2.val)

        if (elemen_2.nivel_2.buckets.length > max_length){
          max_length = elemen_2.nivel_2.buckets.length
        }
        $.each(elemen_2.nivel_2.buckets, function(nivel_3, elemen_3){
          if (elemen_3.val.toString().indexOf('|') == -1){
            todos_nivel_2[elemen_3.val] = elemen_3.val
            dict['data'].push(elemen_3)
          }
        })
        json_d3.push(dict)
      })

      /*
      * Este loop e tudo o que se refere ao max_length acima, eh para equalizar o tamanho
      * do array de objestos que passa para o stacked bar.
      * Precisam ser do mesmo tamanho, apesar de nao verificar consistencia dos dados do
      * objeto do array
      */
      $.each(todos_nivel_2, function(id, elemen){
          for (var j=0; j < json_d3.length; j++) {
            var existe = false;
            for (var k=0; k < json_d3[j].data.length; k++) {
              if (json_d3[j].data[k].val == elemen) {
                  existe = true;
              }
            }
            if (!existe){json_d3[j].data[k]={'count':0, 'val':elemen}}
          }
      })
    })
    return json_d3
  }

  $.ajax({
    url: '/pt/buscador/bv/' + bv_collection + '/' + id_collection + '/',
    type: 'post',
    dataType: 'json',
    headers: {
       "cache-control": "no-cache",
       'X-Requested-With': 'XMLHttpRequest',
       "Content-Type" : "application/json; charset=utf-8",
       "Accept" : "application/json",
       'X-CSRFToken': csrf //a varivel csrf provem da pagina html
     },
     data: JSON.stringify(result_cp_gd),
     success: function(data){
       json_d3 = json_solr_2_d3(data.facets);
       useReturnData(json_d3);
       drawStackChart(json_d3, false, null, null, null, null);
     }
   });

}


function useReturnData(data){
    json_d3_glb = data;
    // debugger;
};


/**
* Função cria todos os graficos apartir de um unico JSON fornecido pelo solr API
* @param {JSON} json - Json contendo dados retornados pelo ajax do Solr
*/
function geraCharts(json){
      // Lista que define as funções de desenho que cada categoria ira executar
      var define_render = {
        'datas' : temporalChart,
        'barChart_1':barChart,
        'halfPieChart':halfPieChart,
      }
      // limpa grafico anterior se houver
      $('.group_barchart').html('')
      // console.log(json)
      // console.log('json')

      for (i in json){
        var item = json[i];

        /* é recuperado apartir da chave do facet o grupo
         que o facet pertence e recuperado o atributo render
         da configuração */

        var render = getRender(facetsCategorias,i)
        var label = pegaLabel(facetsCategorias,i)

        if(Object.keys(item).length){
          if(render){
            define_render[render](i, label, item);
          }
        }
      }
}


/** Função que define quais graficos temporais ira ser renderizado */
function temporalChart(id, label, json){
  if( Object.keys(json)[0].indexOf('-') != -1){
    MensalChart(id,label,json)
  }else{
    AnualChart(id,label,json)
  }

}


/** Função que renderiza grafico para apresentar dados anuais */
function AnualChart(id,label, json){

  var margin = {top: 20, right: 20, bottom: 70, left: 40},
    width = (Object.keys(json).length*10)+5 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

  var parseY = d3.time.format("%Y").parse;
  var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);
  var y = d3.scale.linear().range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .tickFormat(d3.time.format("%Y").parse);

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(10);

  var blocos = d3.select('.group_barchart')
              .append('div')
              .attr('id', 'bloco_'+id)
              .style('padding', '20px')
              .style('width', 'auto')
              .attr('class', 'col-md-4 card card-1')

  var titulos = blocos.append('h2')
              .attr('class','titulo')
              .html(label)

  var svg = blocos.append('svg')
              .attr('id',id)
              .attr('width',  width + margin.left + margin.right)
              .attr('height',height + margin.top + margin.bottom)
              .append("g")
                .attr("transform",
                      "translate(" + margin.left + "," + margin.top + ")");

  var refaz_data = {};

  for(var i = 0,j =0; j < Object.keys(json).length; j+=2,i++){
      refaz_data[ i ] = {
        'label': Object.keys(json)[j],
        'ano': parseY(Object.keys(json)[j]),
        'valor': json[Object.keys(json)[j]].count,
      }
  }



  // ordena por data
  refaz_data = d3.entries(refaz_data)
                .sort( function(a,b) {
                   try {
                        var context = d3.ascending(a.value.ano,b.value.ano);
                    }
                    catch(err) {
                        var context = a.value.ano;
                    }
                   return context
   } );



  x.domain( refaz_data.map(function(d) { return d.value.ano; }) );
  y.domain( [0, d3.max(refaz_data, function(d) { return d.value.valor; }) ]);

  try{
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
      .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", "-.55em")
        .attr("transform", "rotate(-90)" );

  }catch(err){
    // debugger
  }
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Quantidade");

  svg.selectAll("bar")
      .data(refaz_data)
    .enter().append("rect")
      .style("fill", "steelblue")
      .attr("x", function(d) { return x(d.value.ano); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.value.valor); })
      .attr("height", function(d) { return height - y(d.value.valor); });

}




/** Função que renderiza grafico para apresentar dados mensais usando linha com grade em anos */
function MensalChart(id,label,json) {

  // Parse the date / time
  var	parseYm = d3.time.format("%Y-%m").parse;
  // var  margin = {top: 20, right: 20, bottom: 30, left: 50},
  var margin = {top: 20, right: 20, bottom: 70, left: 40},
    width = (Object.keys(json).length)+500 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

  var blocos = d3.select('.group_barchart')
              .append('div')
              .attr('id', 'bloco_'+id)
              .style('padding', '30px')
              .style('width', 'auto')
              .attr('class', 'col-md-4 card card-1')

  var titulos = blocos.append('h2')
              .attr('class','titulo')
              .html(label)

  var svg = blocos.append('svg')
                  .attr('id',id)
                  .attr('width',  width + margin.left + margin.right)
                  .attr('height', height + margin.top + margin.bottom)
                  .append("g")
                  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  g = svg.append("g")
    .attr('width', width)
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var refaz_data = {};

  for(var i = 0,j =0; j < Object.keys(json).length; j+=2,i++){
    refaz_data[ i ] = {
      'label': Object.keys(json)[j],
      'ano': parseYm(Object.keys(json)[j]),
      'valor': json[Object.keys(json)[j]].count,
    }
  }

  // ordena por data
  refaz_data = d3.entries(refaz_data)
                .sort( function(a,b) {
                   try {
                        var context = d3.ascending(a.value.ano,b.value.ano);
                    }
                    catch(err) {
                        var context = a.value.ano;
                    }

                   return context
   } );

  var x = d3.time.scale()
      .rangeRound( [0, width-margin.left] );

  var y = d3.scale.linear()
      .rangeRound( [height, 0] );




  var line = d3.svg.line()
      .interpolate("cardinal")
      .x(function(d) { return x(d.value.ano); })
      .y(function(d) { return y(d.value.valor); });


  x.domain(d3.extent(refaz_data, function(d) { return d.value.ano; }));
  y.domain(d3.extent(refaz_data, function(d) { return d.value.valor; }));

  //array de meses por extenso
  var meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezenbro"];

  //desenha linha
  g.append("path")
      .datum(refaz_data)
      .attr("fill", "none")
      .attr("stroke", "#e44998")
      .attr("class", "line_chart")
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-width", 1)
      .attr("d", line);

  // Define o div para o tooltip
  var div = d3.select("body").append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);

      // funções para desenhar a grade
      yticksMax = 20
      rangeMax = d3.max(refaz_data, function(d) { return d.value.valor; })
      yticks =  rangeMax > yticksMax ? yticksMax : rangeMax;

      xticks = 10;

      function make_x_axis() {
        return d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks( xticks )

      }

      function make_y_axis() {
        return d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks( yticks)
      }

      // desenha a grade
      svg.append("g")
      .attr("class", "grid")
      // .attr("transform", "translate(" + margin.left + "," + height+margin.top+ ")")
      .attr("transform", "translate(" + margin.left + "," + (height+margin.top) + ")")
      .call(make_x_axis()
            .tickSize(-height, 0, 0)
            .tickPadding(20)
      )

      svg.append("g")
      .attr("class", "grid")
      .attr("transform", "translate(" + margin.top + "," + margin.top + ")")
      .call(make_y_axis()
            .tickSize(-width, 0, 0)


      )

  // funções de formatação da data
  var parseMes =d3.time.format("%m")
  var parseAno =d3.time.format("%Y")

  //Adciona pontos na linha
  svg.selectAll("dot")
      .data(refaz_data)
      .enter().append("circle")
          .attr("r", 1.5)
          .attr("cx", function(d) { return x(d.value.ano)+ margin.left })
          .attr("cy", function(d) { return y(d.value.valor)+ margin.top ; })
          .style('fill', '#e44998')
          .on("mouseover", function(d) {
              div.transition()
                  .duration(200)
                  .style("opacity", .9);
              div	.html( meses[parseInt(parseMes(d.value.ano))] +' <br> '+parseAno(d.value.ano) )
                  .style("left", (d3.event.pageX) + "px")
                  .style("top", (d3.event.pageY - 28) + "px");
              })
          .on("mouseout", function(d) {
              div.transition()
                  .duration(500)
                  .style("opacity", 0);
          });

}




/**
* Lista de grafico de barras na horizontal
*/
function halfPieChart(id, label, json){

    //https://jsfiddle.net/rcxp0udt/

    var datasetTotal = [];
    for (f in json['facets']){
      pct = json['facets'][f]['count'] * 100 / json['count']
      pct = pct.toFixed(2)
      datasetTotal.push({'label':' ('+ pct +'%) ' + f , value:json['facets'][f]['count'] })
    }

    var blocos = d3.select('.group_half_pie_chart')
                .append('div')
                .attr('id', 'bloco_'+id)
                .attr('class', 'half_pie_chart_div')
                .classed('col-xs-2', 'true')

    var titulos = blocos.append('h4')
                .attr('class','half_donut')
                .style('min-height','70px')
                .html(label)

    var pi = pi = Math.PI;


    var svg = blocos.append('svg')
                .attr('id',id)
                .attr("preserveAspectRatio", "xMinYMin meet")
                .attr("viewBox", "0 0 120 120")
                .classed("svg-content", true)
                .style("position", 'relative')
                .attr("transform", "translate(0,-20)")


                	.append("g")

                svg.append("g")
                	.attr("class", "slices");
                svg.append("g")
                	.attr("class", "labelName");
                svg.append("g")
                	.attr("class", "labelValue");
                svg.append("g")
                	.attr("class", "lines");

                var width = 100,
                    height = 120,
                	radius = Math.min(width, height) / 2;

                var pie = d3.layout.pie()
                	.sort(null)
                  .startAngle(-90 * (pi/180))
                        .endAngle(90 * (pi/180))
                	.value(function(d) {
                		return d.value;
                	});

                var arc = d3.svg.arc()
                	.outerRadius(radius * 0.7)
                	.innerRadius(radius * 0.45);

                var outerArc = d3.svg.arc()
                	.innerRadius(radius * 0.9)
                	.outerRadius(radius * 0.9);

                var legendRectSize = (radius * 0.05);
                var legendSpacing = radius * 0.02;


                var div = d3.select("body").append("div").attr("class", "toolTip");
                svg.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

                var colorRange = d3.scale.category10();
                var color = d3.scale.ordinal()
                	.range(colorRange.range());


                change(datasetTotal);


                d3.selectAll("input")
                	.on("change", selectDataset);

                function selectDataset()
                {
                	var value = this.value;
                	if (value == "total")
                	{
                		change(datasetTotal);
                	}
                	else if (value == "option1")
                	{
                		change(datasetOption1);
                	}
                	else if (value == "option2")
                	{
                		change(datasetOption2);
                	}
                }

                function change(data) {

                	/* ------- PIE SLICES -------*/
                	var slice = svg.select(".slices").selectAll("path.slice")
                        .data(pie(data), function(d){ return d.data.label });

                    slice.enter()
                        .insert("path")
                        .style("fill", function(d) { return color(d.data.label); })
                        .attr("class", "slice");

                    slice
                        .transition().duration(1000)
                        .attrTween("d", function(d) {
                            this._current = this._current || d;
                            var interpolate = d3.interpolate(this._current, d);
                            this._current = interpolate(0);
                            return function(t) {
                                return arc(interpolate(t));
                            };
                        })
                    slice
                        .on("mousemove", function(d){
                            div.style("left", d3.event.pageX+10+"px");
                            div.style("top", d3.event.pageY-25+"px");
                            div.style("display", "inline-block");
                            div.html((d.data.label)+"<br>"+(d.data.value));
                        });
                    slice
                        .on("mouseout", function(d){
                            div.style("display", "none");
                        });

                    slice.exit()
                        .remove();

                    var legend = svg.selectAll('.legend')
                        .data(color.domain())
                        .enter()
                        .append('g')
                        .attr('class', 'legend')
                        .attr('transform', function(d, i) {
                            var height = legendRectSize + legendSpacing + 10;
                            var offset =  height * color.domain().length / 2;
                            var horz = -15 * legendRectSize;
                            var vert = i * height + 12;
                            return 'translate(' + horz + ',' + vert + ')';
                        });

                    legend.append('rect')
                        .attr('width', legendRectSize)
                        .attr('height', legendRectSize)
                        .style('fill', color)
                        .style('stroke', color);

                    legend.append('text')
                        .attr('x', legendRectSize + legendSpacing)
                        .attr('y', legendRectSize - legendSpacing)
                        .attr("font-family","roboto")
                        .attr("font-size","8px")
                        .text(function(d) { return d; });

                    /* ------- TEXT LABELS -------*/
                    /*

                    var text = svg.select(".labelName").selectAll("text")
                        .data(pie(data), function(d){ return d.data.label });

                    text.enter()
                        .append("text")
                        .attr("dy", ".35em")
                        .text(function(d) {
                            return (d.data.label+": "+d.value+"%");
                        });

                    function midAngle(d){
                        return d.startAngle + (d.endAngle - d.startAngle)/2;
                    }

                    text
                        .transition().duration(1000)
                        .attrTween("transform", function(d) {
                            this._current = this._current || d;
                            var interpolate = d3.interpolate(this._current, d);
                            this._current = interpolate(0);
                            return function(t) {
                                var d2 = interpolate(t);
                                var pos = outerArc.centroid(d2);
                                pos[0] = radius * (midAngle(d2) < Math.PI ? 1 : -1) -10;
                                return "translate("+ pos +")";
                            };
                        })
                        .styleTween("text-anchor", function(d){
                            this._current = this._current || d;
                            var interpolate = d3.interpolate(this._current, d);
                            this._current = interpolate(0);
                            return function(t) {
                                var d2 = interpolate(t);
                                return midAngle(d2) < Math.PI ? "start":"end";
                            };
                        })
                        .text(function(d) {
                            return (d.data.label+": "+d.value+"%");
                        });


                    text.exit()
                        .remove();
                    */
                    /* ------- SLICE TO TEXT POLYLINES -------*/
                    /*
                    var polyline = svg.select(".lines").selectAll("polyline")
                        .data(pie(data), function(d){ return d.data.label });

                    polyline.enter()
                        .append("polyline");

                    polyline.transition().duration(1000)
                        .attrTween("points", function(d){
                            this._current = this._current || d;
                            var interpolate = d3.interpolate(this._current, d);
                            this._current = interpolate(0);
                            return function(t) {
                                var d2 = interpolate(t);
                                var pos = outerArc.centroid(d2);
                                pos[0] = radius * 0.85 * (midAngle(d2) < Math.PI ? 1 : -1);
                                return [arc.centroid(d2), outerArc.centroid(d2), pos];
                            };
                        });

                    polyline.exit()
                        .remove();
                    */
                };

}












/**
* Lista de grafico de barras na horizontal
*/
function barChart(id, label, json){
    var blocos = d3.select('.group_barchart')
                .append('div')
                .attr('id', 'bloco_'+id)
                .style('padding', '10px')
                .style('max-height', '300px')
                .style('overflow-y', 'auto')
                .attr('class', 'col-md-4 card card-1')

    var titulos = blocos.append('h2')
                .attr('class','titulo')
                .html(label)

    var svg = blocos.append('svg')
                .attr('id',id)
                .attr('width',500)
                .attr('height', (Object.keys(json['facets']).length*18)+150)

    var refaz_data = {};
    var altura_bar = 20;
    var idx = 0;

    for (facet in json['facets']){
      refaz_data[ idx ] = {
      'label': json['facets'][facet]['label'],
      'valor': json['facets'][facet]['count']
      }
      idx++;
    }

    // ordena por valor
    refaz_data = d3.entries(refaz_data)
                  .sort( function(a,b) {
                     try {
                          var context = d3.descending(a.value.valor,b.value.valor);
                      }
                      catch(err) {
                          var context = a.value.valor;
                      }

                     return context
                   } );

  if( refaz_data.length  ){
    var x = d3.scale.log()
      .base(Math.E)
      .domain([0.5, refaz_data[0].value.valor ])
      .range([ 0, svg.attr('width') ]);

      var group = svg.selectAll('#'+id)
                    .data(refaz_data)
                    .enter()
                    .append('g')

      var rects =  group.append('rect')
                    .style("fill","steelblue")
                    .attr('width', function(d) {  return x(d.value.valor) } )
                    .attr("height", 5 )
                    .style("background-color","yellow")
                    .style("border","2px solid orange")
                    .attr('x',function(d) { return 0 })
                    .attr('y',function(d,i) {return (altura_bar*i)+altura_bar+(10*i)} )

      var texts =  group.append('text')
                    .text(function(d){return d.value.valor +' - '+d.value.label;})
                    .attr("font-family","roboto  ")
                    .attr("font-size","12px")
                    .attr("y",function(d,i) {return (altura_bar*i)+altura_bar+(10*i)+17})
                    .style("border","20px solid orange");
  }
}






/*
* Funcoes genericas para os graficos.
*/

/**
* Função retorna label do facet, comparando categorias de lista de referencia e facet
* @param {Array} referência - Lista de Arrays que contem todos os facets
* @param {String} id - Valor da chave que existe no Array do facet
*
*/
function pegaLabel(referencia, id){
  var result = ''

  //itera categorias e define qual categoria o item atual pertence
    //estrutura intimamente dependente da estrutura de dicionario do conf.py
  $.each(referencia,function(i,group){

      $.each(group.facetGroup, function(u,item){
        var label;
        $.each(item.facets, function(u,facet){
          if(facet['chave'] === id ){
            result = decodeURIComponent(escape(facet['label']));
          }
        });
      });
  });
  return result;
}



/**
* Função define categoria do facet passado no id e encontrado na lista de facets
*
* @param {Array} referência - Lista de Arrays que contem todos os facets
* @param {String} id - Valor da chave que existe no Array do facet
*
*/
function getRender(referencia, id){
  // remove extensão em nome da categoria
  // var name = id.replace('_exact','');
  var render = ''

  //itera categorias e define qual categoria o item atual pertence
  //estrutura de loop intimamente dependente da estrutura de dicionario do conf.py
  $.each(referencia,function(i,group){
    //loop nivel de grupos
    $.each(group.facetGroup, function(u,item){
        $.each(item.facets, function(u,facet){
            if(facet['chave'] == id){
              render = item.render;
            }
        });
    });
  });
  return render;
}
