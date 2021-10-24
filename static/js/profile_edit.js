function checkParams() {
	let login = $('#login').val(),
	    name = $('#name').val(),
	    surname = $('#surname').val();

	if (login && name && surname) $('#submit').removeAttr('disabled');
	else $('#submit').attr('disabled', 'disabled');
}
