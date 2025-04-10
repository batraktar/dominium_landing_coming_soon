// 🔹 Конфігурація фільтрів
const filterConfig = {
    apartments: ["Поверх", "Поверховість", "Ремонт", "Опалення", "Меблі", "Без комісії"],
    houses: ["Площа ділянки", "Поверховість", "Опалення", "Меблі"],
    land: ["Призначення", "Комунікації", "Площа ділянки"],
    commercial: ["Тип об'єкта", "Опалення", "Меблі"],
};

// 🔹 Модальне вікно фільтрів
const filterBtn = document.getElementById("filterBtn");
const filterModal = document.getElementById("filterModal");
const closeModal = document.getElementById("closeModal");

filterBtn?.addEventListener("click", () => {
    filterModal.classList.add("active");
});

closeModal?.addEventListener("click", () => {
    filterModal.classList.remove("active");
});

filterModal?.addEventListener("click", (e) => {
    if (e.target === filterModal) {
        filterModal.classList.remove("active");
    }
});

// 🔹 Випадаючий список "Тип нерухомості"
function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    const allDropdowns = document.querySelectorAll('[id^="propertyType"]');
    allDropdowns.forEach((d) => {
        if (d.id !== id) d.classList.add("hidden");
    });
    dropdown.classList.toggle("hidden");
}

document.addEventListener("click", (e) => {
    const dropdowns = document.querySelectorAll('.relative > div[id^="propertyType"]');
    dropdowns.forEach((dropdown) => {
        if (!dropdown.contains(e.target) && !e.target.closest("button")) {
            dropdown.classList.add("hidden");
        }
    });
});

// 🔹 Динамічні фільтри
const propertyCheckboxes = document.querySelectorAll('#propertyType input[type="checkbox"]');

const dynamicFiltersContainer = document.createElement("div");
dynamicFiltersContainer.className = "grid grid-cols-1 md:grid-cols-2 gap-6 mt-6";
document.querySelector("#filterModal > div")?.appendChild(dynamicFiltersContainer);

function renderDynamicFilters(selectedTypes) {
    dynamicFiltersContainer.innerHTML = "";
    const fields = new Set();
    selectedTypes.forEach((type) => {
        filterConfig[type]?.forEach((f) => fields.add(f));
    });

    fields.forEach((field) => {
        const wrapper = document.createElement("div");
        const label = document.createElement("label");
        label.className = "block text-sm font-medium text-gray-700 mb-2";
        label.textContent = field;

        const input = document.createElement("input");
        input.className = "w-full p-3 border rounded-button bg-gray-50";
        input.placeholder = field;

        wrapper.appendChild(label);
        wrapper.appendChild(input);
        dynamicFiltersContainer.appendChild(wrapper);
    });
}

propertyCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
        const selected = Array.from(propertyCheckboxes)
            .filter((cb) => cb.checked)
            .map((cb) => cb.value);
        renderDynamicFilters(selected);

        // Показ/приховування додаткового поля комерційної нерухомості
        const commercialCheckbox = document.querySelector(".commercial-checkbox");
        const commercialType = document.getElementById("commercialType");
        if (commercialCheckbox?.checked) {
            commercialType.classList.remove("hidden");
        } else {
            commercialType.classList.add("hidden");
        }

        // Відображення обраних назв у кнопці
        const selectedNames = Array.from(propertyCheckboxes)
            .filter((cb) => cb.checked)
            .map((cb) => cb.nextElementSibling.textContent);
        document.getElementById("propertyTypeSelected").textContent =
            selectedNames.length ? selectedNames.join(", ") : "Оберіть тип";
    });
});

// 🔹 Кнопка “Застосувати фільтри” – повідомлення
const applyBtn = document.querySelector("#filterModal button.bg-primary");
applyBtn?.addEventListener("click", () => {
    const note = document.createElement("div");
    note.className =
        "fixed bottom-4 right-4 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg z-[1100]";
    note.textContent = "Фільтри застосовано!";
    document.body.appendChild(note);
    setTimeout(() => note.remove(), 3000);
    filterModal.classList.remove("active");
});

// 🔹 Кнопка “Скинути фільтри”
document.addEventListener('DOMContentLoaded', function () {
    const resetFiltersBtn = document.getElementById('resetFilters');

    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', () => {
            document.querySelectorAll('#propertyType input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = false;
            });

            document.getElementById('propertyTypeSelected').textContent = 'Оберіть тип';

            document.querySelectorAll('#filterModal input[type="number"]').forEach(input => {
                input.value = '';
            });

            document.querySelectorAll('#filterModal select').forEach(select => {
                select.selectedIndex = 0;
            });

            document.getElementById('commercialType')?.classList.add('hidden');
            renderDynamicFilters([]);
        });
    }
});

// 🔹 Відправка форми “Зв’язок з нами”
const contactForm = document.querySelector("form");
contactForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    const notification = document.createElement("div");
    notification.className =
        "fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg";
    notification.textContent = "Повідомлення успішно надіслано!";
    document.body.appendChild(notification);
    e.target.reset();
    setTimeout(() => notification.remove(), 3000);
});
