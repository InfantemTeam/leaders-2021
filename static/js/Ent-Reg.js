$(document).ready(function() {
  $(".Ent_hide").click(function() {
    $('.registration_form').toggleClass("active");
    $('.entrance_form').toggleClass("active");
    $('.entrance_window').toggleClass("active");
    $('.menu').slideToggle(300, function(){
    });
  });
})