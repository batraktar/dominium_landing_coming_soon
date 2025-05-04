document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("contactForm");
    const propertyInput = document.getElementById("propertyTitle");
    const emailField = form.querySelector('input[name="email"]');

    // Автоматично вставляємо URL поточної сторінки в поле "property"
    propertyInput.value = window.location.href;

    // Додаємо чекбокс "Немає пошти"
    const emailWrapper = emailField.parentElement;
    const noEmailCheckbox = document.createElement("div");
    noEmailCheckbox.innerHTML = `
        <label class="flex items-center space-x-2 mt-2 text-sm text-gray-700">
            <input type="checkbox" id="noEmail" class="h-4 w-4">
            <span>Немає пошти</span>
        </label>
    `;
    emailWrapper.appendChild(noEmailCheckbox);

    document.getElementById("noEmail").addEventListener("change", function (e) {
        if (e.target.checked) {
            emailField.value = "";
            emailField.disabled = true;
            emailField.classList.add("bg-gray-100");
        } else {
            emailField.disabled = false;
            emailField.classList.remove("bg-gray-100");
        }
    });

    // Відправка форми
    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        if (emailField.disabled) {
            formData.set("email", ""); // якщо пошта відсутня
        }
        console.log([...formData.entries()]);


        try {
            const response = await fetch("/consultation/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams(formData),
            });


            const data = await response.json();

            if (response.ok) {
                showNotification("Повідомлення успішно надіслано!", "bg-green-500");
                form.reset();
                emailField.disabled = false;
                emailField.classList.remove("bg-gray-100");
                // Після reset треба ще раз записати URL у приховане поле:
                propertyInput.value = window.location.href;
            } else {
                const errorMessages = data.errors?.join("\n") || "Сталася помилка.";
                showNotification(errorMessages, "bg-red-500");
            }
        } catch (error) {
            showNotification("Помилка з'єднання з сервером.", "bg-red-500");
        }
    });

    function showNotification(message, bgColor) {
        const notification = document.createElement("div");
        notification.className = `fixed bottom-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50`;
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }
});
