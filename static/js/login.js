$(document).ready(function() {
	/*$('#vk').magnificPopup({
		closeOnBgClick: true,
	});*/

	$('.show_reg').click(function() {
		$('.registration_form').addClass('active');
		$('.login_form').addClass('active');
		$('.card').addClass('active');
		$('.menu').slideToggle(300);
	});

	$('.hide_reg').click(function() {
		$('.registration_form').removeClass('active');
		$('.login_form').removeClass('active');
		$('.card').removeClass('active');
		$('.menu').slideToggle(300);
	});

	VK.init({apiId: 7980616});

	$('#vk').click(function() {
		VK.Auth.login(function(data) {
			console.log(data);
		});
	});

	$('#telegram').click(function() {
		window.Telegram.Login.auth({
			bot_id: 2051141677,
			request_access: true,
		}, function(data) {
			if (!data) {
				// authorization failed
			}

			// Here you would want to validate data like described there https://core.telegram.org/widgets/login#checking-authorization
			console.log(data);
		});
	});
})
