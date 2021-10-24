$(document).ready(function() {
	$('.menuToggle').click(function() {
		$(this).toggleClass('active');
		$('.border_menu').toggleClass('active');
		$('.menu').slideToggle(300, function() {
			
		});
	});
});
