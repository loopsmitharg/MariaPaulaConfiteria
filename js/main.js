/**
 * María Paula Confitería
 * Hamburger Menu – Mobile Navigation Controller
 * Drawer deslizante desde la derecha con accordion dropdowns.
 */

(function () {
    'use strict';

    const hamburgerBtn  = document.getElementById('hamburger-btn');
    const closeBtn      = document.getElementById('mobile-nav-close');
    const mobileNav     = document.getElementById('mobile-nav');
    const navOverlay    = document.getElementById('nav-overlay');
    const body          = document.body;

    // ─── Abrir / Cerrar menú ─────────────────────────────────────────────────
    function openMenu() {
        hamburgerBtn.classList.add('is-active');
        mobileNav.classList.add('is-open');
        navOverlay.classList.add('is-visible');
        body.classList.add('menu-open');
        hamburgerBtn.setAttribute('aria-expanded', 'true');
    }

    function closeMenu() {
        hamburgerBtn.classList.remove('is-active');
        mobileNav.classList.remove('is-open');
        navOverlay.classList.remove('is-visible');
        body.classList.remove('menu-open');
        hamburgerBtn.setAttribute('aria-expanded', 'false');
    }

    function toggleMenu() {
        if (mobileNav.classList.contains('is-open')) {
            closeMenu();
        } else {
            openMenu();
        }
    }

    // ─── Eventos ─────────────────────────────────────────────────────────────
    if (hamburgerBtn) {
        hamburgerBtn.addEventListener('click', toggleMenu);
    }

    // Cerrar desde la "X" adentro del drawer
    if (closeBtn) {
        closeBtn.addEventListener('click', closeMenu);
    }

    // Cerrar al hacer click en el overlay
    if (navOverlay) {
        navOverlay.addEventListener('click', closeMenu);
    }

    // Cerrar con tecla Escape
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeMenu();
    });

    // Cerrar al hacer click en un link que NO sea accordion
    document.querySelectorAll('#mobile-nav .mobile-nav-link:not(.accordion-toggle)').forEach(function (link) {
        link.addEventListener('click', closeMenu);
    });

    // ─── Accordion Dropdowns ─────────────────────────────────────────────────
    document.querySelectorAll('.accordion-toggle').forEach(function (toggle) {
        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            const parent      = toggle.closest('.mobile-dropdown');
            const submenu     = parent.querySelector('.mobile-submenu');
            const isOpen      = parent.classList.contains('accordion-open');

            // Cerrar todos los otros acordeones
            document.querySelectorAll('.mobile-dropdown.accordion-open').forEach(function (openItem) {
                openItem.classList.remove('accordion-open');
                openItem.querySelector('.mobile-submenu').style.maxHeight = null;
            });

            // Abrir / cerrar el actual
            if (!isOpen) {
                parent.classList.add('accordion-open');
                submenu.style.maxHeight = submenu.scrollHeight + 'px';
            }
        });
    });

    // ─── Resize: cerrar menú si la ventana crece a desktop ───────────────────
    window.addEventListener('resize', function () {
        if (window.innerWidth > 1024) {
            closeMenu();
        }
    });

    // ─── Modal Carta: bloqueo de scroll ──────────────────────────────────────
    // El modal usa CSS puro (checkbox + label). Solo necesitamos JS para
    // bloquear/desbloquear el scroll del body cuando el modal está abierto.
    document.querySelectorAll('.modal-toggle').forEach(function (toggle) {
        toggle.addEventListener('change', function () {
            if (this.checked) {
                body.classList.add('no-scroll');      // Modal abierto → bloquear scroll
            } else {
                body.classList.remove('no-scroll');   // Modal cerrado → restaurar scroll
            }
        });
    });

    // Cerrar modal con tecla Escape (desmarca el checkbox)
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-toggle:checked').forEach(function (t) {
                t.checked = false;
                body.classList.remove('no-scroll');
            });
        }
    });

})();
