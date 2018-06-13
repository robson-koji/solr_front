$(".modal").each(function(index) {
$(this).on('show.bs.modal', function(e) {
  var open = $(this).attr('data-easein');
  if (open == 'shake') {
    $('.modal-dialog').velocity('callout.' + open);
  } else if (open == 'pulse') {
    $('.modal-dialog').velocity('callout.' + open);
  } else if (open == 'tada') {
    $('.modal-dialog').velocity('callout.' + open);
  } else if (open == 'flash') {
    $('.modal-dialog').velocity('callout.' + open);
  } else if (open == 'bounce') {
    $('.modal-dialog').velocity('callout.' + open);
  } else if (open == 'swing') {
    $('.modal-dialog').velocity('callout.' + open);
  } else {
    $('.modal-dialog').velocity('transition.' + open);
  }

});
});
