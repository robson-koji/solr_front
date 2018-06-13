

/*
*
*
* Definicao da classe Grupo de Componentes, que agrupa componentes.
*
*
*/
function GroupComponent(){
  this.instances = []
}

GroupComponent.prototype.add = function(obj){
  this.instances.push(obj)
}

GroupComponent.prototype.filterByOrderData = function(key, reverse){
  $('#'+key).find('.test').sort(function (a, b) {
     return $(a).attr('data-percentage') - $(b).attr('data-percentage');
  })
  .appendTo('.testWrapper');
}

GroupComponent.prototype.ArrayObjectOrder= function(list, field, reverse){
  fields = field.split('.')
  var ordem = list.sort( function(a,b){
    var ac = a.contexto[0]
    var bc = b.contexto[0]

    if(fields.length > 0){
      for(var i =0; i < fields.length; i++){
        ac = ac[fields[i]] || ''
        bc = bc[fields[i]] || ''
      }
      var an = ac,
      bn = bc;
      }else{
        var an = a[field],
        bn = b[field];
      }

      if( an > bn){
        return 1;
      }

      if (an < bn){
        return -1;
      }
      return 0;
  })
  return ordem
}

GroupComponent.prototype.renderExec = function(clean, byorder){
   $('#loader_facets').css('display', 'flex');
  var clear = clean || false
  var byorder = byorder || false
  if(clear){
    this.instances[0].cleanContainer()
  }

  if(byorder){
    var instances_ordem = this.ArrayObjectOrder(this.instances, byorder)
    for(var i =0; i < instances_ordem.length; i++){
      instances_ordem[i].exec()
    }
  }else{
    for(var i =0; i < this.instances.length; i++){
      this.instances[i].exec()
    }
  }
}


GroupComponent.prototype.renderAll = function(clean){
  if (clean == true){
    for(var i =0; i < this.instances.length; i++){
      if(typeof this.instances[i].anexo != 'undefined'){
        var container = document.getElementById(this.instances[i].anexo)
        container.innerHTML = ''
      }
    }
  }

  for(var i =0; i < this.instances.length; i++){
    if(typeof this.instances[i].anexo != 'undefined' ){
      var container = document.getElementById(this.instances[i].anexo)
      container.innerHTML += this.instances[i].render()
    }
  }
  this.instances = []
}






/**
*
*
* Definicao de classe dos Componentes
* Cada tipo de comonente extende esta classe.
*
*
**/
function Component(contexto, anexo, ordem) {
    //construtor da classe
    //Dicionario (objeto) contendo chave valor para as variaveis usadas no template
    this.contexto = contexto;

    // id do container que armazena o componente
    this.anexo = anexo;

    ordem = ordem ? ordem : false
    this.ordem = ordem
}

// metodo destroi instancia
Component.prototype.destroy = function () {
  delete this
}

Component.prototype.template = function(){
  // Interface deve ser definida na subclasse contendo o html e variaveis de contexto usadas
  // deve retornar uma string html
}

//metodo retorna html do componente
Component.prototype.render = function(){
  return this.template()
}

Component.prototype.equals = function(other) {
 return other.contexto == this.contexto && other.anexo == this.anexo;
};
// anexa todos os componentes da classe em seus respectivos containers








/**
* Criacao do componente de Totais
*/
function TotaisComponent(contexto, anexo){
  Component.call(this, contexto, anexo);
}

// herda de Component
TotaisComponent.prototype = new Component();
TotaisComponent.prototype.constructor = TotaisComponent// ajusta apontamento para classe correta


TotaisComponent.prototype.template = function(){
  if(this.contexto['total']){

    return '<div class="card has-value col-md-4"> \
      <div class="card__value"> \
        <p>'+this.contexto['total']+'</p> \
      </div> \
      <p class="card__desc"> \
        '+ this.contexto['label'] +'\
      </p> \
    </div>';

  }else{

    return '<div class="card"> \
      <div class="card__value"> \
        <p>0</p> \
      </div> \
      <p class="card__desc"> \
        '+ this.contexto['label'] +' \
      </p> \
    </div>'

  }
}






/**
* Criacao do componente Doc
*/
function DocsComponent(contexto, anexo){
  Component.call(this, contexto, anexo);
}

// herda de Component
DocsComponent.prototype = new Component();
DocsComponent.prototype.constructor = DocsComponent// ajusta apontamento para classe correta


DocsComponent.prototype.template = function(){
  var id_html = this.contexto['label'].replace(/ /g, '_')+'_id'
  var print = false
  var links = ''
  var height = ''
  for(var i = 0; i < this.contexto['links'].length; i++){

    // debugger;
    if (this.contexto['links'][i].url === ''){
      print = true
      links += this.contexto['links'][i]['titulo'] + '<hr>'
    }
    else if(typeof this.contexto['links'][i].url != 'undefined') {
      print = true
      links += '<a href="' + this.contexto['links'][i]['url']+ '" target="_blank">' + this.contexto['links'][i]['titulo'] + '</a><hr>'

      // Para os conteudos de processos estah com valor hardcoded.
      // Rever isso.
      if (this['contexto']['colunas'] == 6){
        height = '300px'
      }
    }
  }
  if(print){
    var subtitulo = this.contexto['situacao'] || '';

    return '<div class="col-md-' + this.contexto['colunas'] + '" style="height:' + height + '">\
    <h2 class="title_primary">'+this.contexto['label']+'</h2> \
    <div class="col-md-11 has-col" id="todos_documentos">\
      <div class="content_section__header">\
        <h3 class="title_secondary">'+subtitulo +'</h3>\
        <div class="info_qtd" id="'+id_html+'_qt">\
        '+this.contexto['total']+'</div> \
      </div> \
      <ul id="'+id_html+'"> \
      '+  links +  '\
      </ul></div></div>'

    /*
    return '<div class="col-md-6" style="height:300px">\
    <h2 class="title_primary">'+this.contexto['label']+'</h2> \
  <div class="col-md-11 has-col" id="todos_documentos">\
    <div class="content_section__header">\
      <h3 class="title_secondary">'+subtitulo +'</h3>\
      <div class="info_qtd" id="'+id_html+'_qt">\
      '+this.contexto['total']+'</div> \
    </div> \
    <ul id="'+id_html+'"> \
    '+  links +  '\
    </ul></div></div>'
    */
  }
  else{
    return ' '
  }



}



/**
* Componente do tipo Exec.
* Deve ser executado para gerar o componente ao invez de renderizado
**/
function FacetComponentExec(contexto, anexo, ordem){
  Component.call(this, contexto, anexo, ordem);
}

// herda de Component
FacetComponentExec.prototype = new Component();
FacetComponentExec.prototype.constructor = FacetComponentExec// ajusta apontamento para classe correta


FacetComponentExec.prototype.html = function(id, label, order){

  order = order || 0

  html = '\
  <style>.list-group-item {\
    padding: 3px 5px;\
    border: 1px solid #ddd; </style>\
  <!-- botão --> \
   <a href="#'+id+'" role="button" data-target="#'+ id +'" data-order="'+order+'"class="btn btn-tag" data-toggle="modal"> <i class="fa fa-check" hidden></i> '+label+' <i class="contador"></i> </a>' +

  ' <!-- modal -->\
   <div id="'+id+'" class="modal" data-easein="swoopIn" tabindex="-1" role="dialog" aria-labelledby="'+id+'ModalLabel" aria-hidden="false">\
     <div class="modal-dialog">\
       <div class="modal-content">\
         <div class="modal-header">\
           <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>\
           <h4 class="modal-title" id="'+id+'ModalLabel">'+label+'</h4>'+
         '</div>\
         <div class="modal-body" style="max-height: 70vh; overflow-y: auto;">\
           <div id="tree_'+id+'" class="facet_list"></div>'+
         '</div>'+
         '<div class="modal-footer">'+
            '<button class="btn btn-default form_facet_submit" id="btn-uncheck-all_' + id + '" data-target="tree_'+id+'" data-dismiss="modal" aria-hidden="true">Limpar Filtros</button>'+
            '<button class="btn btn-default form_facet_submit" id="div_id' + id + '" data-dismiss="modal" aria-hidden="true">Filtrar</button>'+
            '<button class="btn btn-default" data-dismiss="modal" aria-hidden="true">Cancelar</button>'+
         '</div></div></div></div>';

   return html

}
FacetComponentExec.prototype.cleanContainer = function(){
  $('#'+this.anexo).html('')
}

FacetComponentExec.prototype.limparselecaoNo = function(id){
  var selecao = $(id).treeview('getEnabled');
  for (var i =0; i < selecao.length; i++){
    var facet = selecao[i]
    var chave = facet.tag[0].split(':')[0]
    // define a posição index do elemento
    // var index = selectedFacets[chave].indexOf(facet.tag[0].split(':')[1])
    // deleta item encontrado
    removeAllElementSelectedFacets(chave)
    break
  }
}


FacetComponentExec.prototype.exec = function(){
  // variaveis necessarias no contexto
  // array[{
  // label
  // situacao
  // data
 //}, lista de facets selecionados]
  $('#loader_facets').hide()
  var id_html = this.contexto[0]['id']
  if( this.contexto[0].count > 0){
    // caso existir definição de agrupamento
    if (typeof this.contexto[0].groupBy != 'undefined'){
      // se elemento com id ja existe dentro do alvo anexo
      if( $('#'+this.anexo).find('#'+this.contexto[0].groupBy.id).length ){
        //anexa elemento no grupo
        $('#'+this.anexo+ ' #'+this.contexto[0].groupBy.id).append(this.html(id_html, this.contexto[0]['label'], this.contexto[0]['order'] ))
        $('#'+this.anexo+ ' #'+this.contexto[0].groupBy.id).ordenaElementByAtribute('a', 'data-order')
      }
      //caso negativo inclui elemento no alvo anexo
      else {
        //inclui grupo
        var ordenamento = this.contexto[0].groupBy.order || 0
        $('#'+this.anexo).append('<fieldset data-order='+ordenamento+' ><legend>'+this.contexto[0].groupBy.label +'</legend> <div class="groupBy" id="'+this.contexto[0].groupBy.id+'"></div></fieldset>')
        //anexa elemento no grupo
        $('#'+this.anexo+ ' #'+this.contexto[0].groupBy.id).append(this.html(id_html, this.contexto[0]['label'], this.contexto[0]['order'] ))
        $('#'+this.anexo+ ' #'+this.contexto[0].groupBy.id).ordenaElementByAtribute('a', 'data-order')
      }
    }else{
      $('#'+this.anexo).append(this.html(id_html, this.contexto[0]['label'], this.contexto[0]['order'] ))
      $('#'+this.anexo+ ' #'+this.contexto[0].groupBy.id).ordenaElementByAtribute('a', 'data-order')
    }

    var itens = [makeFacetObjectTree(this.contexto[0], this.contexto[1], this,ordem =this.ordem)] || []

    if( itens.length > 0){
      $('#tree_'+id_html).treeview({
        data: itens,
        levels: 2,
        showCheckbox: true,
        multiSelect: true, // permite selecionar multiplos valores
        highlightSelected: false, // remove coloração do selected
      });

      // /quando existir seleção de algum nó
      $('#tree_'+id_html).on('nodeSelected', function(event, data){
        // aqui deve existir metodo que checa nó ao
        // selecionaar quando nó não possui filhos
        $('#tree_'+id_html).treeview('checkNode', [ data.nodeId,  { silent: false } ]) ;
      });

        //quando existir seleção de algum nó
      $('#tree_'+id_html).on('nodeUnselected', function(event, data){
        // aqui deve existir metodo que checa nó ao
        // deselecionar quando nó não possui filhos
        $('#tree_'+id_html).treeview('uncheckNode', [ data.nodeId,  { silent: false} ]) ;
      });

      // //quando caixa do nó for checada
      $('#tree_'+id_html).on('nodeChecked', function(event, data){
        if(data.nodeId == 0){
          addElementInSelectedFacets(data.tag[0].split(':')[0], '*')
          $('#tree_'+id_html).treeview('checkAll', { silent: false})
          }else{
            addElementInSelectedFacets(data.tag[0].split(':')[0], data.tag[0].split(':')[1])
            if(typeof data.nodes != 'undefined'){
              for(var i = 0; i < data.nodes.length; i++){
                $('#tree_'+id_html).treeview('checkNode', [ data.nodes[i].nodeId,  { silent: false } ]) ;
                addElementInSelectedFacets(data.nodes[i].tag[0].split(':')[0], data.nodes[i]  .tag[0].split(':')[1])
              }
            }
          }
      });

      //quando caixa do nó for deschecada
      $('#tree_'+id_html).on('nodeUnchecked', function(event, data){
          if(data.nodeId == 0){
            // removeElementInSelectedFacets(data.tag[0].split(':')[0], '*')
            removeAllElementSelectedFacets(data.tag[0].split(':')[0])
            //ativa ignoreChildren para aliviar a carga de processamento na recursividade do evento
            $('#tree_'+id_html).treeview('uncheckAll', { silent: true, ignoreChildren: true })
          }else{
            var paiNode =  $('#tree_'+id_html).treeview('getParent', [data.nodeId])
            if(typeof data.nodes != 'undefined'){
              for(var i=0; i < data.nodes.length; i++){
                  $('#tree_'+id_html).treeview('uncheckNode', [data.nodes[i].nodeId, {selent: true}])
                  removeElementInSelectedFacets(data.nodes[i].tag[0].split(':')[0], data.nodes[i].tag[0].split(':')[1])
              }
            }
            removeElementInSelectedFacets(data.tag[0].split(':')[0], data.tag[0].split(':')[1])
            if(typeof paiNode.nodeId != undefined){
              if(paiNode.state.checked ){
                // laço necessario para deselecionar pais sem reexecutar evento e causar seleções indesejadas
                  while(typeof paiNode.parentId != 'undefined' || paiNode.nodeId == 0){
                    $('#tree_'+id_html).treeview('uncheckNode', [paiNode.nodeId, { silent: true }])
                    removeElementInSelectedFacets(paiNode.tag[0].split(':')[0], paiNode.tag[0].split(':')[1])
                    paiNode =  $('#tree_'+id_html).treeview('getParent', [paiNode.nodeId])
                  }
              }
            }
          }
      });
    }

    // lida com botões do componente
    var classe = this

    $('button[id^=btn-uncheck-all_'+id_html+']').click(function(){
       classe.limparselecaoNo('#'+this.dataset.target) ;
       getData();
    })

      // Trata evento de clique do botao de submite no modal dos facets
    $('#div_id' + id_html).click(function(){
        // Chama o servidor para recuperar os dados.
        getData();
    })

      // caso elemento ainda não existir inclui
      if($('#'+classe.anexo+' #menu').length == 0){
        $('#'+classe.anexo).prepend('<div id="menu" style="display:inline-flex"></div>')
      }

      if( this.checked == true){
        if($('#'+classe.anexo+' #menu #limpaAllFiltros').length == 0){
          $('#'+classe.anexo+' #menu').append('\
          <button id="limpaAllFiltros" class="btn btn-info" style="margin-left:10px">\
          <i class="fa fa-erase"></i>\
          Limpa todos os Filtros\
          </button>')
        }
        /*
        Limpa todos os facets,
        exceto se indicar que eh funil de uma collection anterior
        */
        $('#'+classe.anexo+' #menu #limpaAllFiltros').on('click', function(){
          Object.keys(selectedFacets).forEach(function(key){
            // Indica que eh facet de funil
            // '/cross_collection_/y' causa problema em IE
            if (! key.match(RegExp("cross_collection_","i"))){
              delete selectedFacets[key]
            }
          });
          getData();
        })
      }


      // adiciona menu de ordenação
      if($('#'+classe.anexo+' #menu #ordena').length == 0){
        
        $('#'+classe.anexo+' #menu').append('\
        <span id="ordena" style="margin-left:10px;">\
        <button id="Alfabetica" class="btn btn-default" data-order=[\"+text\"] onclick="order_facet(this, [\'+text\'])" data-toggle="popover" title="Ordena facets" data-trigger="hover" data-placement="top" data-content="por ordem Alfabética">\
        <i class="glyphicon glyphicon-sort-by-alphabet"></i>\
        </button>\
        <button id="Alfabetica-alt" class="btn btn-default" data-order=[\"-text\"] onclick="order_facet(this, [\'-text\'])" data-toggle="popover" title="Ordena facets" data-trigger="hover" data-placement="top" data-content="por ordem Alfabética inversa">\
        <i class="glyphicon glyphicon-sort-by-alphabet-alt"></i>\
        </button>\
        <button id="Numerica" class="btn btn-default" data-order=[\"+count\"] onclick="order_facet(this, [\'+count\'])" data-toggle="popover" title="Ordena facets" data-trigger="hover" data-placement="top" data-content="por quantidade">\
        <i class="glyphicon glyphicon-sort-by-order"></i>\
        </button>\
        <button id="Numerica-alt" class="btn btn-default" data-order=[\"-count\"] onclick="order_facet(this, [\'-count\'])" data-toggle="popover" title="Ordena facets" data-trigger="hover" data-placement="top" data-content="por quantidade inversa">\
        <i class="glyphicon glyphicon-sort-by-order-alt"></i>\
        </button>\
        </span>')

        if (typeof colore_botao != 'undefined'){
          $('#'+colore_botao).addClass('btn-success')
        }
        $('[data-toggle="popover"]').popover();


      }


  }
}

/* monta unidade de objeto usado no componente de facet
recursivamente usado para construir arvore de facets */
function makeFacetObjectTree(item, selecteds, element, ordem){

    ordem = ordem || false
    if(typeof item != 'undefined'){
      var itens = item['itens'] || []
      var label = item['label']  || ''
      var tag = ''
      if(  item['id'] != element.contexto[0].id){
        tag = element.contexto[0].id +':' + item['id']
      }else{
        tag = element.contexto[0].id +':*'
      }

      var obj = {}
      if (typeof item.count != 'undefined'){
        if(tag.split(':')[1] != '*'){
          label = label + ' ('+item.count+')'
        }
      }

      obj['text'] = label
      obj['count'] = item.count && typeof item.count != 'function' ? item.count : 0
      obj['tag'] = [tag]
      obj['selectable'] = true
      obj['color'] = "#000"

      var contador = {}
      contador[element.contexto[0].id] = 0

      if( typeof selecteds == 'undefined'){
        selecteds = []
      }

      /**se estiver dentro da seleção deve ser checado**/
      // codigo exempl

      if($.inArray(tag, selecteds) >= 0){
        if(typeof element != 'undefined'){
          // nao faz nada
        }

        contador[element.contexto[0].id] += 1

        //pega botão do facet
        $('a[href^="#'+ element.contexto[0]['id'] +'"')
        .addClass('active')
        .find('i').show()

        // dados possiveis em state
          // checked: true,
         // disabled: true,
         // expanded: true,
         // selected: true

        // usado para verificação externa
        element.checked = true;
        //
        // //checa e expande elemento
        obj['state'] = {expanded: true, checked: true}

      }

      for(var i = 0; i < itens.length; i++){

        if ( typeof obj['nodes'] == 'undefined'){
          obj['nodes'] = []
        }

        var unit = itens[i]

        var _obj = makeFacetObjectTree(unit, selecteds, element, ordem )

        obj.nodes.push(_obj)

        // so faz a ordenação depois que todos os elementos estiverem incluidos no obj
        if(obj.nodes.length >= item['itens'].length){
            // ordena elementos filhos alfabeticamente usando campo texto do obj

            if(ordem){
              // lista do parametro de ordenamento
              ordenamento = ordem
            }else{
              // ordenamento padrão
              ordenamento = ['-count', '+text']
            }

            // chama a função convertendo array em objeto Argument usando metodo apply
            obj.nodes = obj.nodes.sortBy.apply(obj.nodes, ordenamento)
       }
      }

      return obj
    }
}


/**
* Componente do tipo Exec
* Deve ser executado para gerar o componente ao invez de renderizado
**/
function DropdownFormComponentExec(contexto, anexo, ordem){
  Component.call(this, contexto, anexo, ordem);
}

// herda de Component
DropdownFormComponentExec.prototype = new Component();
DropdownFormComponentExec.prototype.constructor = DropdownFormComponentExec// ajusta apontamento para classe correta


DropdownFormComponentExec.prototype.template = function(id, click_interface, fields){
// componente Botão dropdwon com conteudo editavel

    id =  id || ''
    fields = fields || []

    if (typeof click_interface != 'undefined'){
      var element = $(click_interface)
      $(element).attr('id', 'dropdown'+id )
      $(element).attr('data-toggle', 'dropdown')
      $(element).attr('aria-haspopup', 'true')
      $(element).attr('aria-expanded', 'false')
      click_interface = $(element).prop('outerHTML')

    }else{
      click_interface = '<i class="glyphicon glyphicon-info-sign dropdown-toggle" id="dropdown'+id+'" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="font-size:18px; color:white"></i>'
    }

    html = '<span id="'+id+'" class="dropdown"> '+ click_interface +'\
        <div class="dropdown-menu" aria-labelledby="dropdown'+id+'" style="min-width:250px;" >\
        <div class dropdown-content" style="margin:15px">\
        <form class="px-4 py-3" >'

        for (var i = 0; i < fields.length; i++){
          html += '<div class="form-group">\
                    <label for="">'+fields[i]['label']+'</label>\
                    <a href="#" id="dp-field_'+fields[i]['id']+'" data-name="'+fields[i]['label']+'" data-params={csrfmiddlewaretoken:"'+csrf+'"}  data-mode="'+fields[i]['mode']+'" data-type="'+fields[i]['type']+'"  data-pk ="'+fields[i]['pk']+'" data-url="'+fields[i]['url_ajax']+'" >'+fields[i]['initial_data']+'</a>\
                  </div>'
        }

    html += '</form>\
            </div>\
            </span>'

    return html
}

DropdownFormComponentExec.prototype.cleanContainer = function(){
  $('#'+this.anexo).html('')
}

DropdownFormComponentExec.prototype.exec = function(){

  // variaveis necessarias no contexto
  // {
  // id : string
  // click_interface : string(html)
  // fields : array[{
  //  id
  //  label
  //  type (
  //     text
  //     textarea
  //     select
  //     date
  //     datetime
  //     dateui
  //     combodate
  //     html5types
  //     checklist
  //     wysihtml5
  //     typeahead
  //     typeaheadjs
  //     select2
  //  )
  //  initial_data
  //  url_ajax
  //  mode (inline or popup)
  // }]
  // }



    $('#'+this.anexo).append(this.template(this.contexto['id'], this.contexto['click_interface'], this.contexto['fields'] ))

    //ativa todos os fileds para edição
    for(var i =0; i < this.contexto['fields'].length; i++){
      $('#dp-field_'+this.contexto['fields'][i]['id']).editable({
        success : function ( response , newValue ) {
          console.log(response)
          if ( response.status == 'error' ) return response.msg ; // msg será mostrado em formato editável
          vertice = response.vertice
          navigation_tree = response.navigation_tree
          // redesenha grafico de navegação
          create_svg_navigate(navigation_tree)
        }
      })
    }
}
