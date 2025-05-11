const images = window.propertyImages || [];
let currentIndex = 0;

function updateAll() {
    const mainImg = document.querySelector('#gallery img');
    const modalImg = document.getElementById('modalImage');

    if (mainImg) mainImg.src = images[currentIndex];
    if (modalImg) modalImg.src = images[currentIndex];

    // Update dots
    document.querySelectorAll('#gallery .absolute.bottom-3 div').forEach((dot, index) => {
        dot.className = `w-2 h-2 rounded-full ${index === currentIndex ? 'bg-white/90' : 'bg-white/50'}`;
    });

    // Update thumbnails
    document.querySelectorAll('.thumbnail-img').forEach((thumb, index) => {
        const isActive = index === currentIndex;
        thumb.style.opacity = isActive ? '1' : '0.5';

        if (isActive) {
            thumb.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        }
    });


    // Toggle prev/next buttons
    const prevBtns = document.querySelectorAll('.btn-prev');
    const nextBtns = document.querySelectorAll('.btn-next');

    prevBtns.forEach(btn => {
        btn.style.display = currentIndex === 0 ? 'none' : 'block';
    });

    nextBtns.forEach(btn => {
        btn.style.display = currentIndex === images.length - 1 ? 'none' : 'block';
    });
}

function nextImage() {
    if (currentIndex < images.length - 1) {
        currentIndex++;
        updateAll();
    }
}

function prevImage() {
    if (currentIndex > 0) {
        currentIndex--;
        updateAll();
    }
}

function openGallery(index = null) {
    if (index !== null) {
        currentIndex = index;
    }
    updateAll();
    document.getElementById('galleryModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeGallery() {
    document.getElementById('galleryModal').classList.add('hidden');
    document.body.style.overflow = '';
}

function showModalImage(index) {
    currentIndex = index;
    updateAll();
}

document.addEventListener('DOMContentLoaded', () => {
    if (!images.length) return;

    updateAll();

    const container = document.querySelector('#galleryModal .flex.space-x-2');
    if (container) {
        container.innerHTML = '';
        images.forEach((src, index) => {
            const img = document.createElement('img');
            img.src = src;
            img.className = 'thumbnail-img';
            img.alt = `Thumbnail ${index + 1}`;
            img.onclick = () => showModalImage(index);
            container.appendChild(img);
        });
    }

    // Swipe in gallery
    const gallery = document.querySelector('#gallery');
    if (gallery) {
        let startX = 0;
        gallery.addEventListener('touchstart', e => startX = e.changedTouches[0].screenX);
        gallery.addEventListener('touchend', e => {
            const deltaX = e.changedTouches[0].screenX - startX;
            if (deltaX > 40) prevImage();
            else if (deltaX < -40) nextImage();
        });
    }

    // Swipe in modal
    const modalImg = document.getElementById('modalImage');
    if (modalImg) {
        let startX = 0;
        modalImg.addEventListener('touchstart', e => startX = e.changedTouches[0].screenX);
        modalImg.addEventListener('touchend', e => {
            const deltaX = e.changedTouches[0].screenX - startX;
            if (deltaX > 40) prevImage();
            else if (deltaX < -40) nextImage();
        });
    }

    // Keyboard navigation
    document.addEventListener('keydown', e => {
        const modal = document.getElementById('galleryModal');
        if (modal.classList.contains('hidden')) return;

        if (e.key === 'Escape') closeGallery();
        if (e.key === 'ArrowRight') nextImage();
        if (e.key === 'ArrowLeft') prevImage();
    });
});

function nextModalImage() {
    nextImage();
}

function prevModalImage() {
    prevImage();
}
