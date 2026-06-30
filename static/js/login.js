const slides = document.querySelectorAll('.carousel-slide');
const counter = document.getElementById('carouselCounter');
const nextBtn = document.getElementById('nextArrowBtn');

let currentIndex = 0;
const totalSlides = slides.length;
const AUTO_PLAY_DELAY = 5000; // 5 secondes

let autoPlayTimer = null;

function showSlide(index) {
    slides.forEach(function (slide) {
        slide.classList.remove('active');
    });
    slides[index].classList.add('active');
    counter.textContent = (index + 1) + ' of ' + totalSlides;
}

function nextSlide() {
    currentIndex = (currentIndex + 1) % totalSlides;
    showSlide(currentIndex);
}

function startAutoPlay() {
    autoPlayTimer = setInterval(nextSlide, AUTO_PLAY_DELAY);
}

function resetAutoPlay() {
    clearInterval(autoPlayTimer);
    startAutoPlay();
}

// Clic manuel sur la flèche
if (nextBtn) {
    nextBtn.addEventListener('click', function () {
        nextSlide();
        resetAutoPlay(); // relance le timer pour ne pas changer trop vite après un clic
    });
}

// Démarrer le carrousel automatique
if (slides.length > 0) {
    startAutoPlay();
}