document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".ri-heart-line").forEach((icon) => {
        icon.addEventListener("click", function () {
            if (this.classList.contains("ri-heart-line")) {
                this.classList.remove("ri-heart-line");
                this.classList.add("ri-heart-fill");
                this.classList.add("text-red-500");
            } else {
                this.classList.remove("ri-heart-fill");
                this.classList.remove("text-red-500");
                this.classList.add("ri-heart-line");
            }
        });
    });
// View toggle
    const gridButton = document.querySelector(".ri-layout-grid-line").parentElement;
    const listButton = document.querySelector(".ri-list-check-2").parentElement;
    const resultsGrid = document.querySelector(
        ".grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-3",
    );
    gridButton.addEventListener("click", function () {
        gridButton.classList.remove("bg-white", "text-gray-500");
        gridButton.classList.add("bg-blue-50", "text-primary");
        listButton.classList.remove("bg-blue-50", "text-primary");
        listButton.classList.add("bg-white", "text-gray-500");
        // Переключаємо на відображення сіткою
        resultsGrid.classList.remove("md:grid-cols-1", "lg:grid-cols-1");
        resultsGrid.classList.add("md:grid-cols-2", "lg:grid-cols-3");
        // Змінюємо стиль карток
        document.querySelectorAll(".grid-cols-1 > div").forEach((card) => {
            card.classList.remove("flex", "flex-row");
            card.querySelector(".relative").classList.remove("w-1/3");
            card.querySelector(".p-4").classList.remove("w-2/3");
        });
    });
    listButton.addEventListener("click", function () {
        listButton.classList.remove("bg-white", "text-gray-500");
        listButton.classList.add("bg-blue-50", "text-primary");
        gridButton.classList.remove("bg-blue-50", "text-primary");
        gridButton.classList.add("bg-white", "text-gray-500");
        // Переключаємо на відображення списком
        resultsGrid.classList.remove("md:grid-cols-2", "lg:grid-cols-3");
        resultsGrid.classList.add("md:grid-cols-1", "lg:grid-cols-1");
        // Змінюємо стиль карток
        document.querySelectorAll(".grid-cols-1 > div").forEach((card) => {
            card.classList.add("flex", "flex-row");
            card.querySelector(".relative").classList.add("w-1/3");
            card.querySelector(".p-4").classList.add("w-2/3");
        });
    });
// Property type dropdown
    const propertyTypeBtn = document.getElementById("property-type-btn");
    const propertyTypeOptions = document.getElementById("property-type-options");
    const propertyTypeSelected = document.getElementById("property-type-selected");
    const propertyTypeCheckboxes = document.querySelectorAll(
        ".property-type-option",
    );
    propertyTypeBtn.addEventListener("click", function () {
        propertyTypeOptions.classList.toggle("hidden");
    });
    document.addEventListener("click", function (event) {
        if (
            !propertyTypeBtn.contains(event.target) &&
            !propertyTypeOptions.contains(event.target)
        ) {
            propertyTypeOptions.classList.add("hidden");
        }
    });
    propertyTypeCheckboxes.forEach((checkbox) => {
        checkbox.addEventListener("change", function () {
            const checkedOptions = Array.from(propertyTypeCheckboxes).filter(
                (cb) => cb.checked,
            );
            if (checkedOptions.length === 0) {
                propertyTypeSelected.textContent = "Всі типи";
            } else if (checkedOptions.length === 1) {
                const optionText = checkbox.parentElement.nextElementSibling.textContent;
                propertyTypeSelected.textContent = optionText;
            } else {
                propertyTypeSelected.textContent = `Вибрано ${checkedOptions.length}`;
            }
        });
    });
// Rooms dropdown
    const roomsBtn = document.getElementById("rooms-btn");
    const roomsOptions = document.getElementById("rooms-options");
    const roomsSelected = document.getElementById("rooms-selected");
    const roomOptions = document.querySelectorAll(".room-option");
    roomsBtn.addEventListener("click", function () {
        roomsOptions.classList.toggle("hidden");
    });
    document.addEventListener("click", function (event) {
        if (
            !roomsBtn.contains(event.target) &&
            !roomsOptions.contains(event.target)
        ) {
            roomsOptions.classList.add("hidden");
        }
    });
    roomOptions.forEach((option) => {
        option.addEventListener("click", function () {
            const value = this.getAttribute("data-value");
            roomsSelected.textContent = value ? this.textContent : "Будь-яка";
            roomOptions.forEach((opt) => {
                opt.classList.remove("bg-primary", "text-white");
                opt.classList.add("border-gray-300", "hover:bg-gray-50");
            });
            this.classList.remove("border-gray-300", "hover:bg-gray-50");
            this.classList.add("bg-primary", "text-white");
            roomsOptions.classList.add("hidden");
        });
    });
// Sort dropdown
    const sortBtn = document.getElementById("sort-btn");
    const sortOptions = document.getElementById("sort-options");
    const sortSelected = document.getElementById("sort-selected");
    const sortOptionBtns = document.querySelectorAll(".sort-option");
    const sortChecks = document.querySelectorAll(".sort-check");
    sortBtn.addEventListener("click", function () {
        sortOptions.classList.toggle("hidden");
    });
    document.addEventListener("click", function (event) {
        if (!sortBtn.contains(event.target) && !sortOptions.contains(event.target)) {
            sortOptions.classList.add("hidden");
        }
    });
    sortOptionBtns.forEach((option) => {
        option.addEventListener("click", function () {
            const value = this.getAttribute("data-value");
            sortSelected.textContent = this.textContent.trim();
            sortChecks.forEach((check) => {
                check.classList.add("hidden");
            });
            const checkIcon = this.querySelector(".sort-check");
            checkIcon.classList.remove("hidden");
            sortOptions.classList.add("hidden");
        });
    });
// Advanced filters toggle
    const advancedFiltersBtn = document.getElementById("advanced-filters-btn");
    const advancedFiltersPanel = document.getElementById("advanced-filters-panel");
    const advancedFiltersIcon = document.getElementById("advanced-filters-icon");
    const collapseFiltersBtn = document.getElementById("collapse-filters-btn");
    advancedFiltersBtn.addEventListener("click", function () {
        advancedFiltersPanel.classList.toggle("hidden");
        if (advancedFiltersPanel.classList.contains("hidden")) {
            advancedFiltersIcon.classList.remove("ri-arrow-up-s-line");
            advancedFiltersIcon.classList.add("ri-arrow-down-s-line");
        } else {
            advancedFiltersIcon.classList.remove("ri-arrow-down-s-line");
            advancedFiltersIcon.classList.add("ri-arrow-up-s-line");
        }
    });
    collapseFiltersBtn.addEventListener("click", function () {
        advancedFiltersPanel.classList.add("hidden");
        advancedFiltersIcon.classList.remove("ri-arrow-up-s-line");
        advancedFiltersIcon.classList.add("ri-arrow-down-s-line");
    });
// Repair type dropdown
    const repairTypeBtn = document.getElementById("repair-type-btn");
    const repairTypeOptions = document.getElementById("repair-type-options");
    const repairTypeSelected = document.getElementById("repair-type-selected");
    const repairTypeCheckboxes = document.querySelectorAll(".repair-type-option");
    repairTypeBtn.addEventListener("click", function () {
        repairTypeOptions.classList.toggle("hidden");
    });
    document.addEventListener("click", function (event) {
        if (
            !repairTypeBtn.contains(event.target) &&
            !repairTypeOptions.contains(event.target)
        ) {
            repairTypeOptions.classList.add("hidden");
        }
    });
    repairTypeCheckboxes.forEach((checkbox) => {
        checkbox.addEventListener("change", function () {
            const checkedOptions = Array.from(repairTypeCheckboxes).filter(
                (cb) => cb.checked,
            );
            if (checkedOptions.length === 0) {
                repairTypeSelected.textContent = "Будь-який";
            } else if (checkedOptions.length === 1) {
                const optionText = checkbox.parentElement.nextElementSibling.textContent;
                repairTypeSelected.textContent = optionText;
            } else {
                repairTypeSelected.textContent = `Вибрано ${checkedOptions.length}`;
            }
        });
    });
// search_filters.js

const modal = document.getElementById("advanced-filters-modal");
const openBtn = document.getElementById("advanced-filters-btn");
const closeBtn = document.getElementById("close-filters-btn");

if (modal && openBtn && closeBtn) {
  openBtn.addEventListener("click", () => {
    modal.classList.add("show"); // дає display: flex
    setTimeout(() => {
      modal.classList.add("visible"); // дає opacity + scale
    }, 10); // щоб дати браузеру час застосувати display
  });

  closeBtn.addEventListener("click", () => {
    modal.classList.remove("visible"); // починається анімація зникнення
    setTimeout(() => {
      modal.classList.remove("show"); // ховаємо після завершення
    }, 300); // дорівнює transition-duration
  });
}



// Heating type dropdown
    const heatingTypeBtn = document.getElementById("heating-type-btn");
    const heatingTypeOptions = document.getElementById("heating-type-options");
    const heatingTypeSelected = document.getElementById("heating-type-selected");
    const heatingTypeCheckboxes = document.querySelectorAll(".heating-type-option");
    heatingTypeBtn.addEventListener("click", function () {
        heatingTypeOptions.classList.toggle("hidden");
    });
    document.addEventListener("click", function (event) {
        if (
            !heatingTypeBtn.contains(event.target) &&
            !heatingTypeOptions.contains(event.target)
        ) {
            heatingTypeOptions.classList.add("hidden");
        }
    });
    heatingTypeCheckboxes.forEach((checkbox) => {
        checkbox.addEventListener("change", function () {
            const checkedOptions = Array.from(heatingTypeCheckboxes).filter(
                (cb) => cb.checked,
            );
            if (checkedOptions.length === 0) {
                heatingTypeSelected.textContent = "Будь-який";
            } else if (checkedOptions.length === 1) {
                const optionText = checkbox.parentElement.nextElementSibling.textContent;
                heatingTypeSelected.textContent = optionText;
            } else {
                heatingTypeSelected.textContent = `Вибрано ${checkedOptions.length}`;
            }
        });
    });
});