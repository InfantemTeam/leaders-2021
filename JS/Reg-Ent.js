$(document).ready(function() {
  $(".Reg_hide").click(function() {
    $('.registration_form').removeClass("active");
    $('.entrance_form').removeClass("active");
    $('.entrance_window').removeClass("active");
    $('.menu').slideToggle(300, function(){
    });
  });
})