/**
* @file
* - Customizacao do Querybuilder
* - Autocomplete
* - Chamada Ajax para o autocomplete
*
* @module solr_front::bv_querybuilder
*/

/**
* Variavel global que armazena as tags de autocomplete, utilizadas no querybuilder pelo usuário
* @param {Array} selecionados
*/
var selecionados = []

/**
* Gera hmtl do bloco principal do querybuilder
* @param {String} id - Será o id do bloco querybuilder
* @param {Object} opt - Opções de construção
*/
function geraRoot(id, opt, query){

    var div = document.createElement('div');
    div.className += 'bloco';
    div.id = id+'_block';

    var divQb = document.createElement('div');

    divQb.id = id;

    $(id+'_block').trigger('change');
    div.appendChild(divQb);

    $('#querybody').append(div);

    $('#querybody').change();

    opt = reverse_filter( opt, query)

    if (typeof querybuilder_lang != 'undefined'){
      opt['lang'] = querybuilder_lang
    }

    $('#'+id).queryBuilder(opt)



    //executar apos a construção do queryBuilder caso contrario nao ira aparecer as tags
    reverse_tag_input(id, values_tag)

    //desativa a validação do query builder
    $('#'+id).on('validationError.queryBuilder', function(e, rule, error, value){

        e.preventDefault();
        value = "*"
     }
    );
}



function reverse_tag_input(id, tags){
  // deve executar apos a construção do queryBuilder para aparecer

    $.each(tags, function(key,value){
      $("input[id^='"+id + '_rule_'+key+"']").importTags(value);

      // limpa campo de busca que é preenchido pelo jquery taginput com a ultima tag inclusa
      $("input[id^='"+id + '_rule_'+key+"']").removeTag('')

    })





}
/**
* Recupera no Querybuilder os parametros da busca efetuada e monta a visualização.
* Este arquivo Json serah enviado ao servidor, que irah processar e recuperar as informacoes no Solr.
*/
function reverse_filter( opt, query){

  if( typeof query != 'undefined' ){



    if (query[Object.keys(query)[0]].hasOwnProperty('query')){
      query = query[Object.keys(query)[0]].query



    }

    opt_rules = []
    values_tag = {}

    if(query !== null){

      if (query.hasOwnProperty('rules')){

        $.each(query.rules, function(key, rule){
           opt_rules.push(rule)
           values_tag[key] = rule.value
        })
        if(opt_rules){
          for (var i = 0, n=opt_rules.length; i< n; i++){
            valores = opt_rules[i].value.split(',')
            for (var j=0, n2=valores.length; j< n2; j++){
              selecionados.push(valores[j])
            }
          }
          opt['rules'] = opt_rules
        }
      }
    }
    return opt
  }
}
/**
* Recupera no Querybuilder os parametros da busca efetuada e gera um arquivo Json.
* Este arquivo Json serah enviado ao servidor, que irah processar e recuperar as informacoes no Solr.
* @return {JSON}
*/
function getBuscaRealizada(facets_col2){

  if($('#querybody').children().length > 0){
    var json = {}

    json[bv_collection] =
      {
          'query': $('#builder_dinamic').queryBuilder('getRules'),
          'ordem': 0,
          'collection':bv_collection,
          //Envia versão filtrada do selectedFacets
          'selected_facets_col1': cleanSelectedFacets(),
      };

  }
  else{
    var json = {}
    json[bv_collection] =
      {
          'query': null,
          'ordem': 0,
          'collection':bv_collection,
          //Envia versão filtrada do selectedFacets
          'selected_facets_col1': cleanSelectedFacets(),
      };


  }
    return json;
}


/**
* Essa funcao eh chamada pelo autocomplete injetado no querybuilder.
* Responsavel por fazer a chamada ajax no servidor para recuperar os dados do
* autocomplete.
* @param {String} id - identificação do bloco queryBuilder onde será incluido
* @param {String} q - texto digitado
* @param {number} rows - parametro do Solr
* @param {String} fl - parametro do Solr
* @param {string} labelAtribute - campo do label utilizada
* @param {String} valueAtribute - campo do value utilizado
* @param {String} fq - parametro do Solr
* @param {String} facet_field - parametro do Solr
*/
function ajax_solr(id, q, rows, fl, labelAtribute, valueAtribute, fq, facet_field, ac_facet_field) {

  $('[name="'+id+'"]').next('div').find('[id$="_addTag"] input').autocomplete({
    minLength: 0,
    focus: function( event, ui ) {
      return false;
    },
    select: function( event, ui ) {
        if (!$('[name="'+id+'"]').tagExist(ui.item.query)) {
           selecionados.push(ui.item.query)
           $('[name="'+id+'"]').addTag( ui.item.query);
           $('[name="'+id+'"]').change();
           return false;
        }
        else{
          //caso já existir a tag selecionada
          terms [" "]
          return false
        }
    },
    source: function( request, response ) {
        var request = extractLast( request.term ) ;
        if (fq){
          filtro_chave = fq
        }
        else{
          filtro_chave = labelAtribute
        }
        // debugger;

        // var url = window.location.protocol+'//'+window.location.hostname+"/buscador/params/bv/select"

        var url = home_sf_rurl + bv_collection + '/autocomplete/'

        $.ajax({
          url: url,
          type: 'POST',
          data: {
              q: q,
              fl: fl,
              wt: 'json',
              fq: filtro_chave + ':' + "\"" + request + "\"",
              rows: rows,
              facet:Boolean(facet_field),
              'facet.field': facet_field,
              selected_facets : JSON.stringify(query[bv_collection]['selected_facets_col1']),
              csrfmiddlewaretoken: csrf
           },
           // dataType: "jsonp",
           // jsonp: 'json.wrf',

           success: function( data ) {
             /*
             Caso tenha recebido o parametro facet, busca em uma collection os
             itens do facete para apresetnar para a filtragem de projetos
             */

              if ('facet_counts' in data){
                var item = []
                $.each(data.facet_counts.facet_fields[facet_field], function(idx, facet){

                  if (idx % 2 == 0){
                    label = facet //+ ' (' + data.facet_counts.facet_fields[facet_field][idx + 1] + ')'
                    item.push({
                        label: label,
                        value: facet,
                    })
                  }
                })
                response(item);
              }
              else{
                response( $.map(data.buckets, function( item ) {

                  if( $.inArray(item.val, selecionados) == -1 ){

                    if(item.count > 0){

                      return {
                        label: item.val,// +' ('+ item.count +')',
                        query: item.val,
                        value: item.count,
                      };

                    }
                  }
                }).slice(0, rows) );
              }



              /*
              Busca no metodo antigo, diretamente no nginx do servidor.
              else{
                response($.map(data.response.docs, function( item ) {
                  if (Array.isArray(item[labelAtribute])){
                    var label = item[labelAtribute][0];
                  }else{
                    var label = item[labelAtribute];
                  }
                  if (Array.isArray(item[valueAtribute])){
                    var value = item[valueAtribute][0];
                  }else{
                    var value = item[valueAtribute];
                  }
                  return {
                      label: label,
                      value: value,
                  };
                }));
              }
              */

          },
      });
     },
    minLength: 1
    });
}



/**
* Injeta um autocomplete no querybuilder.
* E qdo o usuario comeca a digitar no querybuilder, o autocomplete faz uma chamada ajax no
* servidor utilizando o funcao ajax_solr()
* @param {String} id - identificação do bloco queryBuilder onde será incluido
* @param {String} q - texto digitado
* @param {number} rows - parametro do Solr
* @param {String} fl - parametro do Solr
* @param {Array} fieldsArray - dois campos informados, um sera pesquisado e retornado como value no schema e o outro retornado como key
* @param {String} fq - parametro do Solr
* @param {String} facet_field - parametro do Solr
*
*/



function injectAutocompleteTag(id, q, rows, fl, fieldsArray, fq, facet_field, ac_facet_field){

  // Use ("block_string":true) nas opções do tagsInput
  // para bloquear a inserção aleatoria de texto quando utilizar função de autocomplete que não é passada nestas opções


  return   ' <input  type="hidden" id="'+ id +'" name="'+id+'"\/>'+
 '<script> $(function(){ $("[name=\''+id +'\']").tagsInput({"width": "auto","block_string":true,"delimiter":":::", "onRemoveTag": function(item){ var index = selecionados.indexOf(item);if (index !== -1) selecionados.splice(index, 1);  $(this).change();},"defaultText":"Digite um(a) %s para buscar",} ); ajax_solr( "'+id+'" ,"'+q+'",'+rows+',"'+fl+'","'+ fieldsArray[0]+'", "'+fieldsArray[1]+'", "'+fq+'", "'+facet_field+'", "'+ac_facet_field+'"); });<\/script> '
}



var bv_memoria_opt = {
        roots: [
          {
            'value':'bv_memoria',
            'text': 'Publicações'
          }

        ],
        filters: [
                {
                   id: 'referencia',
                   label: 'Referência',
                   type: 'string',
                   operators: ["equal","not_equal"],
                   input: function(rule, name){
                     /*
                       Função usada no atributo input dos filtros
                       para criar um campo input com autocomplete.
                     */
                     var $container = rule.$el.find('.rule-value-container');

                     id =  name;
                     q = 'django_ct:memoria.serie_periodica';
                     fl = "*";
                     rows = 20;
                     fields = ["referencia","referencia"];
                     return injectAutocompleteTag(id, q, rows, fl, fields, ''  );
                   },
               },
               {
                  id: 'descricao',
                  label: 'Descrição',
                  multiple: true,
                  input: 'string',
                  operators: ["equal","not_equal"],
                  input: function(rule, name){
                    /*
                      Função usada no atributo input dos filtros
                      para criar um campo input com autocomplete.
                    */
                    var $container = rule.$el.find('.rule-value-container');

                    id =  name;
                    q = 'django_ct:memoria.serie_periodica';
                    fl = "*";
                    rows = 20;
                    fields = ["descricao","descricao"];
                    return injectAutocompleteTag(id, q, rows, fl, fields, ''  );
                  },
              },
              {
                 id: 'revista_text',
                 label: 'Revista',
                 multiple: true,
                 input: 'string',
                 operators: ["equal","not_equal"],
                 input: function(rule, name){
                   /*
                     Função usada no atributo input dos filtros
                     para criar um campo input com autocomplete.
                   */
                   var $container = rule.$el.find('.rule-value-container');

                   id =  name;
                   q = 'django_ct:memoria.serie_periodica';
                   fl = "*";
                   rows = 20;
                   fields = ["revista_text","revista_text"];
                   return injectAutocompleteTag(id, q, rows, fl, fields, ''  );
                 },
             },
             {
               id: 'ano_publicacao',
               label: 'Ano de publicação',
               type: 'integer',
               operators: ["equal","not_equal", "less_or_equal", "greater_or_equal", ],

               plugin: 'bootstrapSlider',
               plugin_config: {
                 min: 1989,
                 max: 2020,
                 value: 2017
               },
             }
          ]
};


var memoria_autoria_opt = {
        roots: [
          {
            'value':'memoria_autoria',
            'text': 'Autores e instituições das publicações'
          }

        ],
        filters: [
                {
                   id: 'instituicao_list',
                   label: 'Instituição',
                   type: 'string',
                   operators: ["equal","not_equal"],
                   input: function(rule, name){
                     /*
                       Função usada no atributo input dos filtros
                       para criar um campo input com autocomplete.
                     */
                     var $container = rule.$el.find('.rule-value-container');

                     id =  name;
                     q = 'django_ct:bv_memoria';
                     fl = "*";
                     rows = 20;
                     fields = ["instituicao_list","instituicao_list"];
                     return injectAutocompleteTag(id, q, rows, fl, fields, ''  );
                   },
               },
               {
                  id: 'pais_list',
                  label: 'Pais',
                  multiple: true,
                  input: 'string',
                  operators: ["equal","not_equal"],
                  input: function(rule, name){
                    /*
                      Função usada no atributo input dos filtros
                      para criar um campo input com autocomplete.
                    */
                    var $container = rule.$el.find('.rule-value-container');

                    id =  name;
                    q = 'django_ct:bv_memoria';
                    fl = "*";
                    rows = 20;
                    fields = ["pais_list","pais_list"];
                    return injectAutocompleteTag(id, q, rows, fl, fields, ''  );
                  },
              },

          ]
};



var pesquisa_pipe_opt = {
        roots: [
          {
            'value':'pesquisa_pipe',
            'text': 'Pesquisa PIPE 2017'
          }

        ],
        filters: [
                {
                   id: 'razao_social_atual',
                   label: 'Razão Social',
                   type: 'string',
                   operators: ["equal","not_equal"],
                   input: function(rule, name){
                     /*
                       Função usada no atributo input dos filtros
                       para criar um campo input com autocomplete.
                     */
                     var $container = rule.$el.find('.rule-value-container');

                     id =  name;
                     q = 'django_ct:bv_memoria';
                     fl = "*";
                     rows = 20;
                     fields = ["instituicao_list","instituicao_list"];
                     return injectAutocompleteTag(id, q, rows, fl, fields, ''  );
                   },
               },


          ]
};


var inep_docentes_opt = {
        roots: [
          {
            'value':'inep_docentes',
            'text': 'Docentes INEP'
          }

        ],
        filters: [
                {
                   id: 'no_ies',
                   label: 'Instituicao',
                   type: 'string',
                   operators: ["equal","not_equal"],
                   input: function(rule, name){
                     /*
                       Função usada no atributo input dos filtros
                       para criar um campo input com autocomplete.
                     */
                     var $container = rule.$el.find('.rule-value-container');

                     id =  name;
                     q = 'django_ct:bv_memoria';
                     fl = "*";
                     rows = 20;
                     fields = ["NO_IES","NO_IES"];
                     return injectAutocompleteTag(id, q, rows, fl, fields, ''  );
                   },
               },
               {
                  id: 'co_docente',
                  label: 'Código do docente',
                  type: 'string',
                  operators: ["equal","not_equal"],
                  input: function(rule, name){
                    /*
                      Função usada no atributo input dos filtros
                      para criar um campo input com autocomplete.
                    */
                    var $container = rule.$el.find('.rule-value-container');

                    id =  name;
                    q = 'django_ct:bv_memoria';
                    fl = "*";
                    rows = 20;
                    fields = ["CO_DOCENTE","CO_DOCENTE"];
                    return injectAutocompleteTag(id, q, rows, fl, fields, ''  );
                  },
              },


          ]
};




var inep_alunos_opt = {
        roots: [
          {
            'value':'inep_alunos',
            'text': 'Alunos INEP'
          }

        ],
        filters: [

               {
                  id: 'co_aluno',
                  label: 'Código do aluno',
                  type: 'string',
                  operators: ["equal","not_equal"],
                  input: function(rule, name){
                    /*
                      Função usada no atributo input dos filtros
                      para criar um campo input com autocomplete.
                    */
                    var $container = rule.$el.find('.rule-value-container');

                    id =  name;
                    q = 'django_ct:bv_memoria';
                    fl = "*";
                    rows = 20;
                    fields = ["CO_ALUNO","CO_ALUNO"];
                    return injectAutocompleteTag(id, q, rows, fl, fields, ''  );
                  },
              },


          ]
};



var fazenda_sp_opt = {
        roots: [{
            'value':'fazenda_sp',
            'text': 'Alunos INEP'
          }],
        filters: [
               {
                  id: 'co_aluno',
                  label: 'Código do aluno',
                  type: 'string',
                  operators: ["equal","not_equal"],
                  input: function(rule, name){
                    /*
                      Função usada no atributo input dos filtros
                      para criar um campo input com autocomplete.
                    */
                    var $container = rule.$el.find('.rule-value-container');

                    id =  name;
                    q = 'django_ct:bv_memoria';
                    fl = "*";
                    rows = 20;
                    fields = ["CO_ALUNO","CO_ALUNO"];
                    return injectAutocompleteTag(id, q, rows, fl, fields, '' );
                  },
              },
          ]
};


var lattes_opt = {
        roots: [{
            'value':'lattes',
            'text': 'CV Lattes'
          }],
        filters: [
               {
                  id: 'ATIVIDADES-DE-ENSINO_DISCIPLINAS',
                  label: 'ATIVIDADES-DE-ENSINO_DISCIPLINAS',
                  type: 'string',
                  operators: ["equal","not_equal"],
                  input: function(rule, name){
                    /*
                      Função usada no atributo input dos filtros
                      para criar um campo input com autocomplete.
                    */
                    var $container = rule.$el.find('.rule-value-container');

                    id =  name;
                    q = 'django_ct:bv_memoria';
                    fl = "*";
                    rows = 20;
                    fields = ["ATIVIDADES-DE-ENSINO_DISCIPLINAS_busca","ATIVIDADES-DE-ENSINO_DISCIPLINAS_busca"];
                    ac_facet_field = "ATIVIDADES-DE-ENSINO_DISCIPLINAS";
                    return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                  },
              },

              {
                 id: 'GRADUACAO_NOME-AGENCIA',
                 label: 'GRADUACAO_NOME-AGENCIA',
                 type: 'string',
                 operators: ["equal","not_equal"],
                 input: function(rule, name){
                   var $container = rule.$el.find('.rule-value-container');
                   id =  name; q = 'django_ct:bv_memoria'; fl = "*"; rows = 20;

                   fields = ["GRADUACAO_NOME-AGENCIA_busca","GRADUACAO_NOME-AGENCIA_busca"];
                   ac_facet_field = "GRADUACAO_NOME-AGENCIA";
                   return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                 },
             },
             {
                id: 'GRADUACAO_NOME-INSTITUICAO',
                label: 'GRADUACAO_NOME-INSTITUICAO',
                type: 'string',
                operators: ["equal","not_equal"],
                input: function(rule, name){
                  var $container = rule.$el.find('.rule-value-container');
                  id =  name; q = 'django_ct:bv_memoria'; fl = "*"; rows = 20;

                  fields = ["GRADUACAO_NOME-INSTITUICAO_busca","GRADUACAO_NOME-INSTITUICAO_busca"];
                  ac_facet_field = "GRADUACAO_NOME-INSTITUICAO";
                  return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                },
            },

                    {
                       id: 'ESPECIALIZACAO_NOME-AGENCIA',
                       label: 'ESPECIALIZACAO_NOME-AGENCIA',
                       type: 'string',
                       operators: ["equal","not_equal"],
                       input: function(rule, name){
                         var $container = rule.$el.find('.rule-value-container');
                         id =  name; q = 'django_ct:bv_memoria'; fl = "*"; rows = 20;

                         fields = ["ESPECIALIZACAO_NOME-AGENCIA_busca","ESPECIALIZACAO_NOME-AGENCIA_busca"];
                         ac_facet_field = "ESPECIALIZACAO_NOME-AGENCIA";
                         return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                       },
                   },
                   {
                      id: 'ESPECIALIZACAO_NOME-INSTITUICAO',
                      label: 'ESPECIALIZACAO_NOME-INSTITUICAO',
                      type: 'string',
                      operators: ["equal","not_equal"],
                      input: function(rule, name){
                        var $container = rule.$el.find('.rule-value-container');
                        id =  name; q = 'django_ct:bv_memoria'; fl = "*"; rows = 20;

                        fields = ["ESPECIALIZACAO_NOME-INSTITUICAO_busca","ESPECIALIZACAO_NOME-INSTITUICAO_busca"];
                        ac_facet_field = "ESPECIALIZACAO_NOME-INSTITUICAO";
                        return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                      },
                  },
                  {
                     id: 'MESTRADO_NOME-AGENCIA',
                     label: 'MESTRADO_NOME-AGENCIA',
                     type: 'string',
                     operators: ["equal","not_equal"],
                     input: function(rule, name){
                       var $container = rule.$el.find('.rule-value-container');
                       id =  name; q = 'django_ct:bv_memoria'; fl = "*"; rows = 20;

                       fields = ["MESTRADO_NOME-AGENCIA_busca","MESTRADO_NOME-AGENCIA_busca"];
                       ac_facet_field = "MESTRADO_NOME-AGENCIA";
                       return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                     },
                 },
                 {
                    id: 'MESTRADO_NOME-INSTITUICAO',
                    label: 'MESTRADO_NOME-INSTITUICAO',
                    type: 'string',
                    operators: ["equal","not_equal"],
                    input: function(rule, name){
                      var $container = rule.$el.find('.rule-value-container');
                      id =  name; q = 'django_ct:bv_memoria'; fl = "*"; rows = 20;

                      fields = ["MESTRADO_NOME-INSTITUICAO_busca","MESTRADO_NOME-INSTITUICAO_busca"];
                      ac_facet_field = "MESTRADO_NOME-INSTITUICAO";
                      return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                    },
                },
                {
                   id: 'MESTRADO_ESPECIALIDADE',
                   label: 'MESTRADO_ESPECIALIDADE',
                   type: 'string',
                   operators: ["equal","not_equal"],
                   input: function(rule, name){
                     var $container = rule.$el.find('.rule-value-container');
                     id =  name; q = 'django_ct:bv_memoria'; fl = "*"; rows = 20;

                     fields = ["MESTRADO_ESPECIALIDADE_busca","MESTRADO_ESPECIALIDADE_busca"];
                     ac_facet_field = "MESTRADO_ESPECIALIDADE";
                     return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                   },
               },
              {
                 id: 'MESTRADO_PALAVRA-CHAVE',
                 label: 'MESTRADO_PALAVRA-CHAVE',
                 type: 'string',
                 operators: ["equal","not_equal"],
                 input: function(rule, name){
                   /*
                     Função usada no atributo input dos filtros
                     para criar um campo input com autocomplete.
                   */
                   var $container = rule.$el.find('.rule-value-container');

                   id =  name;
                   q = 'django_ct:bv_memoria';
                   fl = "*";
                   rows = 20;
                   fields = ["MESTRADO_PALAVRA-CHAVE_busca","MESTRADO_PALAVRA-CHAVE_busca"];
                   ac_facet_field = "MESTRADO_PALAVRA-CHAVE";
                   return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                 },
             },
             {
                id: 'DOUTORADO_PALAVRA-CHAVE',
                label: 'DOUTORADO_PALAVRA-CHAVE',
                type: 'string',
                operators: ["equal","not_equal"],
                input: function(rule, name){
                  /*
                    Função usada no atributo input dos filtros
                    para criar um campo input com autocomplete.
                  */
                  var $container = rule.$el.find('.rule-value-container');

                  id =  name;
                  q = 'django_ct:bv_memoria';
                  fl = "*";
                  rows = 20;
                  fields = ["DOUTORADO_PALAVRA-CHAVE_busca","DOUTORADO_PALAVRA-CHAVE_busca"];
                  ac_facet_field = "DOUTORADO_PALAVRA-CHAVE";
                  return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                },
            },
            {
               id: 'DOUTORADO_NOME-AGENCIA',
               label: 'DOUTORADO_NOME-AGENCIA',
               type: 'string',
               operators: ["equal","not_equal"],
               input: function(rule, name){
                 var $container = rule.$el.find('.rule-value-container');
                 id =  name; q = 'django_ct:bv_memoria'; fl = "*"; rows = 20;

                 fields = ["DOUTORADO_NOME-AGENCIA_busca","DOUTORADO_NOME-AGENCIA_busca"];
                 ac_facet_field = "DOUTORADO_NOME-AGENCIA";
                 return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
               },
           },
           {
              id: 'DOUTORADO_NOME-INSTITUICAO',
              label: 'DOUTORADO_NOME-INSTITUICAO',
              type: 'string',
              operators: ["equal","not_equal"],
              input: function(rule, name){
                var $container = rule.$el.find('.rule-value-container');
                id =  name; q = 'django_ct:bv_memoria'; fl = "*"; rows = 20;

                fields = ["DOUTORADO_NOME-INSTITUICAO_busca","DOUTORADO_NOME-INSTITUICAO_busca"];
                ac_facet_field = "DOUTORADO_NOME-INSTITUICAO";
                return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
              },
          },



                  {
                     id: 'DOUTORADO_ESPECIALIDADE',
                     label: 'DOUTORADO_ESPECIALIDADE',
                     type: 'string',
                     operators: ["equal","not_equal"],
                     input: function(rule, name){
                       var $container = rule.$el.find('.rule-value-container');
                       id =  name; q = 'django_ct:bv_memoria'; fl = "*"; rows = 20;

                       fields = ["DOUTORADO_ESPECIALIDADE_busca","DOUTORADO_ESPECIALIDADE_busca"];
                       ac_facet_field = "DOUTORADO_ESPECIALIDADE";
                       return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                     },
                 },
            {
               id: 'POS-DOUTORADO_PALAVRA-CHAVE',
               label: 'POS-DOUTORADO_PALAVRA-CHAVE',
               type: 'string',
               operators: ["equal","not_equal"],
               input: function(rule, name){
                 /*
                   Função usada no atributo input dos filtros
                   para criar um campo input com autocomplete.
                 */
                 var $container = rule.$el.find('.rule-value-container');

                 id =  name;
                 q = 'django_ct:bv_memoria';
                 fl = "*";
                 rows = 20;
                 fields = ["POS-DOUTORADO_PALAVRA-CHAVE_busca","POS-DOUTORADO_PALAVRA-CHAVE_busca"];
                 ac_facet_field = "POS-DOUTORADO_PALAVRA-CHAVE";
                 return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
               },
           },
          {
             id: 'POS-DOUTORADO_NOME-AGENCIA	',
             label: 'POS-DOUTORADO_NOME-AGENCIA	',
             type: 'string',
             operators: ["equal","not_equal"],
             input: function(rule, name){
               /*
                 Função usada no atributo input dos filtros
                 para criar um campo input com autocomplete.
               */
               var $container = rule.$el.find('.rule-value-container');

               id =  name;
               q = 'django_ct:bv_memoria';
               fl = "*";
               rows = 20;
               fields = ["POS-DOUTORADO_NOME-AGENCIA	_busca","POS-DOUTORADO_NOME-AGENCIA	_busca"];
               ac_facet_field = "POS-DOUTORADO_NOME-AGENCIA	";
               return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
             },
         },

         {
            id: 'POS-DOUTORADO_NOME-INSTITUICAO	',
            label: 'POS-DOUTORADO_NOME-INSTITUICAO	',
            type: 'string',
            operators: ["equal","not_equal"],
            input: function(rule, name){
              /*
                Função usada no atributo input dos filtros
                para criar um campo input com autocomplete.
              */
              var $container = rule.$el.find('.rule-value-container');

              id =  name;
              q = 'django_ct:bv_memoria';
              fl = "*";
              rows = 20;
              fields = ["POS-DOUTORADO_NOME-INSTITUICAO	_busca","POS-DOUTORADO_NOME-INSTITUICAO	_busca"];
              ac_facet_field = "POS-DOUTORADO_NOME-INSTITUICAO	";
              return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
            },
        },
        {
           id: 'POS-DOUTORADO_ESPECIALIDADE	',
           label: 'POS-DOUTORADO_ESPECIALIDADE	',
           type: 'string',
           operators: ["equal","not_equal"],
           input: function(rule, name){
             /*
               Função usada no atributo input dos filtros
               para criar um campo input com autocomplete.
             */
             var $container = rule.$el.find('.rule-value-container');

             id =  name;
             q = 'django_ct:bv_memoria';
             fl = "*";
             rows = 20;
             fields = ["POS-DOUTORADO_ESPECIALIDADE	_busca","POS-DOUTORADO_ESPECIALIDADE	_busca"];
             ac_facet_field = "POS-DOUTORADO_ESPECIALIDADE	";
             return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
           },
       },




        ]
};

var rais_opt = {
        roots: [{
            'value':'rais',
            'text': 'RAIS'
          }],
        filters: [
               {
                  id: 'co_aluno',
                  label: 'Código do aluno',
                  type: 'string',
                  operators: ["equal","not_equal"],
                  input: function(rule, name){
                    /*
                      Função usada no atributo input dos filtros
                      para criar um campo input com autocomplete.
                    */
                    var $container = rule.$el.find('.rule-value-container');

                    id =  name;
                    q = 'django_ct:bv_memoria';
                    fl = "*";
                    rows = 20;
                    fields = ["CO_ALUNO","CO_ALUNO"];
                    return injectAutocompleteTag(id, q, rows, fl, fields, '' );
                  },
              },
          ]
};



var wos_opt = {
        roots: [{
            'value':'wos',
            'text': 'Web of Sciece'
          }],
            filters: [
              {
                 id: 'ATIVIDADES-DE-ENSINO_DISCIPLINAS',
                 label: 'ATIVIDADES-DE-ENSINO_DISCIPLINAS',
                 type: 'string',
                 operators: ["equal","not_equal"],
                 input: function(rule, name){
                   /*
                     Função usada no atributo input dos filtros
                     para criar um campo input com autocomplete.
                   */
                   var $container = rule.$el.find('.rule-value-container');

                   id =  name;
                   q = 'django_ct:bv_memoria';
                   fl = "*";
                   rows = 20;
                   fields = ["ATIVIDADES-DE-ENSINO_DISCIPLINAS_busca","ATIVIDADES-DE-ENSINO_DISCIPLINAS_busca"];
                   ac_facet_field = "ATIVIDADES-DE-ENSINO_DISCIPLINAS";
                   return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                 },
             },


           ]
};




var enade_opt = {
        roots: [{
            'value':'enade',
            'text': 'ENADE'
          }],
            filters: [
              {
                 id: 'ATIVIDADES-DE-ENSINO_DISCIPLINAS',
                 label: 'ATIVIDADES-DE-ENSINO_DISCIPLINAS',
                 type: 'string',
                 operators: ["equal","not_equal"],
                 input: function(rule, name){
                   /*
                     Função usada no atributo input dos filtros
                     para criar um campo input com autocomplete.
                   */
                   var $container = rule.$el.find('.rule-value-container');

                   id =  name;
                   q = 'django_ct:bv_memoria';
                   fl = "*";
                   rows = 20;
                   fields = ["ATIVIDADES-DE-ENSINO_DISCIPLINAS_busca","ATIVIDADES-DE-ENSINO_DISCIPLINAS_busca"];
                   ac_facet_field = "ATIVIDADES-DE-ENSINO_DISCIPLINAS";
                   return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
                 },
             },


           ]
};




var bv_empresas_opt = {
        roots: [
          {
            'value':'bv_empresas',
            'text': 'Empresas do PIPE'
          }

        ],
        filters: [
                {
                   id: 'razao_social',
                   label: 'Razão Social',
                   type: 'string',
                   operators: ["equal","not_equal"],
                   input: function(rule, name){
                     /*
                       Função usada no atributo input dos filtros
                       para criar um campo input com autocomplete.
                     */
                     var $container = rule.$el.find('.rule-value-container');

                     id =  name;
                     q = 'django_ct:empresas.empresa';
                     fl = "*";
                     rows = 20;
                     fields = ["razao_social","razao_social"];
                     return injectAutocompleteTag(id, q, rows, fl, fields, '' );
                   },
               },
               {
                  id: 'municipio_cpd',
                  label: 'Município',
                  multiple: true,
                  input: 'string',
                  operators: ["equal","not_equal"],
                  input: function(rule, name){
                    /*
                      Função usada no atributo input dos filtros
                      para criar um campo input com autocomplete.
                    */
                    var $container = rule.$el.find('.rule-value-container');

                    id =  name;
                    q = 'django_ct:empresas.empresa';
                    fl = "*";
                    rows = 20;
                    fields = ["municipio_cpd","municipio_cpd"];
                    return injectAutocompleteTag(id, q, rows, fl, fields, '' );
                  },
              },

             {
               id: 'ano_primeiro_processo',
               label: 'Ano do primeiro processo no programa PIPE',
               type: 'integer',
               operators: ["equal","not_equal", "less_or_equal", "greater_or_equal", ],

               plugin: 'bootstrapSlider',
               plugin_config: {
                 min: 1989,
                 max: 2020,
                 value: 2017
               },
             }
          ]
};




var bv_pesquisadores_opt = {
        roots: [
          {
            'value':'bv_pesquisadores',
            'text': 'Pesquisadores FAPESP'
          }

        ],
        filters: [
                {
                  id: 'nome_tooltip',
                  label: 'Pesquisador',
                  multiple: true,
                  input: 'string',
                  operators: ["equal", "not_equal"],
                  input: function(rule, name){
                    /*
                      Função usada no atributo input dos filtros
                      para criar um campo input com autocomplete.
                    */
                    var $container = rule.$el.find('.rule-value-container');

                    id =  name;
                    q = 'django_ct:geral.pesquisador';
                    fl = "*";
                    rows = 20;
                    fields = ["nome_tooltip","nome_tooltip"];
                    return injectAutocompleteTag(id, q, rows, fl, fields, '' );
                  },
               },
              {
                 id: 'instituicao_afiliacao',
                 label: 'Instituição',
                 multiple: true,
                 input: 'string',
                 operators: ["equal", "not_equal"],
                 input: function(rule, name){
                   /*
                     Função usada no atributo input dos filtros
                     para criar um campo input com autocomplete.
                   */
                   var $container = rule.$el.find('.rule-value-container');

                   id =  name;
                   q = 'django_ct:geral.instituicao_sede';
                   fl = "*";
                   rows = 20;
                   fields = ["nome","nome"];
                   return injectAutocompleteTag(id, q, rows, fl, fields, '' );
                 },
             },

          ]
};



/**
* Configurações do plugin queryBuilder para instituição sede
* @var {Object}
*/
var instituicao_sede_opt = {
        roots: [
          {
            'value':'geral.instituicao_sede',
            'text': 'Instituição'
          }

        ],
        filters: [
                {
                   id: 'nome',
                   label: 'Nome',
                   type: 'string',
                   operators: ["equal","not_equal"],
                   input: function(rule, name){
                     /*
                       Função usada no atributo input dos filtros
                       para criar um campo input com autocomplete.
                     */
                     var $container = rule.$el.find('.rule-value-container');

                     id =  name;
                     q = 'django_ct:geral.instituicao_sede';
                     fl = "*";
                     rows = 20;
                     fields = ["nome","nome"];
                     return injectAutocompleteTag(id, q, rows, fl, fields, '' );
                   },
               },
               {
                  id: 'tipo',
                  label: 'Tipo',
                  multiple: true,
                  input: 'string',
                  operators: ["equal","not_equal"],
                  input: function(rule, name){
                    /*
                      Função usada no atributo input dos filtros
                      para criar um campo input com autocomplete.
                    */
                    var $container = rule.$el.find('.rule-value-container');

                    id =  name;
                    q = 'django_ct:geral.instituicao_sede';
                    fl = "*";
                    rows = 20;
                    fields = ["tipo","tipo"];
                    return injectAutocompleteTag(id, q, rows, fl, fields, '' );
                  },
              },
              {
                 id: 'super_pai_id',
                 label: 'Instituição Pai po ID',
                 operators:["is_empty", "is_not_empty"],
                 type: 'integer'
             },
             {
                id: 'numeros_patentes',
                label: 'Numero de patentes',
                type: 'double',
                validation: {
                  min: 0,
                  step: 0.01
                },
                operators: ["equal","is_empty", "is_not_empty"]
            },
        ]
};


FILTER_FUNCTIONS = {
  "text": "text",
  "autocomplete": function(rule, name){
    /*
      Função usada no atributo input dos filtros
      para criar um campo input com autocomplete.
    */
    var solr_params = rule.__.filter.solr_params

    id =  name;
    q = solr_params.q || '';
    fl = solr_params.fl || '*';
    fq = solr_params.fq || '';
    rows = solr_params.rows || 10;
    fields = [solr_params.field,solr_params.field];
    facet_field = solr_params.facet_field || '';
    ac_facet_field = facet_field;
    return injectAutocompleteTag(id, q, rows, fl, fields, fq, facet_field, ac_facet_field );

  },

}

function generate_options(list_filters_config){

  opt = {}
  if(Object.keys(list_filters_config).length){
    opt['filters'] = []

    opt['plugins'] = list_filters_config['plugins']

    for( var i =0, n = list_filters_config['filters'].length; i<n; i++ ){
      obj = {}
      $.each(list_filters_config['filters'][i], function(key, value){
        if(key == 'input'){
          obj[key] = FILTER_FUNCTIONS[value]
        }
        else if(key == 'get_from_solr_field'){
          obj['id'] = value
        }
        else if(key == 'plugin' && value == 'slider'){

          obj['plugin'] = 'bootstrapSlider'

          obj['valueSetter'] = function(rule, value) {

            if (rule.operator.nb_inputs == 1) value = [value];
            rule.$el.find('.rule-value-container input').each(function(i) {
              $(this).bootstrapSlider('setValue', value[i] || 0);

            });
          }
          obj['valueGetter'] = function(rule) {
              var value = [];
              rule.$el.find('.rule-value-container input').each(function() {
                value.push($(this).bootstrapSlider('getValue'));

            });
            return rule.operator.nb_inputs == 1 ? value[0] : value;
          }
        }
        else{
          obj[key] = value

        }

      });

      opt['filters'].push(obj)
    }
  }
  return opt
}
