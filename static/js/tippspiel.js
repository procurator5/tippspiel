$('#btn-menu').bind('click', function() {
	  alert( 'Клик!' );
  $(this).prop("html").attr('data-sidebar', 'visible');
});
