document.addEventListener("DOMContentLoaded", () => {
    // ========== Мобільне меню ==========
    const mobileMenuToggle = document.getElementById("mobile-menu-toggle");
    const sidebar = document.getElementById("sidebar");

    mobileMenuToggle?.addEventListener("click", () => {
        sidebar.classList.toggle("open");
    });

    document.addEventListener("click", (event) => {
        if (
            window.innerWidth < 1024 &&
            !sidebar.contains(event.target) &&
            !mobileMenuToggle.contains(event.target) &&
            sidebar.classList.contains("open")
        ) {
            sidebar.classList.remove("open");
        }
    });

    function getCSRFToken() {
        const name = "csrftoken";
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
        return null;
    }

    // ========== Імпорт об'єкта через URL ==========
    const importBtn = document.getElementById("import-btn");
    const importText = document.getElementById("import-text");
    const importSpinner = document.getElementById("import-spinner");

    importBtn?.addEventListener("click", async () => {
        const urlsText = document.getElementById("import-urls")?.value;
        const urls = urlsText
            .split("\n")
            .map((url) => url.trim())
            .filter((url) => url.length > 0);

        if (urls.length === 0) {
            return alert("Введіть хоча б один URL");
        }

        importBtn.disabled = true;
        importSpinner.classList.remove("hidden");
        importText.textContent = "Імпортування...";

        let successCount = 0;

        for (const url of urls) {
            try {
                const response = await fetch("/admin-panel/import-from-url/", {
                    method: "POST",
                    headers: {"Content-Type": "application/x-www-form-urlencoded"},
                    body: new URLSearchParams({url}),
                });

                const data = await response.json();

                if (data.status === "ok") {
                    successCount++;
                    console.log("✅ Успішно імпортовано:", url);
                } else {
                    console.warn("❌ Помилка імпорту:", url, data.message);
                }
            } catch (error) {
                console.error("⚠️ Помилка під час запиту:", url, error);
            }
        }

        importText.textContent = "Імпортувати";
        importSpinner.classList.add("hidden");
        importBtn.disabled = false;

        alert(`Готово! Успішно імпортовано: ${successCount} з ${urls.length}`);
    });


    // ========== Модалка додавання об'єкта ==========
    const propertyModal = document.getElementById("property-modal");
    const addPropertyBtn = document.getElementById("add-property-btn");
    const closeModalBtn = document.getElementById("close-edit-modal");
    const cancelBtn = document.getElementById("cancel-edit-btn");
    const modalTitle = document.getElementById("modal-title");

    function openModal(isEdit = false) {
        propertyModal.classList.remove("hidden");
        document.body.style.overflow = "hidden";
        modalTitle.textContent = isEdit ? "Редагувати об'єкт" : "Додати новий об'єкт";
    }

    function closeModal() {
        propertyModal.classList.add("hidden");
        document.body.style.overflow = "";
    }

    addPropertyBtn?.addEventListener("click", () => openModal(false));
    closeModalBtn?.addEventListener("click", closeModal);
    cancelBtn?.addEventListener("click", closeModal);

    propertyModal?.addEventListener("click", (event) => {
        if (event.target === propertyModal) closeModal();
    });

    const propertyForm = document.getElementById("property-form");
    propertyForm?.addEventListener("submit", (event) => {
        event.preventDefault();
        closeModal();
    });

    // ========== Історія змін ==========
    const historyButtons = document.querySelectorAll(".ri-history-line");
    historyButtons.forEach((button) => {
        button.parentElement.addEventListener("click", () => {
            const historyModal = document.createElement("div");
            historyModal.className =
                "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50";
            historyModal.innerHTML = `...`; // залишив скорочено, можу вставити повністю при потребі
            document.body.appendChild(historyModal);

            historyModal.querySelector(".close-history").addEventListener("click", () => historyModal.remove());
            historyModal.addEventListener("click", (e) => {
                if (e.target === historyModal) historyModal.remove();
            });
        });
    });

    // ========== Редагування об'єкта (модалка + фото) ==========
    const editModal = document.getElementById("property-edit-modal");
    const editBtns = document.querySelectorAll(".edit-property-btn");
    const closeEditModal = editModal?.querySelector("#close-edit-modal");


    function openEditModal(data) {
        console.log("data перед вставкою в модалку:", data);
        editModal.classList.remove("hidden");
        document.body.style.overflow = "hidden";

        document.getElementById("edit-title").value = data.title;
        document.getElementById("edit-address").value = data.address;
        document.getElementById("edit-rooms").value = data.rooms;
        document.getElementById("edit-area").value = data.area;
        document.getElementById("deal_type").value = data["deal-type"];
        document.getElementById("property_type").value = data["property-type"];

        document.getElementById("edit-price").value = data.price
            ? data.price.replace(",", ".")
            : "";
        document.getElementById("edit-property-id").value = data.id;

        const gallery = document.getElementById("edit-gallery");
        gallery.innerHTML = "<p class='text-sm text-gray-400'>Завантаження фото...</p>";

        fetch(`/admin-panel/api/property/${data.id}/images/`)
            .then((res) => res.json())
            .then((images) => {
                gallery.innerHTML = "";

                if (!images.length) {
                    gallery.innerHTML = "<p class='text-sm text-gray-400'>Фото відсутні</p>";
                    return;
                }

                images.forEach((img, index) => {
                    const isMain = img.is_main;
                    const wrapper = document.createElement("div");
                    wrapper.className = "relative group";

                    wrapper.innerHTML = `
        <div class="aspect-w-1 aspect-h-1 w-full overflow-hidden rounded-lg bg-gray-100">
            <img src="${img.url}" alt="Фото ${index + 1}" class="w-full h-full object-cover object-top" />
        </div>
        <div class="absolute inset-0 bg-black bg-opacity-40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
            <button type="button" class="p-1 bg-white rounded-full whitespace-nowrap !rounded-button">
                <i class="ri-eye-line text-gray-700"></i>
            </button>
            <button type="button" class="p-1 bg-white rounded-full whitespace-nowrap !rounded-button">
                <i class="ri-delete-bin-line text-red-500"></i>
            </button>
        </div>
        <div class="absolute top-2 left-2">
            <label class="custom-checkbox">
                <input type="checkbox" name="main_photo" data-id="${img.id}" ${isMain ? "checked" : ""} />
                <span class="checkmark"></span>
            </label>
        </div>
    `;

                    gallery.appendChild(wrapper);
                });

// 🧠 Тут одразу додаємо логіку: тільки одне головне фото
                setTimeout(() => {
                    const dynamicMainInputs = gallery.querySelectorAll('input[name="main_photo"]');
                    dynamicMainInputs.forEach((input) => {
                        input.addEventListener("change", () => {
                            dynamicMainInputs.forEach((otherInput) => {
                                if (otherInput !== input) {
                                    otherInput.checked = false;
                                }
                            });
                        });
                    });
                }, 0);
            })
            .catch((err) => {
                gallery.innerHTML = "<p class='text-sm text-red-500'>⚠️ Помилка завантаження фото</p>";
                console.error(err);
            });
    }

    editBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            openEditModal(btn.dataset);
        });
    });

    closeEditModal?.addEventListener("click", () => {
        editModal.classList.add("hidden");
        document.body.style.overflow = "";
    });

    // ========== Експорт ==========
    const exportButton = document.querySelector("button:has(.ri-download-line)");
    exportButton?.addEventListener("click", () => {
        const exportModal = document.createElement("div");
        exportModal.className =
            "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50";
        exportModal.innerHTML = `...`; // можу додати повну розмітку
        document.body.appendChild(exportModal);

        exportModal.querySelector(".close-export").addEventListener("click", () => exportModal.remove());
        exportModal.addEventListener("click", (e) => {
            if (e.target === exportModal) exportModal.remove();
        });
    });
    const editForm = document.getElementById("property-edit-modal");

    editForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const id = document.getElementById("edit-property-id").value;
        const title = document.getElementById("edit-title").value;
        const address = document.getElementById("edit-address").value;
        const area = document.getElementById("edit-area").value;
        const rooms = document.getElementById("edit-rooms").value;
        const price = document.getElementById("edit-price").value;

        // 🧠 Валідація: лише одне головне фото
        const mainPhotoInputs = document.querySelectorAll('#edit-gallery input[name="main_photo"]');
        const mainPhotoIds = [];

        mainPhotoInputs.forEach((checkbox, index) => {
            if (checkbox.checked) {
                const photoId = checkbox.dataset.id;
                if (photoId && !isNaN(photoId)) {
                    mainPhotoIds.push(parseInt(photoId));
                }
            }
        });

        if (mainPhotoIds.length > 1) {
            alert("Можна вибрати лише одне головне фото.");
            return;
        }
        const deal_type = parseInt(document.getElementById("deal_type").value);
        const property_type = parseInt(document.getElementById("property_type").value);

        const payload = {
            title,
            address,
            area,
            rooms,
            price,
            deal_type,
            property_type,
            main_photo_ids: mainPhotoIds,
        };


        const response = await fetch(`/admin-panel/api/properties/${id}/patch/`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify(payload),
        });


        const result = await response.json();

        if (result.status === "ok") {
            alert("Обʼєкт оновлено");
            location.reload();
        } else {
            alert("Помилка: " + result.message);
        }
    });

    // ========== Radio для головного фото ==========
    const mainPhotoInputs = document.querySelectorAll('input[name="main_photo"]');
    mainPhotoInputs.forEach((input) => {
        input.addEventListener("change", function () {
            mainPhotoInputs.forEach((otherInput) => {
                if (otherInput !== input) {
                    otherInput.checked = false;
                }
            });
        });
    });
});
