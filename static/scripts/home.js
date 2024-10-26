var currentSlide = 0;

function showSlide(index) {
    const slides = document.querySelectorAll('.carousel-images img');

    let slideLimit;
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

    const offset = -currentSlide * 100;
    document.querySelector('.carousel-images').style.transform = `translateX(${offset}%)`;
}

function moveSlide(step) {
    showSlide(currentSlide + step);
}

function showFeedbackSlide(index) {
    const slides = document.querySelectorAll('.feedback-images img');

    let slideLimit;
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

    const offset = -currentSlide * 100;
    document.querySelector('.feedback-images').style.transform = `translateX(${offset}%)`;
}

function moveFeedbackSlide(step) {
    showFeedbackSlide(currentSlide + step);
}


