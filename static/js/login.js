$(document).ready(function() {
	$('#show_reg').click(function() {
		$('#login_form').addClass('hidden');
		$('#register_form').removeClass('hidden');
		$('#register_link').addClass('hidden');
		$('#login_link').removeClass('hidden');
		$('.card').addClass('active');
	});

	$('#hide_reg').click(function() {
		$('#register_form').addClass('hidden');
		$('#login_form').removeClass('hidden');
		$('#login_link').addClass('hidden');
		$('#register_link').removeClass('hidden');
		$('.card').removeClass('active');
	});

	$('#register_form').addClass('hidden');
	$('#login_link').addClass('hidden');

	$('.submit').click(function() {
		let form = this.parent('form');

		$.ajax({
			url: form.attr('action'),
			method: 'POST',
			data: form.serialize(),
			success: function() {
				window.location = '/';
			},
			complete: function(xhr, msg) {
				if (xhr.status != 200) alert(msg);
			}
		});
	});

	VK.init({apiId: 7980616});

	$('#vk').click(function() {
		VK.Auth.login(function(data) {
			$.ajax({
				url: '/oauth/vk',
				method: 'POST',
				data: JSON.stringify(data),
				contentType: 'application/json',
				success: function() {
					window.location = '/';
				},
				complete: function(xhr, msg) {
					if (xhr.status != 200) alert(msg);
				}
			});
		});
	});

	$('#telegram').click(function() {
		window.Telegram.Login.auth({
			bot_id: 2051141677,
			request_access: false,
		}, function(data) {
			$.ajax({
				url: '/oauth/telegram',
				method: 'POST',
				data: JSON.stringify(data),
				contentType: 'application/json',
				success: function() {
					window.location = '/';
				},
				complete: function(xhr, msg) {
					if (xhr.status != 200) alert(msg);
				}
			});
		});
	});
})
