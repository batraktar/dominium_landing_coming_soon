document.addEventListener('DOMContentLoaded', () => {
    const csrfToken = document.querySelector('#csrf-token')?.value;

    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const propertyId = button.getAttribute('data-property-id');

            try {
                const res = await fetch(`/like/${propertyId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                const data = await res.json();
                const icon = button.querySelector('i');

                if (data.status === 'liked') {
                    icon.classList.remove('ri-heart-line', 'text-coolSage');
                    icon.classList.add('ri-heart-fill', 'text-deepOcean');
                    showLikeNotification('Додано до обраного');
                } else if (data.status === 'unliked') {
                    icon.classList.remove('ri-heart-fill', 'text-deepOcean');
                    icon.classList.add('ri-heart-line', 'text-coolSage');
                    showLikeNotification('Видалено з обраного');
                }

            } catch (err) {
                console.error(err);
                showLikeNotification('Помилка лайку', true);
            }
        });
    });
});

function showLikeNotification(message, isError = false) {
    const note = document.createElement('div');
    note.textContent = message;
    note.className = `fixed bottom-6 right-6 px-4 py-2 rounded-lg shadow-lg text-white text-sm z-50 
                      ${isError ? 'bg-red-500' : 'bg-green-500'}`;
    document.body.appendChild(note);
    setTimeout(() => note.remove(), 2500);
}
