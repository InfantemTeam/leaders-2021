function checkParams() {
    var login = $('#login').val();
    var password = $('#password').val();

    if(login.length != 0 && password.length != 0) {
        $('#submit').removeAttr('disabled');
    } else {
        $('#submit').attr('disabled', 'disabled');
    }
}
