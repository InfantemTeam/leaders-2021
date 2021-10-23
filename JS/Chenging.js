function checkParams() {
    var login = $('#login').val();
    var name = $('#name').val();
    var surname = $('#surname').val();
     
    if(login.length != 0 && name.length != 0 && surname.length != 0) {
        $('#submit').removeAttr('disabled');
    } else {
        $('#submit').attr('disabled', 'disabled');
    }
}