document.addEventListener("DOMContentLoaded", () => {
    const carousel = document.querySelector("[data-carousel]");

    if (!carousel) {
        return;
    }

    const track = carousel.querySelector("[data-carousel-track]");
    const previousButton = carousel.querySelector("[data-carousel-previous]");
    const nextButton = carousel.querySelector("[data-carousel-next]");
    const status = carousel.querySelector("[data-carousel-status]");
    const originalSlides = Array.from(track.children);

    const useFallback = (slide) => {
        const fallback = slide.dataset.fallback;

        if (fallback) {
            delete slide.dataset.fallback;
            slide.src = fallback;
        }
    };

    track.addEventListener("error", (event) => {
        if (event.target.matches("img")) {
            useFallback(event.target);
        }
    }, true);

    originalSlides.forEach((slide) => {
        if (slide.complete && slide.naturalWidth === 0) {
            useFallback(slide);
        }
    });

    if (originalSlides.length < 2) {
        previousButton.hidden = true;
        nextButton.hidden = true;
        return;
    }

    const firstClone = originalSlides[0].cloneNode(true);
    const lastClone = originalSlides[originalSlides.length - 1].cloneNode(true);
    firstClone.setAttribute("aria-hidden", "true");
    lastClone.setAttribute("aria-hidden", "true");
    track.prepend(lastClone);
    track.append(firstClone);

    let currentIndex = 1;
    let isMoving = false;
    let touchStartX = 0;

    const updateStatus = () => {
        const visibleIndex = ((currentIndex - 1 + originalSlides.length) % originalSlides.length) + 1;
        status.textContent = `Photo ${visibleIndex} of ${originalSlides.length}`;
    };

    const setPosition = (animate = true) => {
        track.classList.toggle("is-jumping", !animate);
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
        updateStatus();
    };

    const move = (direction) => {
        if (isMoving) {
            return;
        }

        isMoving = true;
        currentIndex += direction;
        setPosition();
    };

    previousButton.addEventListener("click", () => move(-1));
    nextButton.addEventListener("click", () => move(1));

    carousel.addEventListener("keydown", (event) => {
        if (event.key === "ArrowLeft") {
            event.preventDefault();
            move(-1);
        }

        if (event.key === "ArrowRight") {
            event.preventDefault();
            move(1);
        }
    });

    carousel.addEventListener("touchstart", (event) => {
        touchStartX = event.changedTouches[0].clientX;
    }, { passive: true });

    carousel.addEventListener("touchend", (event) => {
        const distance = event.changedTouches[0].clientX - touchStartX;

        if (Math.abs(distance) >= 50) {
            move(distance > 0 ? -1 : 1);
        }
    }, { passive: true });

    track.addEventListener("transitionend", () => {
        if (currentIndex === 0) {
            currentIndex = originalSlides.length;
            setPosition(false);
        } else if (currentIndex === originalSlides.length + 1) {
            currentIndex = 1;
            setPosition(false);
        }

        isMoving = false;
    });

    setPosition(false);
});
