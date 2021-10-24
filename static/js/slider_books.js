var slideNow = 0,
    slideInterval = 9000,
    slideCount;

$(document).ready(function() {
	slideCount = $('#slidewrapper').children().length;

	let switchInterval = setInterval(nextSlide, slideInterval);

	$('#viewport').hover(function() {
		clearInterval(switchInterval);
	}, function() {
		switchInterval = setInterval(nextSlide, slideInterval);
	});

	$('#next-btn').click(function() {
		nextSlide();
	});

	$('#prev-btn').click(function() {
		prevSlide();
	});

	$('.slide-nav-btn').click(function() {
		let navBtnId = $(this).index();

		if (navBtnId != slideNow) {
			slideNow = navBtnId;
			updateSlide();
		}
	});
});

function nextSlide() {
	if (slideNow >= slideCount-1) slideNow = 0;
	else slideNow++;
	updateSlide();
}

function prevSlide() {
	if (slideNow <= 0) slideNow = slideCount-1;
	else slideNow--;
	updateSlide();
}

function updateSlide() {
	let translateWidth = -$('#viewport').width() * slideNow;
	$('#slidewrapper').css({
		'transform': 'translate(' + translateWidth + 'px, 0)',
		'-webkit-transform': 'translate(' + translateWidth + 'px, 0)',
		'-ms-transform': 'translate(' + translateWidth + 'px, 0)',
	});
}
