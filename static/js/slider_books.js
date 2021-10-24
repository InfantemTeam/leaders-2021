const slideInterval = 9000;

$(document).ready(function() {
	$('.slider-viewport').each(function() {
		let e = this;

		e.slideCount = $(this).find('.slidewrapper').children().length;
		e.slideNow = 0;

		$(this).hover(function() {
			clearInterval(e.switchInterval);
		}, function() {
			e.switchInterval = setInterval(function() { nextSlide(e); }, slideInterval);
		});
		e.switchInterval = setInterval(function() { nextSlide(e); }, slideInterval);

		$(this).find('.next-btn').click(function() {
			nextSlide(e);
		});

		$(this).find('.prev-btn').click(function() {
			prevSlide(e);
		});

		$(this).find('.slide-nav-btn').click(function() {
			let navBtnId = $(this).index();

			if (navBtnId != e.slideNow) {
				e.slideNow = navBtnId;
				updateSlide(e);
			}
		});
	});
});

function nextSlide(slider) {
	if (slider.slideNow >= slider.slideCount-1) slider.slideNow = 0;
	else slider.slideNow++;
	updateSlide(slider);
}

function prevSlide(slider) {
	if (slider.slideNow <= 0) slider.slideNow = slider.slideCount-1;
	else slider.slideNow--;
	updateSlide(slider);
}

function updateSlide(slider) {
	let translateWidth = -$(slider).width() * slider.slideNow;
	$(slider).find('.slidewrapper').css({'transform': 'translateX('+translateWidth+'px)'});
}
