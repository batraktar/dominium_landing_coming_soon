/**
 * Template Name: MyResume
 * Template URL: https://bootstrapmade.com/free-html-bootstrap-template-my-resume/
 * Updated: Jun 29 2024 with Bootstrap v5.3.3
 * Author: BootstrapMade.com
 * License: https://bootstrapmade.com/license/
 */

(function () {
    "use strict";


    /**
     * Preloader
     */
    const preloader = document.querySelector('#preloader');
    if (preloader) {
        window.addEventListener('load', () => {
            preloader.remove();
        });
    }

    /**
     * Scroll top button
     */
    let scrollTop = document.querySelector('.scroll-top');

    function toggleScrollTop() {
        if (scrollTop) {
            window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
        }
    }

    scrollTop.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    window.addEventListener('load', toggleScrollTop);
    document.addEventListener('scroll', toggleScrollTop);

    /**
     * Animation on scroll function and init
     */
    function aosInit() {
        AOS.init({
            duration: 600,
            easing: 'ease-in-out',
            once: true,
            mirror: false
        });
    }

    window.addEventListener('load', aosInit);

    /**
     * Init typed.js
     */
    const selectTyped = document.querySelector('.typed');
    if (selectTyped) {
        let typed_strings = selectTyped.getAttribute('data-typed-items');
        typed_strings = typed_strings.split(',');
        new Typed('.typed', {
            strings: typed_strings,
            loop: true,
            typeSpeed: 100,
            backSpeed: 50,
            backDelay: 2000
        });
    }

    /**
     * Initiate Pure Counter
     */
    new PureCounter();

    /**
     * Animate the skills items on reveal
     */
    let skillsAnimation = document.querySelectorAll('.skills-animation');
    skillsAnimation.forEach((item) => {
        new Waypoint({
            element: item,
            offset: '80%',
            handler: function (direction) {
                let progress = item.querySelectorAll('.progress .progress-bar');
                progress.forEach(el => {
                    el.style.width = el.getAttribute('aria-valuenow') + '%';
                });
            }
        });
    });

    /**
     * Initiate glightbox
     */
    const glightbox = GLightbox({
        selector: '.glightbox'
    });

//   /**
//    * Init isotope layout and filters
//    */
//   document.querySelectorAll('.isotope-layout').forEach(function(isotopeItem) {
//     let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
//     let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
//     let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

//     let initIsotope;
//     imagesLoaded(isotopeItem.querySelector('.isotope-container'), function() {
//       initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
//         itemSelector: '.isotope-item',
//         layoutMode: layout,
//         filter: filter,
//         sortBy: sort
//       });
//     });

//     isotopeItem.querySelectorAll('.isotope-filters li').forEach(function(filters) {
//       filters.addEventListener('click', function() {
//         isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
//         this.classList.add('filter-active');
//         initIsotope.arrange({
//           filter: this.getAttribute('data-filter')
//         });
//         if (typeof aosInit === 'function') {
//           aosInit();
//         }
//       }, false);
//     });

//   });

    /**
     * Init swiper sliders
     */
    function initSwiper() {
        document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
            let config = JSON.parse(
                swiperElement.querySelector(".swiper-config").innerHTML.trim()
            );

            if (swiperElement.classList.contains("swiper-tab")) {
                initSwiperWithCustomPagination(swiperElement, config);
            } else {
                new Swiper(swiperElement, config);
            }
        });
    }

    window.addEventListener("load", initSwiper);

    /**
     * Correct scrolling position upon page load for URLs containing hash links.
     */
    window.addEventListener('load', function (e) {
        if (window.location.hash) {
            if (document.querySelector(window.location.hash)) {
                setTimeout(() => {
                    let section = document.querySelector(window.location.hash);
                    let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
                    window.scrollTo({
                        top: section.offsetTop - parseInt(scrollMarginTop),
                        behavior: 'smooth'
                    });
                }, 100);
            }
        }
    });

    /**
     * Navmenu Scrollspy
     */
    let navmenulinks = document.querySelectorAll('.navmenu a');

    function navmenuScrollspy() {
        navmenulinks.forEach(navmenulink => {
            if (!navmenulink.hash) return;
            let section = document.querySelector(navmenulink.hash);
            if (!section) return;
            let position = window.scrollY + 200;
            if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
                document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
                navmenulink.classList.add('active');
            } else {
                navmenulink.classList.remove('active');
            }
        })
    }

    window.addEventListener('load', navmenuScrollspy);
    document.addEventListener('scroll', navmenuScrollspy);

    document.addEventListener('DOMContentLoaded', function () {
        // Ініціалізація dropdown через JavaScript
        var dropdowns = document.querySelectorAll('.dropdown-toggle');
        dropdowns.forEach(function (dropdown) {
            new bootstrap.Dropdown(dropdown);
        });
    });

    // document.addEventListener("DOMContentLoaded", function () {
    //     const options = ["Option 1", "Option 2"];
    //     const inputField = document.getElementById("autocomplete-input");
    //     const autocompleteList = document.querySelector(".autocomplete-list");
    //     const selectedValueSpan = document.getElementById("selected-value");
    //     const inputValueSpan = document.getElementById("input-value");
    //
    //     function showSuggestions() {
    //         autocompleteList.innerHTML = "";
    //         const inputValue = inputField.value.toLowerCase();
    //         const filteredOptions = options.filter(option => option.toLowerCase().includes(inputValue));
    //
    //         filteredOptions.forEach(option => {
    //             const div = document.createElement("div");
    //             div.textContent = option;
    //             div.addEventListener("click", function () {
    //                 inputField.value = option;
    //                 selectedValueSpan.textContent = option;
    //                 autocompleteList.style.display = "none";
    //             });
    //             autocompleteList.appendChild(div);
    //         });
    //
    //         autocompleteList.style.display = filteredOptions.length ? "block" : "none";
    //     }
    //
    //     inputField.addEventListener("input", function () {
    //         inputValueSpan.textContent = inputField.value;
    //         showSuggestions();
    //     });
    //
    //     document.addEventListener("click", function (e) {
    //         if (!inputField.contains(e.target) && !autocompleteList.contains(e.target)) {
    //             autocompleteList.style.display = "none";
    //         }
    //     });
    // });

    document.addEventListener("DOMContentLoaded", function () {
        // Отримуємо елементи
        let modal = document.getElementById("searchModal");
        let openModalButton = document.getElementById("openModalButton");
        let closeModalButton = document.querySelector(".close");

        // Відкриваємо модальне вікно при натисканні на кнопку
        openModalButton.addEventListener("click", function (event) {
            event.preventDefault();  // Запобігаємо переходу за посиланням
            modal.style.display = "flex";  // Відображаємо модальне вікно
        });

        // Закриваємо модальне вікно при натисканні на кнопку закриття
        closeModalButton.addEventListener("click", function () {
            modal.style.display = "none";  // Приховуємо модальне вікно
        });

        // Закриваємо модальне вікно при кліку поза ним
        window.addEventListener("click", function (event) {
            if (event.target === modal) {
                modal.style.display = "none";  // Приховуємо модальне вікно
            }
        });
    });
    var swiper = new Swiper(".mySwiper", {
        slidesPerView: 1,
        spaceBetween: 10,
        loop: true,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        breakpoints: {
            768: {
                slidesPerView: 2,
                spaceBetween: 20,
            },
            1024: {
                slidesPerView: 3,
                spaceBetween: 30,
            }
        }
    });

    function toggleFilters() {
        const filterDropdown = document.getElementById("filterDropdown");
        if (filterDropdown.classList.contains("active")) {
            filterDropdown.style.opacity = "0";
            setTimeout(() => {
                filterDropdown.style.display = "none";
            }, 300); // Час анімації має збігатися з transition
        } else {
            filterDropdown.style.display = "block";
            setTimeout(() => {
                filterDropdown.style.opacity = "1";
            }, 10);
        }
        filterDropdown.classList.toggle("active");
    }

// Робимо функцію глобальною
    window.toggleFilters = toggleFilters;

})();