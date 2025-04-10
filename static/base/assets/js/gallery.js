const images = window.propertyImages || [];
let currentIndex = 0;
let modalCurrentIndex = 0;

function updateMainImage() {
    document.querySelector('#gallery img').src = images[currentIndex];
    updateDots();
}

function updateModalImage() {
    document.getElementById('modalImage').src = images[modalCurrentIndex];
    updateThumbnails();
}

function updateDots() {
    const dots = document.querySelectorAll('#gallery .absolute.bottom-4 div');
    dots.forEach((dot, index) => {
        dot.className = `w-2 h-2 rounded-full ${index === currentIndex ? 'bg-white/90' : 'bg-white/50'}`;
    });
}

function updateThumbnails() {
    const thumbnails = document.querySelectorAll('.thumbnail-img');
    thumbnails.forEach((thumb, index) => {
        thumb.style.opacity = index === modalCurrentIndex ? '1' : '0.5';
    });
}

function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateMainImage();
}

function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    updateMainImage();
}

function prevModalImage() {
    modalCurrentIndex = (modalCurrentIndex - 1 + images.length) % images.length;
    updateModalImage();
}

function nextModalImage() {
    modalCurrentIndex = (modalCurrentIndex + 1) % images.length;
    updateModalImage();
}

function openGallery(index) {
    currentIndex = index;
    modalCurrentIndex = index;
    updateModalImage();
    document.getElementById('galleryModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeGallery() {
    document.getElementById('galleryModal').classList.add('hidden');
    document.body.style.overflow = '';
}

function showModalImage(index) {
    modalCurrentIndex = index;
    updateModalImage();
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('#galleryModal .flex.space-x-2');
    if (!container || !images.length) return;
    container.innerHTML = '';
    images.forEach((src, index) => {
        const img = document.createElement('img');
        img.src = src;
        img.alt = `Thumbnail ${index + 1}`;
        img.className = 'thumbnail-img';
        img.onclick = () => showModalImage(index);
        container.appendChild(img);
    });
    updateThumbnails();
});

document.addEventListener('keydown', function (event) {
    if (document.getElementById('galleryModal').classList.contains('hidden')) return;
    if (event.key === 'Escape') closeGallery();
    if (event.key === 'ArrowLeft') prevModalImage();
    if (event.key === 'ArrowRight') nextModalImage();
});
document.addEventListener('DOMContentLoaded', () => {
    const gallery = document.querySelector('#gallery img');
    if (gallery && images.length > 0) {
        gallery.src = images[currentIndex];
    }
});
let touchStartX = 0;
let touchEndX = 0;

const gallery = document.getElementById('gallery');

if (gallery) {
    gallery.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, false);

    gallery.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, false);
}

function handleSwipe() {
    if (touchEndX < touchStartX - 40) {
        nextImage();
    } else if (touchEndX > touchStartX + 40) {
        prevImage();
    }
}
