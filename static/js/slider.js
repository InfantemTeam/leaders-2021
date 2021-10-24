var slideIndex = 0;

function plusSlide() {
	showSlides(slideIndex += 1);
}

function minusSlide() {
	showSlides(slideIndex -= 1);
}

function currentSlide(n) {
	showSlides(slideIndex = n);
}

function showSlides(n) {
	let slides = document.querySelectorAll('.item'),
	    dots = document.querySelectorAll('.slider-dots_item');

	if (n < 0) slideIndex = slides.length;
	else if (n >= slides.length) slideIndex = 0;

	for (let i = 0; i < slides.length; i++)
		slides[i].style.display = 'none';

	for (let i = 0; i < dots.length; i++)
		dots[i].className = dots[i].classList.remove('active');

	slides[slideIndex].style.display = 'block';
	dots[slideIndex].classList.add('active');
}

$(document).ready(function() {
	showSlides(slideIndex);
});
