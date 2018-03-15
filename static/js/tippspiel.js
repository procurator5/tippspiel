$(document).ready(function () {

	$('#btn-login').bind('click', function() {
		$('#loginPopup').attr('style', 'display: block;');
	});

	$('#btn-close').bind('click', function() {
		$('#loginPopup').attr('style', 'display: none;');
	});

});