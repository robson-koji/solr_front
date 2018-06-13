

/*
* Classe para gerar o report aa partir dos facets
*/
function ReportFacets(){
  this.facets = from_ajax['hierarquia']
  this.jsonFacets = {}
}


/*
* Metodo estatico recursivo para navegar no objeto passado.
*/
ReportFacets.prototype.recFacet = function(facets, label, level, send_last, ignore_last, obj_parent){
  var self = this;
  self.label = label

  var label_level = '_nivel_' + level

  // Prepara objeto, junta com o ancestral e grava no json.
  obj = {}
  Object.assign(obj, obj_parent);
  obj[label_level] = facets['label']
  obj['contagem'] = facets['count']
  this.jsonFacets[self.label].push(obj)

  // Prepara o ancestral para enviar para os filhos, em caso de recursao.
  obj_parent_merge = {}
  Object.assign(obj_parent_merge, obj_parent);
  obj_parent_merge[label_level] = facets['label']

  // Se for o ultimo elemento de uma recursao
  // remove o valor do ancestral enviado para os filhos.
  // Decrementa o nivel.
  if (send_last){
    obj_parent_merge[label_level] = '';
    level--;
  }

  // Se objeto tem subnivel, faz verificacoes e chama recursivamente.
  if ('facets' in facets && facets['facets'] ){
    // if (send_last){level--}
    if (Object.keys(facets['facets']).length !== 0 && facets['facets'].constructor === Object){
      // Incrementa o nivel
      level++

      /*
      * Estrutura do facets eh objeto de objetos.
      * Se não for o ultimo elemento de uma recursao, envia aviso para decrementar
      * o nivel que identifica a coluna onde o valor deve ser alocado.
      */
      var keys = Object.keys(facets['facets']);
      var last = keys[keys.length-1];
      var send_last = false;

      for (var key in facets['facets']) {
        if (key === last && key !== ignore_last){
          send_last = true;
        }
        // Chamada recursiva
        self.recFacet(facets['facets'][key], self.label, level, send_last, ignore_last, obj_parent_merge)
      }
    }
  }
}


ReportFacets.makeCsv = function(json){

  // Como as chaves do json variam entre os jsons, cria um objeto com todos as chaves.
  var header_obj = {}
  json.map(function(row){
    var fields = Object.keys(row);
    fields.map(function(fieldName){
      header_obj[fieldName] = '';
    })
  })
  header = Object.keys(header_obj).sort()


  var replacer = function(key, value) { return value === null ? '' : value }
  var csv = json.map(function(row){
    return header.map(function(fieldName){
      return JSON.stringify(row[fieldName], replacer)
    }).join(',')
  })

  csv.unshift(header) // add header column
  csv = csv.join('\r\n')
  return csv
  // debugger;
}



/*
* Metodo de instancia para recuperar o report
*/
ReportFacets.prototype.getReport = function(){
  var csvs = {}
  for (var key in this.facets) {
    var level = 0;

    var label = this.facets[key]['label'];
    this.jsonFacets[label] = []

    // Variavel de controle para a contagem recursiva de niveis.
    var keys = Object.keys( this.facets[key]['facets']);
    var last = keys[keys.length-1];


    this.recFacet( this.facets[key], label, level, false, last, {})

    csvs[label] = ReportFacets.makeCsv(this.jsonFacets[label])

    // console.log(this.jsonFacets[this.facets[key]['label']])
    // debugger;
  }
  return csvs
}


/*
* Funcao utilitaria chamada para gerar o report.
*/
/*
function reportFacets(){
  var report = new ReportFacets()
  csv = report.getReport()
  // console.log(report.jsonFacets)
  // debugger;
}
*/


$(document).ready(function(){


  jQuery("#report_facets").on("click", function () {
      var zip = new JSZip();
      zip.file('LEIAME.TXT', 'Cada arquivo .csv incluido neste arquivo zip se refere a um filtro do buscador.\n'  +
      'Cada arquivo .csv reflete todos os níveis do respectivo filtro. Para a correta utilização dos dados do arquivo .csv, ' +
      'exclua as linhas dos níveis que se sobrepõem para que a contagem não duplique valores.\n' +
      'Os valores apresentados nos arquivos .csv refletem os filtros que foram utilizados na análise. Para ver quais ' +
      'filtros foram aplicados abra o arquivo FILTROS_APLICADOS.TXT') ;

      zip.file('FILTROS_APLICADOS.TXT', 'Mostrar quais filtros foram aplicados, para controle do usuário\n');

      var report = new ReportFacets()
      csvs = report.getReport()
      for (csv in csvs){
        csv_name = csv + '.csv'
        zip.file(csv_name, csvs[csv]);
      }

      zip.generateAsync({type:"blob"}).then(function (blob) { // 1) generate the zip file
          saveAs(blob, "buscador_filtros.zip");                          // 2) trigger the download
      }, function (err) {
          jQuery("#blob").text(err);
      });
  });
})
