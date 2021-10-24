$(document).ready(function() {
	$('.popup-link').magnificPopup({
		closeOnBgClick: true,
	});

	$('.Ent_hide').click(function() {
		$('.registration_form').addClass('active');
		$('.login_form').addClass('active');
		$('.card').addClass('active');
		$('.menu').slideToggle(300);
	});

	$('.Reg_hide').click(function() {
		$('.registration_form').removeClass('active');
		$('.login_form').removeClass('active');
		$('.card').removeClass('active');
		$('.menu').slideToggle(300);
	});
})
