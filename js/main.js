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
        const orderPanel = document.getElementById('orderPanel');
        if (orderPanel && orderPanel.classList.contains('open')) {
            orderPanel.classList.remove('open');
        }
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
        if (document.activeElement && mobileNav.contains(document.activeElement)) {
            document.activeElement.blur();
        }
        window.scrollTo({ left: 0 });
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

    // ─── Patrón Facade: Carga Diferida de Video (YouTube / Vimeo) ────────────
    document.querySelectorAll('.video-facade').forEach(function (facade) {
        function activateVideo() {
            if (facade.classList.contains('is-loaded')) return;
            const videoId  = facade.getAttribute('data-video-id');
            const platform = facade.getAttribute('data-platform') || 'youtube';
            const embedUrl = facade.getAttribute('data-embed-url');

            let src = '';
            if (embedUrl) {
                src = embedUrl;
            } else if (platform === 'youtube') {
                src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(videoId) + '?autoplay=1&rel=0';
            } else if (platform === 'vimeo') {
                src = 'https://player.vimeo.com/video/' + encodeURIComponent(videoId) + '?autoplay=1';
            }

            if (!src) return;

            const iframe = document.createElement('iframe');
            iframe.setAttribute('src', src);
            iframe.setAttribute('title', facade.getAttribute('data-video-title') || 'Reproductor de video');
            iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
            iframe.setAttribute('allowfullscreen', 'true');
            iframe.style.width = '100%';
            iframe.style.height = '100%';
            iframe.style.border = '0';
            iframe.style.position = 'absolute';
            iframe.style.top = '0';
            iframe.style.left = '0';
            iframe.style.zIndex = '3';

            facade.classList.add('is-loaded');

            const playBtn = facade.querySelector('.facade-play-btn');
            if (playBtn) playBtn.remove();

            facade.appendChild(iframe);
            iframe.focus();
        }

        facade.addEventListener('click', activateVideo);
        facade.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                activateVideo();
            }
        });
    });

})();
