/**
 * Template Name: ComingSoon
 * Template URL: https://bootstrapmade.com/comingsoon-free-html-bootstrap-template/
 * Updated: Aug 07 2024 with Bootstrap v5.3.3
 * Author: BootstrapMade.com
 * License: https://bootstrapmade.com/license/
 */

(function () {
    "use strict";


    /**
     * Apply .scrolled class to the body as the page is scrolled down
     */

    /**
     * Mobile nav toggle
     */
    const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

    function mobileNavToogle() {
        document.querySelector('body').classList.toggle('mobile-nav-active');
        mobileNavToggleBtn.classList.toggle('bi-list');
        mobileNavToggleBtn.classList.toggle('bi-x');
    }

    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);

    /**
     * Hide mobile nav on same-page/hash links
     */
    document.querySelectorAll('#navmenu a').forEach(navmenu => {
        navmenu.addEventListener('click', () => {
            if (document.querySelector('.mobile-nav-active')) {
                mobileNavToogle();
            }
        });

    });

    /**
     * Toggle mobile nav dropdowns
     */
    // document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    //   navmenu.addEventListener('click', function(e) {
    //     e.preventDefault();
    //     this.parentNode.classList.toggle('active');
    //     this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
    //     e.stopImmediatePropagation();
    //   });
    // });

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

    document.addEventListener("DOMContentLoaded", function () {
        const serviceTitles = document.querySelectorAll(".service-title");
        const serviceCards = document.querySelectorAll(".service-card");

        serviceTitles.forEach((title) => {
            title.addEventListener("mouseenter", (e) => {
                const targetId = e.target.getAttribute("data-target");

                // Прибираємо всі активні картки
                serviceCards.forEach((card) => card.classList.remove("active"));

                // Відображаємо відповідну картку
                const activeCard = document.getElementById(targetId);
                if (activeCard) {
                    activeCard.classList.add("active");
                }
            });
        });
    });



})();