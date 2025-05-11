const scrollContainer = document.getElementById('scroll-container');

let startY = 0;
let isPulling = false;

scrollContainer.addEventListener('touchstart', (e) => {
    if (scrollContainer.scrollTop === 0) {
        startY = e.touches[0].clientY;
        isPulling = true;
    }
});

scrollContainer.addEventListener('touchmove', (e) => {
    if (!isPulling) return;
    const currentY = e.touches[0].clientY;
    const diff = currentY - startY;

    if (diff > 80) { // тягнули достатньо вниз
        location.reload(); // оновлюємо сторінку
        isPulling = false;
    }
});

scrollContainer.addEventListener('touchend', () => {
    isPulling = false;
});

