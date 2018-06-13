/**
* @file
* - Customizacao do Querybuilder
* - Autocomplete
* - Chamada Ajax para o autocomplete
*
* @module solr_front::bv_querybuilder
*/


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
    var sel = document.createElement('select');
    $(sel).change(function(){
      if($(this).find(':selected')){

      }
      $(this).find('option[value="'+this.value+'"]').prop('select', true)
    })

    div.appendChild(sel);
    $(sel).hide();
    divQb.id = id;

    $(id+'_block').trigger('change');
    div.appendChild(divQb);

    $('#querybody').append(div);
    sel.id = id+'_seletor';



    for(var i=0; i < opt.roots.length; i++){
      var option = new Option(opt.roots[i].text,opt.roots[i].value);
      $(sel).append($(option));
    }
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
      $("input[id^='"+id + '_rule_'+key+"']").val('')

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
    var json = {}
    var body = null;
    var body = $('#querybody').find('.bloco');

    $(document).change();
    for(var i = 0; i < body.length; i++){
      var id = '#'+body.eq(i).children().eq(1).attr('id')
      var seletor = body.eq(i).children().eq(0).val();

      json[seletor] =
        {
            'query': $(id).queryBuilder('getRules'),
            'ordem': i,
            'collection':'graph_auxilios',

            //Envia versão filtrada do selectedFacets
            'selected_facets_col1': cleanSelectedFacets(),
            //deixa de usar variavel de estado e usa apenas filtro de função que retorna selectedfacets
            //limpa 'selected_facets_col1':selectedFacets,
            // 'selected_facets_col2':facets_col2
        };
    };
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
      //$(this).val(ui.item.label);
      return false;
    },
    select: function( event, ui ) {
        if (!$('[name="'+id+'"]').tagExist(ui.item.label)) {
           var terms = split( this.value );
           var input_ids = $('[name="'+id+'"]').val();

           if (input_ids.length > 0){
             var ids = split( $('[name="'+id+'"]').val() );
           }else{
             var ids = [];
           }
           // remove the current input
           terms.pop();
           //ids.pop();
           // add the selected item
           terms.push( ui.item.label );
           ids.push(ui.item.value);
           // add placeholder to get the comma-and-space at the end
           terms.push( "" );
           this.value = terms.join( " " );

           //$("#"+id).val(ids.join( ", "));
           //ids.push( "" );

           $('[name="'+id+'"]').addTag(ui.item.label);
           $('[name="'+id+'"]').change();
           return false;
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

        var url = '/pt/buscador/bv/' + bv_collection + '/autocomplete/'

        $.ajax({
          url: url,
          data: {
              q: q,
              fl: fl,
              wt: 'json',
              fq: filtro_chave + ':' + request,
              rows: rows,
              facet:Boolean(facet_field),
              'facet.field': facet_field,
              ac_facet_field:ac_facet_field
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
                response($.map(data.buckets, function( item ) {
                  return {
                      label: item.val,
                      value: item.count,
                  };
                }));
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



function injectAutocompleteTag(id, q, rows, fl, fieldsArray, ac_facet_field){
  if (typeof fq === 'undefined'){
    fq = ''
  }
  if (typeof facet_field === 'undefined'){
    facet_field = ''
  }
  if (typeof ac_facet_field === 'undefined'){
    ac_facet_field = ''
  }

  // Use ("block_string":true) nas opções do tagsInput
  // para bloquear a inserção aleatoria de texto quando utilizar função de autocomplete que não é passada nestas opções
  return   ' <input  type="hidden" id="'+ id +'" name="'+id+'"\/>'+
 '<script> $(function(){ $("[name=\''+id +'\']").tagsInput({"width": "auto","block_string":true,"onRemoveTag": function(){$(this).change();},"defaultText":"Digite um(a) %s para buscar",} ); ajax_solr( "'+id+'" ,"'+q+'",'+rows+',"'+fl+'","'+ fieldsArray[0]+'", "'+fieldsArray[1]+'", "'+fq+'", "'+facet_field+'", "'+ac_facet_field+'"); });<\/script> '
}



/**
* Configurações do plugin queryBuilder para auxilios
* @var {Object}
*/
var graph_auxilios_opt = {
  plugins: ['bt-tooltip-errors'],

  roots: [
    {
      'value':'graph_auxilios',
      'text': 'Auxílio'
    },
    {
      'value': 'graph_auxilios',
      'text': 'Bolsa'
    }
  ],
  filters: [
          {
             id: 'text', // indica o campo a ser buscado  no Solr.
             label: 'Busca textual',
             type: 'string',
             operators: ["contains", "not_contains"],
             input: 'text'
           },
           {
              id: 'numero_processo', // indica o campo a ser buscado  no Solr.
              label: 'Número de processo',
              type: 'string',
              operators: ["equal", "not_equal"],
              input: 'text'
            },
          {
             id: 'area',
             label: 'Area',
             type: 'string',
             operators: ["equal", "not_equal"],
             input: function(rule, name){
               /*
                 Função usada no atributo input dos filtros
                 para criar um campo input com autocomplete.
               */
               var $container = rule.$el.find('.rule-value-container');

               id =  name;
               q = 'django_ct:geral.area_conhecimento';
               fl = "*";
               rows = 20;
               fields = ["areas","areas"];
               return injectAutocompleteTag(id, q, rows, fl, fields, '' );

             },
         },
         {
            id: 'instituicao',
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
              fields = ["instituicao","instituicao"];
              ac_facet_field = "instituicao_exact";
              return injectAutocompleteTag(id, q, rows, fl, fields, ac_facet_field);
            },
        },
      {
         id: 'pesquisadores',
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
           fields = ["nome","nome"];
           return injectAutocompleteTag(id, q, rows, fl, fields, ''  );
         },
     },
     {
       /*
       * Ter um problema de indexacao.
       * O campo a ser buscado nao pode ser string.
       * Utilizando o campo nao string titulo_pt_tooltip, ele nao bate com
       * o que estah indexado no documento de auxilios e/ou bolsas, entao
       * nao acha por convenio.
       */

        id: 'convenio',
        label: 'Convênio',
        operators:["equal", "not_equal", "is_empty", "is_not_empty"],
        input: function(rule, name){
          /*
            Função usada no atributo input dos filtros
            para criar um campo input com autocomplete.
          */
          var $container = rule.$el.find('.rule-value-container');

          id =  name;
          q = 'django_ct:geral.acordo_convenio';
          fl = "*";
          rows = 20;
          fields = ["titulo_pt_tooltip","titulo_pt_tooltip"];
          return injectAutocompleteTag(id, q, rows, fl, fields, '' );
        },
    },
    {
       id: 'pais_convenio',
       label: 'País do convênio',
       operators:["equal", "not_equal", "is_empty", "is_not_empty"],
       input: function(rule, name){
         /*
           Função usada no atributo input dos filtros
           para criar um campo input com autocomplete.
         */
         var $container = rule.$el.find('.rule-value-container');

         id =  name;
         q = 'django_ct:geral.acordo_convenio';
         fl = ","; // Nao precisa dos fields, pq irah utilizar o facet com parametros para o do filtro.
         facet_field = 'pais_exact';
         fq = 'pais'
         rows = 20;
         fields = ["pais_convenio","pais"];
         return injectAutocompleteTag(id, q, rows, fl, fields, fq, facet_field, ''  );
       },
   },
   /*
    {
      id: 'programa',
      label: 'Programa',
      multiple: true,
      input: 'string',
      operators: ["equal", "not_equal", "is_empty", "is_not_empty"],
      input: function(rule, name){
        var $container = rule.$el.find('.rule-value-container');

        id =  name;
        q = 'django_ct:projetos.projeto';
        fl = "*";
        rows = 20;
        fields = ["fomento","fomento"];
        return injectAutocompleteTag(id, q, rows, fl, fields, '' );
        }
      },

      */

      {
        id: 'instituicao_colaboracao',
        label: 'Instituição no exterior/ Outras',
        multiple: true,
        input: 'string',
        operators: ["equal", "not_equal", "is_empty", "is_not_empty"],
        input: function(rule, name){
          var $container = rule.$el.find('.rule-value-container');

          id =  name;
          q = 'django_ct:geral.instituicao_exterior';
          fl = "*";
          rows = 20;
          fields = ["instituicao","instituicao"];
          return injectAutocompleteTag(id, q, rows, fl, fields, ''  );
          }
        },
      {
        id: 'data_inicio_ano',
        label: 'Ano de inicio',
        type: 'integer',
        operators: ["equal","not_equal", "less_or_equal", "greater_or_equal", ],

        plugin: 'bootstrapSlider',
        plugin_config: {
          min: 1989,
          max: 2020,
          value: 2017
        },

        valueSetter: function(rule, value) {

          if (rule.operator.nb_inputs == 1) value = [value];
          rule.$el.find('.rule-value-container input').each(function(i) {
            $(this).bootstrapSlider('setValue', value[i] || 0);

          });
        },
        valueGetter: function(rule) {
          var value = [];
          rule.$el.find('.rule-value-container input').each(function() {
            value.push($(this).bootstrapSlider('getValue'));

          });
          return rule.operator.nb_inputs == 1 ? value[0] : value;
        }
      },
      {
        id: 'data_termino_ano',
        label: 'Ano de termino',
        type: 'integer',
        operators: ["equal", "not_equal", "less_or_equal", "greater_or_equal"],

        plugin: 'bootstrapSlider',
        plugin_config: {
          min: 1989,
          max: 2020,
          value: 2017
        },

        valueSetter: function(rule, value) {

          if (rule.operator.nb_inputs == 1) value = [value];
          rule.$el.find('.rule-value-container input').each(function(i) {
            $(this).bootstrapSlider('setValue', value[i] || 0);

          });
        },
        valueGetter: function(rule) {
          var value = [];
          rule.$el.find('.rule-value-container input').each(function() {
            value.push($(this).bootstrapSlider('getValue'));

          });
          return rule.operator.nb_inputs == 1 ? value[0] : value;
        }
      },
  ]
};




/**
* Configurações do plugin queryBuilder para publicacaoes
* @var {Object}
*/
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
