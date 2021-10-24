$(document).ready(function() {
	$('.menuToggle').click(function() {
		$(this).toggleClass('active');
		$('.border_menu').toggleClass('active');
		$('.background_click').toggleClass('active');
		$('.menu').slideToggle(300);
	});
});
