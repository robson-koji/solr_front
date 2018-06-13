function error_409_getdata(data, url_back){

  $('#alert_screen').show()
  var btn_back = '<a href=' + url_back + ' class="btn btn-primary" role="button" style="margin: 30px;">Voltar</a>'
  var btn_home = '<a href="/pt/buscador/bv/" class="btn btn-warning" role="button">Iniciar nova navegação</a>'
  var alert_navigation = '<div class="alert alert-warning">' +
  data['message'] + btn_back + btn_home + '</div>'

  $('#alert_screen_div_id').html(alert_navigation)

}
