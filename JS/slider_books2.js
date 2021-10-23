var slideNow2 = 1;
var slideCount2 = $('#slidewrapper2').children().length;
var slideInterval2 = 10000;
var navBtnId2 = 0;
var translateWidth2 = 0;

$(document).ready(function() {
    var switchInterval2 = setInterval(nextSlide2, slideInterval2);

    $('#viewport2').hover(function() {
        clearInterval(switchInterval2);
    }, function() {
        switchInterval2 = setInterval(nextSlide2, slideInterval2);
    });

    $('#next-btn2').click(function() {
        nextSlide2();
    });

    $('#prev-btn2').click(function() {
        prevSlide2();
    });

    $('.slide-nav-btn').click(function() {
        navBtnId2 = $(this).index();

        if (navBtnId2 + 1 != slideNow2) {
            translateWidth2 = -$('#viewport2').width() * (navBtnId2);
            $('#slidewrapper2').css({
                'transform': 'translate(' + translateWidth2 + 'px, 0)',
                '-webkit-transform': 'translate(' + translateWidth2 + 'px, 0)',
                '-ms-transform': 'translate(' + translateWidth2 + 'px, 0)',
            });
            slideNow2 = navBtnId2 + 1;
        }
    });
});


function nextSlide2() {
    if (slideNow2 == slideCount2 || slideNow2 <= 0 || slideNow2 > slideCount2) {
        $('#slidewrapper2').css('transform', 'translate(0, 0)');
        slideNow2 = 1;
    } else {
        translateWidth2 = -$('#viewport2').width() * (slideNow2);
        $('#slidewrapper2').css({
            'transform': 'translate(' + translateWidth2 + 'px, 0)',
            '-webkit-transform': 'translate(' + translateWidth2 + 'px, 0)',
            '-ms-transform': 'translate(' + translateWidth2 + 'px, 0)',
        });
        slideNow2++;
    }
}

function prevSlide2() {
    if (slideNow2 == 1 || slideNow2 <= 0 || slideNow2 > slideCount2) {
        translateWidth2 = -$('#viewport2').width() * (slideCount2 - 1);
        $('#slidewrappe2').css({
            'transform': 'translate(' + translateWidth2 + 'px, 0)',
            '-webkit-transform': 'translate(' + translateWidth2 + 'px, 0)',
            '-ms-transform': 'translate(' + translateWidth2 + 'px, 0)',
        });
        slideNow2 = slideCount2;
    } else {
        translateWidth2 = -$('#viewport2').width() * (slideNow2 - 2);
        $('#slidewrapper2').css({
            'transform': 'translate(' + translateWidth2 + 'px, 0)',
            '-webkit-transform': 'translate(' + translateWidth2 + 'px, 0)',
            '-ms-transform': 'translate(' + translateWidth2 + 'px, 0)',
        });
        slideNow2--;
    }
}