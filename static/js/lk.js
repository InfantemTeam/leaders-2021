$(document).ready(function() {
	$('#edit_profile_button').click(function() {
		$('#uinfo_display').addClass('hidden');
		$('#uinfo_edit').removeClass('hidden');
		$('#photo_overlay').removeClass('hidden');
		$(this).addClass('hidden');
		$('#save_profile_button').removeClass('hidden');
	});

	$('#save_profile_button').click(function() {
		$('#uinfo_edit').addClass('hidden');
		$('#uinfo_display').removeClass('hidden');
		$('#photo_overlay').addClass('hidden');
		$(this).addClass('hidden');
		$('#edit_profile_button').removeClass('hidden');

		let form = $('form');

		$.ajax({
			url: form.attr('action'),
			method: 'POST',
			data: form.serialize(),
			success: function() {
				window.location.reload();
			},
			complete: function(xhr, msg) {
				if (xhr.status != 200) alert(xhr.responseText || msg);
			}
		});
	});

	$('#uinfo_edit').addClass('hidden');
	$('#save_profile_button').addClass('hidden');
	$('#photo_overlay').addClass('hidden');
});
