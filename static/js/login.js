$(document).ready(function() {
	$('#vk').magnificPopup({
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

	$('#telegram').click(tgAuth);
})

function tgAuth() {
	window.Telegram.Login.auth({
		bot_id: '2051141677',
		request_access: true,
	}, function(data) {
		if (!data) {
			// authorization failed
		}

		// Here you would want to validate data like described there https://core.telegram.org/widgets/login#checking-authorization
		alert(data);
	});
}
