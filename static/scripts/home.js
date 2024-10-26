let currentSlide = 0;

function showSlide(index) {
    const slides = document.querySelectorAll('.carousel-images img');

    if (window.innerWidth >= 1200) {
        slideLimit = slides.length / 3;
    } else if (window.innerWidth >= 900) {
        slideLimit = slides.length / 2;
    } else {
        slideLimit = slides.length;
    }

    if (index < 0 || index >= slideLimit) {
        currentSlide = 0;
    } else {
        currentSlide = index;
    }


    const offset = -currentSlide * 100; // Each slide takes 100% width
    document.querySelector('.carousel-images').style.transform = `translateX(${offset}%)`;
}

function moveSlide(step) {
    showSlide(currentSlide + step);
}

// Initial call to display the first slide
showSlide(currentSlide);


function showFeedbackSlide(index) {
    const slides = document.querySelectorAll('.feedback-images img');

    if (window.innerWidth >= 1200) {
        slideLimit = slides.length / 3;
    } else if (window.innerWidth >= 900) {
        slideLimit = slides.length / 2;
    } else {
        slideLimit = slides.length;
    }

    if (index < 0 || index >= slideLimit) {
        currentSlide = 0;
    } else {
        currentSlide = index;
    }

    const offset = -currentSlide * 100; // Each slide takes 100% width
    document.querySelector('.feedback-images').style.transform = `translateX(${offset}%)`;
}

function moveFeedbackSlide(step) {
    showFeedbackSlide(currentSlide + step);
}

// Initial call to display the first slide
showSlide(currentSlide);