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

	$('.ajax-form').each(function() {
		$(this).submit(function() {
			let form = $(this);

			$.ajax({
				url: form.attr('action'),
				method: 'POST',
				data: form.serialize(),
				success: function() {
					window.location.reload();
				},
				complete: function(xhr, msg) {
					form.find('.spinner').css({display: 'none'});
					if (xhr.status != 200) form.find('.login_button span').text(xhr.responseText || msg);
				}
			});

			form.find('.spinner').css({display: 'initial'});

			return false;
		});
	});

	VK.init({apiId: 7980616});

	$('#vk').click(function() {
		VK.Auth.login(function(data) {
			if (!data || !data.session) return;

			$.ajax({
				url: '/oauth/vk',
				method: 'POST',
				data: JSON.stringify(data),
				contentType: 'application/json',
				success: function() {
					window.location.reload();
				},
				complete: function(xhr, msg) {
					$(this).find('.spinner').css({display: 'none'});
					if (xhr.status != 200) $(this).find('span').text(xhr.responseText || msg);
				}
			});

			$(this).find('.spinner').css({display: 'initial'});
		});
	});

	$('#telegram').click(function() {
		window.Telegram.Login.auth({
			bot_id: 2051141677,
			request_access: false,
		}, function(data) {
			if (!data) return;

			$.ajax({
				url: '/oauth/telegram',
				method: 'POST',
				data: JSON.stringify(data),
				contentType: 'application/json',
				success: function() {
					window.location.reload();
				},
				complete: function(xhr, msg) {
					$(this).find('.spinner').css({display: 'none'});
					if (xhr.status != 200) $(this).find('span').text(xhr.responseText || msg);
				}
			});

			$(this).find('.spinner').css({display: 'initial'});
		});
	});
})
