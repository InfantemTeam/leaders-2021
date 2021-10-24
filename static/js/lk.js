$(document).ready(function() {
	$('#edit_profile_button').click(function() {
		$('#uinfo_display').addClass('hidden');
		$('#uinfo_edit').removeClass('hidden');
		$(this).addClass('hidden');
		$('#save_profile_button').addClass('hidden');
	});

	$('#uinfo_edit').addClass('hidden');
	$('#save_profile_button').addClass('hidden');
});
