function checkParams() {
    var login = $('#login').val();
    var password = $('#password').val();
    var name = $('#name').val();
    var surname = $('#surname').val();
    var date = $('#date').val();
     
    if(login.length != 0 && password.length != 0 && date.length != 0 && name.length != 0 && surname.length != 0) {
        $('#submit').removeAttr('disabled');
    } else {
        $('#submit').attr('disabled', 'disabled');
    }
}
