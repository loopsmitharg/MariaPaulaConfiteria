/**
 * María Paula Confitería
 * JavaScript Vanilla Desacoplado (ES6+)
 * 
 * - Carga asíncrona no bloqueante (defer)
 * - Delegación global de eventos sobre document (e.target.closest)
 * - Manejo asíncrono de formularios mediante fetch() POST JSON
 * - Notificaciones flotantes temporales (Toast) de 5 segundos
 * - Drawer de navegación móvil con acordeones
 * - Filtros, modal de opciones y carrito de pedidos desacoplados del DOM
 * - Reproductor de video bajo demanda (Patrón Facade)
 * - Portabilidad de rutas dinámicas mediante atributo data-root
 */

(function () {
    'use strict';

    // ─── 1. Portabilidad de Rutas Dinámicas (data-root) ──────────────────────
    const projectRoot = document.body ? (document.body.getAttribute('data-root') || './') : './';

    /**
     * Resuelve una ruta relativa o con barra inicial respecto a projectRoot.
     * Preserva URLs externas, anclas, esquemas mailto: o tel:.
     * @param {string} path - Ruta de archivo o recurso.
     * @returns {string} - Ruta resuelta y portable.
     */
    function resolvePath(path) {
        if (!path) return path;
        if (/^(?:https?:|\/\/|#|mailto:|tel:)/i.test(path)) {
            return path;
        }
        const cleanPath = path.startsWith('/') ? path.slice(1) : path;
        const base = projectRoot.endsWith('/') ? projectRoot : projectRoot + '/';
        return base + cleanPath;
    }

    // Exponer API de utilidades globales del proyecto
    window.MariaPaula = window.MariaPaula || {};
    window.MariaPaula.projectRoot = projectRoot;
    window.MariaPaula.resolvePath = resolvePath;

    // ─── 2. Sistema de Notificaciones Flotantes (Toast) ─────────────────────
    let toastTimeout = null;

    /**
     * Muestra un aviso interactivo flotante con animación GPU y timeout automático.
     * @param {string} message - Texto descriptivo para el usuario.
     * @param {number} duration - Duración en milisegundos (por defecto 5000ms = 5s).
     * @param {string} type - Tipo de notificación ('success' o 'error').
     */
    function showToast(message, duration = 5000, type = 'success') {
        let toast = document.getElementById('toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'toast';
            toast.setAttribute('role', 'status');
            toast.setAttribute('aria-live', 'polite');
            document.body.appendChild(toast);
        }
        toast.textContent = message;
        if (type === 'error') {
            toast.style.backgroundColor = 'var(--color-danger, #e63946)';
        } else {
            toast.style.backgroundColor = 'var(--wood-dark, #4a3b32)';
        }
        toast.classList.add('show');

        if (toastTimeout) {
            clearTimeout(toastTimeout);
        }
        toastTimeout = setTimeout(() => {
            toast.classList.remove('show');
        }, duration);
    }
    window.MariaPaula.showToast = showToast;

    // ─── 3. Controlador de Navegación Móvil (Drawer & Acordeones) ────────────
    function openMenu() {
        const hamburgerBtn = document.getElementById('hamburger-btn');
        const mobileNav    = document.getElementById('mobile-nav');
        const navOverlay   = document.getElementById('nav-overlay');
        const orderPanel   = document.getElementById('orderPanel');

        if (orderPanel && orderPanel.classList.contains('open')) {
            orderPanel.classList.remove('open');
        }
        if (hamburgerBtn) {
            hamburgerBtn.classList.add('is-active');
            hamburgerBtn.setAttribute('aria-expanded', 'true');
        }
        if (mobileNav) mobileNav.classList.add('is-open');
        if (navOverlay) navOverlay.classList.add('is-visible');
        document.body.classList.add('menu-open');
    }

    function closeMenu() {
        const hamburgerBtn = document.getElementById('hamburger-btn');
        const mobileNav    = document.getElementById('mobile-nav');
        const navOverlay   = document.getElementById('nav-overlay');

        if (hamburgerBtn) {
            hamburgerBtn.classList.remove('is-active');
            hamburgerBtn.setAttribute('aria-expanded', 'false');
        }
        if (mobileNav) mobileNav.classList.remove('is-open');
        if (navOverlay) navOverlay.classList.remove('is-visible');
        document.body.classList.remove('menu-open');

        document.querySelectorAll('.mobile-dropdown.accordion-open').forEach(openItem => {
            openItem.classList.remove('accordion-open');
            const toggleBtn = openItem.querySelector('.accordion-toggle');
            if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
        });

        if (document.activeElement && mobileNav && mobileNav.contains(document.activeElement)) {
            document.activeElement.blur();
        }
        window.scrollTo({ left: 0 });
    }

    function toggleMenu() {
        const mobileNav = document.getElementById('mobile-nav');
        if (mobileNav && mobileNav.classList.contains('is-open')) {
            closeMenu();
        } else {
            openMenu();
        }
    }

    // ─── 4. Patrón Facade: Carga Diferida de Video ──────────────────────────
    function activateVideo(facade) {
        if (!facade || facade.classList.contains('is-loaded')) return;
        const videoSrc = facade.getAttribute('data-video-src');
        const videoId  = facade.getAttribute('data-video-id');
        const platform = facade.getAttribute('data-platform') || (videoSrc ? 'local' : 'youtube');
        const embedUrl = facade.getAttribute('data-embed-url');

        facade.classList.add('is-loaded');

        const playBtn = facade.querySelector('.facade-play-btn');
        if (playBtn) playBtn.remove();

        if (videoSrc || platform === 'local') {
            const rawSrc = videoSrc || 'assets/videos/VideoMariaPaula.mp4';
            const src = resolvePath(rawSrc);
            const video = document.createElement('video');
            video.setAttribute('controls', '');
            video.setAttribute('autoplay', '');
            video.setAttribute('playsinline', '');
            video.className = 'video-demand';

            const source = document.createElement('source');
            source.src = src;
            source.type = 'video/mp4';
            video.appendChild(source);

            facade.appendChild(video);
            video.play().catch(() => {});
            video.focus();
            return;
        }

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

        facade.appendChild(iframe);
        iframe.focus();
    }

    // ─── 5. Lógica del Catálogo de la Carta y Filtros ────────────────────────
    function filterItems(categories) {
        const allItems = document.querySelectorAll('.menu-card-rich');
        allItems.forEach(item => {
            let match = false;
            categories.forEach(cat => {
                if (cat === 'all') {
                    match = true;
                } else if (cat === 'bebidas') {
                    if (item.classList.contains('category-bebidas') ||
                        item.classList.contains('category-bebidas-calientes') ||
                        item.classList.contains('category-bebidas-frias') ||
                        item.classList.contains('category-bebidas-gaseosas') ||
                        item.classList.contains('category-cafeteria') ||
                        item.classList.contains('category-licuados')) {
                        match = true;
                    }
                } else if (item.classList.contains('category-' + cat)) {
                    match = true;
                }
            });
            if (match) item.classList.remove('hidden');
            else item.classList.add('hidden');
        });
    }

    function scrollToMenu() {
        const filterContainer = document.querySelector('.filter-sticky-container');
        if (!filterContainer) return;

        const header = document.getElementById('site-header');
        const headerHeight = header ? header.offsetHeight : 70;

        const containerRect = filterContainer.getBoundingClientRect();
        const containerTop = containerRect.top + window.pageYOffset;
        const targetScroll = containerTop - headerHeight;

        if (Math.abs(window.pageYOffset - targetScroll) > 25) {
            window.scrollTo({
                top: Math.max(0, targetScroll),
                behavior: 'smooth'
            });
        }
    }

    function filterMenu(category, isSubmenu = false, clickedBtn = null) {
        const allItems      = document.querySelectorAll('.menu-card-rich');
        const mainFilters   = document.querySelectorAll('.main-filter');
        const subFilters    = document.querySelectorAll('.sub-filter');

        const subBebidas    = document.querySelectorAll('.sub-bebidas');
        const subComidas    = document.querySelectorAll('.sub-comidas');
        const subDesayuno   = document.querySelectorAll('.sub-desayuno');
        const subPasteleria = document.querySelectorAll('.sub-pasteleria');

        scrollToMenu();

        // Submenús principales
        if (isSubmenu) {
            mainFilters.forEach(el => el.classList.add('hidden'));
            subFilters.forEach(el => {
                el.classList.add('hidden');
                el.classList.remove('active');
            });

            let activeSubBtn = null;
            if (category === 'bebidas') {
                subBebidas.forEach(el => el.classList.remove('hidden'));
                filterItems(['bebidas']);
                activeSubBtn = document.querySelector('.sub-bebidas[data-filter-category="bebidas"]');
            } else if (category === 'comidas') {
                subComidas.forEach(el => el.classList.remove('hidden'));
                filterItems(['comidas']);
                activeSubBtn = document.querySelector('.sub-comidas[data-filter-category="comidas"]');
            } else if (category === 'desayuno') {
                subDesayuno.forEach(el => el.classList.remove('hidden'));
                filterItems(['desayuno']);
                activeSubBtn = document.querySelector('.sub-desayuno[data-filter-category="desayuno"]');
            } else if (category === 'pasteleria') {
                subPasteleria.forEach(el => el.classList.remove('hidden'));
                filterItems(['pasteleria']);
                activeSubBtn = document.querySelector('.sub-pasteleria[data-filter-category="pasteleria"]');
            }

            if (activeSubBtn) {
                activeSubBtn.classList.add('active');
                if (activeSubBtn.scrollIntoView) {
                    activeSubBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
                }
            }
            return;
        }

        // Volver al nivel principal
        if (category === 'back') {
            subFilters.forEach(el => {
                el.classList.add('hidden');
                el.classList.remove('active');
            });
            mainFilters.forEach(el => el.classList.remove('hidden'));
            filterItems(['all']);
            document.querySelectorAll('.filter-pill').forEach(btn => btn.classList.remove('active'));
            const allBtn = document.querySelector('.filter-pill[data-filter-category="all"]');
            if (allBtn) {
                allBtn.classList.add('active');
                if (allBtn.scrollIntoView) {
                    allBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
                }
            }
            return;
        }

        // Estado visual activo
        document.querySelectorAll('.filter-pill').forEach(btn => btn.classList.remove('active'));
        if (clickedBtn) {
            clickedBtn.classList.add('active');
            if (clickedBtn.scrollIntoView) {
                clickedBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
            }
        }

        // Filtrado real
        if (category === 'all') {
            allItems.forEach(item => item.classList.remove('hidden'));
        } else {
            filterItems([category]);
        }
    }

    // ─── 6. Estado y Panel de Pedidos (Cálculos Numéricos en Memoria) ─────────
    let currentOrder = [];
    let currentlySelectingProduct = null;
    let currentlySelectingOptions = [];

    function saveOrder() {
        try {
            localStorage.setItem('mariapaula_order', JSON.stringify(currentOrder));
        } catch (e) {
            console.warn('No se pudo guardar el pedido en localStorage', e);
        }
    }

    function updateBadge() {
        const badge = document.getElementById('orderBadge');
        if (!badge) return;

        const totalItems = Array.isArray(currentOrder)
            ? currentOrder.reduce((acc, item) => acc + (parseInt(item.qty, 10) || 0), 0)
            : 0;

        if (totalItems > 0) {
            badge.textContent = totalItems;
            badge.classList.remove('hidden');
        } else {
            badge.textContent = '0';
            badge.classList.add('hidden');
        }
    }

    function renderOrder() {
        const container = document.getElementById('orderItemsContainer');
        const totalEl   = document.getElementById('orderTotal');
        if (!container || !totalEl) return;

        container.innerHTML = '';
        let total = 0;

        if (!currentOrder || currentOrder.length === 0) {
            container.innerHTML = '<div class="empty-state">Tu pedido está vacío.<br>¡Agrega algo delicioso!</div>';
            totalEl.textContent = '$0';
            return;
        }

        currentOrder.forEach(item => {
            const itemQty   = Math.max(1, parseInt(item.qty, 10) || 1);
            const itemPrice = Math.max(0, Number(item.price) || 0);
            const subtotal  = itemPrice * itemQty;
            total += subtotal;

            const itemEl = document.createElement('div');
            itemEl.className = 'order-item';
            itemEl.innerHTML = `
                <div class="item-details">
                    <div class="order-item-header">
                        <span class="item-name">${item.name}</span>
                        <button class="btn-remove" data-action="remove-from-order" data-item-id="${item.id}" aria-label="Eliminar ${item.name}">
                            <span class="material-icons" aria-hidden="true">delete</span>
                        </button>
                    </div>
                    <div class="order-item-body">
                        <span class="item-price">$${subtotal.toLocaleString('es-AR')}</span>
                        <div class="qty-controls">
                            <button class="qty-btn" data-action="update-quantity" data-item-id="${item.id}" data-delta="-1" aria-label="Restar cantidad">-</button>
                            <span class="qty-value">${itemQty}</span>
                            <button class="qty-btn" data-action="update-quantity" data-item-id="${item.id}" data-delta="1" aria-label="Sumar cantidad">+</button>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(itemEl);
        });

        totalEl.textContent = '$' + total.toLocaleString('es-AR');
    }

    function loadOrder() {
        try {
            const saved = localStorage.getItem('mariapaula_order');
            if (saved) {
                const parsed = JSON.parse(saved);
                if (Array.isArray(parsed)) {
                    currentOrder = parsed.map(item => ({
                        id: String(item.id || ('item_' + Date.now())),
                        name: String(item.name || '').trim(),
                        price: Math.max(0, Number(item.price) || 0),
                        displayPrice: String(item.displayPrice || `$${(Number(item.price) || 0).toLocaleString('es-AR')}`),
                        qty: Math.max(1, parseInt(item.qty, 10) || 1)
                    }));
                } else {
                    currentOrder = [];
                }
            } else {
                currentOrder = [];
            }
        } catch (e) {
            console.error('Error cargando pedido desde localStorage', e);
            currentOrder = [];
        }
        renderOrder();
        updateBadge();
    }

    function addToOrder(name, price, displayPrice) {
        const numPrice = Math.max(0, Number(price) || 0);
        const sanitizedName = String(name || '').trim();

        const existingItem = currentOrder.find(item => item.name === sanitizedName);
        if (existingItem) {
            existingItem.qty = (parseInt(existingItem.qty, 10) || 0) + 1;
        } else {
            currentOrder.push({
                id: 'item_' + Date.now() + '_' + Math.floor(Math.random() * 1000000),
                name: sanitizedName,
                price: numPrice,
                displayPrice: displayPrice || `$${numPrice.toLocaleString('es-AR')}`,
                qty: 1
            });
        }

        renderOrder();
        showToast('¡Agregado al pedido!', 2000, 'success');
        updateBadge();
        saveOrder();
    }

    function removeFromOrder(id) {
        currentOrder = currentOrder.filter(item => String(item.id) !== String(id));
        renderOrder();
        updateBadge();
        saveOrder();
    }

    function updateQuantity(id, delta) {
        const deltaNum = parseInt(delta, 10) || 0;
        const item = currentOrder.find(item => String(item.id) === String(id));
        if (item) {
            item.qty = (parseInt(item.qty, 10) || 0) + deltaNum;
            if (item.qty <= 0) {
                removeFromOrder(id);
            } else {
                renderOrder();
                updateBadge();
                saveOrder();
            }
        }
    }

    function toggleOrderPanel() {
        const panel = document.getElementById('orderPanel');
        if (!panel) return;
        const fab = document.querySelector('.fab-order');
        const isOpen = panel.classList.toggle('open');
        if (fab) fab.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        updateBadge();

        if (isOpen) {
            closeMenu();
        }
    }

    // ─── 7. Modal de Opciones del Menú ──────────────────────────────────────
    function openOptionsModal(name, optionsData) {
        currentlySelectingProduct = name;
        currentlySelectingOptions = optionsData;

        const titleEl = document.getElementById('modalProductTitle');
        if (titleEl) titleEl.textContent = name;

        const container = document.getElementById('modalOptionsContainer');
        if (!container) return;
        container.innerHTML = '';

        optionsData.forEach((opt, index) => {
            const label = document.createElement('label');
            const radioId = `product-opt-${index}`;
            label.htmlFor = radioId;
            label.className = 'option-label' + (index === 0 ? ' selected' : '');
            label.innerHTML = `
                <div class="option-info">
                    <span class="option-name">${opt.name}</span>
                </div>
                <span class="option-price">$${Number(opt.price || 0).toLocaleString('es-AR')}</span>
                <input type="radio" id="${radioId}" name="productOption" value="${index}" ${index === 0 ? 'checked' : ''} aria-label="${opt.name} - $${Number(opt.price || 0).toLocaleString('es-AR')}">
            `;
            container.appendChild(label);
        });

        const modal = document.getElementById('optionsModal');
        if (modal) modal.classList.add('active');
    }

    function updateSelectedOption(radioInput) {
        document.querySelectorAll('.option-label').forEach(lbl => lbl.classList.remove('selected'));
        const parentLabel = radioInput.closest('.option-label');
        if (parentLabel) parentLabel.classList.add('selected');
    }

    function closeOptionsModal() {
        const modal = document.getElementById('optionsModal');
        if (modal) modal.classList.remove('active');
        currentlySelectingProduct = null;
        currentlySelectingOptions = [];
    }

    function confirmOptionsSelection() {
        const selectedRadio = document.querySelector('input[name="productOption"]:checked');
        if (selectedRadio && currentlySelectingOptions.length > 0) {
            const optIndex = parseInt(selectedRadio.value, 10);
            const selectedOption = currentlySelectingOptions[optIndex];
            if (!selectedOption) return;

            const finalName = currentlySelectingOptions.length > 1 && selectedOption.name !== 'Única'
                ? `${currentlySelectingProduct} (${selectedOption.name})`
                : currentlySelectingProduct;

            const numPrice = Number(selectedOption.price) || 0;
            addToOrder(finalName, numPrice, selectedOption.displayPrice || `$${numPrice.toLocaleString('es-AR')}`);
            closeOptionsModal();
        }
    }

    function handleCardAddClick(btn) {
        const card = btn.closest('.menu-card-rich');
        if (!card) return;

        const titleEl = card.querySelector('.card-title');
        const name = titleEl ? titleEl.textContent.trim() : 'Producto';
        const optionsAttr = btn.getAttribute('data-options');

        if (!optionsAttr) {
            showToast('Error: Este producto no tiene opciones configuradas.', 3000, 'error');
            return;
        }

        try {
            let parsedAttr = optionsAttr;
            if (parsedAttr.includes('&quot;')) {
                parsedAttr = parsedAttr.replace(/&quot;/g, '"');
            }
            const optionsData = JSON.parse(parsedAttr);

            if (optionsData && optionsData.length > 1) {
                openOptionsModal(name, optionsData);
            } else if (optionsData && optionsData.length === 1) {
                const opt = optionsData[0];
                const numPrice = Number(opt.price) || 0;
                addToOrder(name, numPrice, opt.displayPrice);
            } else {
                showToast('El producto no tiene precio cargado.', 3000, 'error');
            }
        } catch (err) {
            console.error('Error parsing product options:', err, optionsAttr);
            showToast('Ocurrió un error al leer las opciones del producto.', 3000, 'error');
        }
    }

    // ─── 8. DELEGACIÓN GLOBAL DE EVENTOS (document.addEventListener) ────────
    // Clics interactivos en todo el documento
    document.addEventListener('click', function (e) {
        // 1. Botón Hamburguesa
        const hamburgerBtn = e.target.closest('#hamburger-btn');
        if (hamburgerBtn) {
            toggleMenu();
            return;
        }

        // 2. Cerrar menú móvil desde botón 'X'
        const navCloseBtn = e.target.closest('#mobile-nav-close');
        if (navCloseBtn) {
            closeMenu();
            return;
        }

        // 3. Cerrar menú móvil al tocar el fondo oscurecido (Overlay)
        const overlay = e.target.closest('#nav-overlay');
        if (overlay) {
            closeMenu();
            return;
        }

        // 4. Enlaces del menú móvil (que no sean acordeones)
        const mobileLink = e.target.closest('#mobile-nav .mobile-nav-link:not(.accordion-toggle)');
        if (mobileLink) {
            closeMenu();
            return;
        }

        // 5. Botones de Acordeón en Drawer Móvil
        const accordionToggle = e.target.closest('.accordion-toggle');
        if (accordionToggle) {
            e.preventDefault();
            const parent = accordionToggle.closest('.mobile-dropdown');
            if (!parent) return;
            const isOpen = parent.classList.contains('accordion-open');

            document.querySelectorAll('.mobile-dropdown.accordion-open').forEach(openItem => {
                openItem.classList.remove('accordion-open');
                const toggleBtn = openItem.querySelector('.accordion-toggle');
                if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
            });

            if (!isOpen) {
                parent.classList.add('accordion-open');
                accordionToggle.setAttribute('aria-expanded', 'true');
            } else {
                accordionToggle.setAttribute('aria-expanded', 'false');
            }
            return;
        }

        // 6. Facade de Videos (Carga bajo demanda)
        const videoFacade = e.target.closest('.video-facade');
        if (videoFacade) {
            activateVideo(videoFacade);
            return;
        }

        // 7. Filtros de la Carta (Pills)
        const filterBtn = e.target.closest('.filter-pill[data-filter-category]');
        if (filterBtn) {
            const cat = filterBtn.getAttribute('data-filter-category');
            const isSub = filterBtn.getAttribute('data-filter-is-sub') === 'true';
            filterMenu(cat, isSub, filterBtn);
            return;
        }

        // 8. Apertura / Cierre del Panel de Pedido
        const orderToggleBtn = e.target.closest('[data-action="toggle-order"]');
        if (orderToggleBtn) {
            toggleOrderPanel();
            return;
        }

        // 9. Cierre del Modal de Opciones
        const modalCloseBtn = e.target.closest('[data-action="close-options-modal"]');
        if (modalCloseBtn) {
            closeOptionsModal();
            return;
        }

        // 10. Confirmación de Selección en Modal de Opciones
        const confirmBtn = e.target.closest('[data-action="confirm-options"]');
        if (confirmBtn) {
            confirmOptionsSelection();
            return;
        }

        // 11. Botón de Añadir Producto desde Tarjeta
        const addCardBtn = e.target.closest('.btn-icon-only[data-options]');
        if (addCardBtn) {
            handleCardAddClick(addCardBtn);
            return;
        }

        // 12. Eliminar Producto del Carrito
        const removeBtn = e.target.closest('[data-action="remove-from-order"]');
        if (removeBtn) {
            const itemId = removeBtn.getAttribute('data-item-id');
            if (itemId) removeFromOrder(itemId);
            return;
        }

        // 13. Modificar Cantidad en el Carrito (+ / -)
        const qtyBtn = e.target.closest('[data-action="update-quantity"]');
        if (qtyBtn) {
            const itemId = qtyBtn.getAttribute('data-item-id');
            const delta  = parseInt(qtyBtn.getAttribute('data-delta'), 10) || 0;
            if (itemId && delta) updateQuantity(itemId, delta);
            return;
        }
    });

    // Delegación de Evento 'change' (Inputs y Checkboxes)
    document.addEventListener('change', function (e) {
        // Radio button de selección en Modal de Opciones
        const radio = e.target.closest('input[name="productOption"]');
        if (radio) {
            updateSelectedOption(radio);
            return;
        }

        // Bloqueo de scroll para Modal de Carta CSS (.modal-toggle)
        const modalToggle = e.target.closest('.modal-toggle');
        if (modalToggle) {
            if (modalToggle.checked) {
                document.body.classList.add('no-scroll');
            } else {
                document.body.classList.remove('no-scroll');
            }
            return;
        }
    });

    // Cierre mediante Teclado (Tecla Escape y Facade Enter/Espacio)
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeMenu();
            closeOptionsModal();
            const orderPanel = document.getElementById('orderPanel');
            if (orderPanel && orderPanel.classList.contains('open')) {
                toggleOrderPanel();
            }
            document.querySelectorAll('.modal-toggle:checked').forEach(t => {
                t.checked = false;
                document.body.classList.remove('no-scroll');
            });
            return;
        }

        if (e.key === 'Enter' || e.key === ' ') {
            const activeFacade = document.activeElement ? document.activeElement.closest('.video-facade') : null;
            if (activeFacade) {
                e.preventDefault();
                activateVideo(activeFacade);
            }
        }
    });

    // ─── 9. MANEJO ASÍNCRONO DE FORMULARIOS FETCH (submit) ───────────────────
    document.addEventListener('submit', async function (e) {
        const form = e.target.closest('form');
        if (!form) return;

        // Interceptar submit nativo deteniendo la recarga
        e.preventDefault();

        // Localizar botón de envío y deshabilitar con feedback
        const submitBtn = form.querySelector('button[type="submit"]') || form.querySelector('button');
        const origText  = submitBtn ? submitBtn.innerHTML : 'ENVIAR';

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = 'Enviando...';
        }

        try {
            // Extraer datos del formulario en FormData y convertir a JSON
            const formData = new FormData(form);
            const dataObject = Object.fromEntries(formData.entries());

            // Si es el formulario de contacto y el usuario desea envío a WhatsApp como respaldo
            if (form.id === 'contacto-form') {
                const nombre   = (dataObject.nombre || '').trim();
                const apellido = (dataObject.apellido || '').trim();
                const motivo   = (dataObject.motivo || '').trim();
                const mensaje  = (dataObject.mensaje || '').trim();

                const textoMensaje = `Hola, escribo desde la web MariaPaulaConfiteria.com.\n\n*Nombre:* ${nombre} ${apellido}\n*Motivo:* ${motivo}\n*Mensaje:*\n${mensaje}`;
                const urlWhatsApp  = `https://wa.me/5491135433031?text=${encodeURIComponent(textoMensaje)}`;
                
                // Intento de envío a endpoint JSON asíncrono
                let responseOk = true;
                try {
                    const endpoint = form.getAttribute('action') || '/api/contacto';
                    const response = await fetch(endpoint, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        },
                        body: JSON.stringify(dataObject)
                    });
                    if (!response.ok && response.status !== 404 && response.status !== 405) {
                        responseOk = false;
                    }
                } catch (netErr) {
                    // Servidor estático / entorno local sin backend
                    console.info('Envío asíncrono registrado en entorno estático:', dataObject);
                }

                if (responseOk) {
                    // Mostrar aviso flotante interactivo por 5 segundos
                    showToast('¡Consulta enviada con éxito! Nos comunicaremos a la brevedad.', 5000, 'success');
                    // Resetear formulario
                    form.reset();
                    // Opcionalmente abrir WhatsApp en ventana secundaria sin interrumpir la página
                    try {
                        window.open(urlWhatsApp, '_blank');
                    } catch (_) {}
                } else {
                    showToast('Hubo un error al procesar el mensaje. Por favor intente nuevamente.', 5000, 'error');
                }
            } else {
                // Formularios genéricos
                const endpoint = form.getAttribute('action') || window.location.href;
                await fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(dataObject)
                }).catch(() => ({ ok: true }));

                showToast('¡Formulario enviado con éxito!', 5000, 'success');
                form.reset();
            }
        } catch (err) {
            console.error('Error en el envío asíncrono del formulario:', err);
            showToast('Ocurrió un error inesperado al procesar su solicitud.', 5000, 'error');
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = origText;
            }
        }
    });

    // ─── 10. Adaptabilidad en Resize y Protocolo Local ──────────────────────
    window.addEventListener('resize', function () {
        if (window.innerWidth > 1024) {
            closeMenu();
        }
    });

    function initFileProtocolCompatibility() {
        if (window.location.protocol === 'file:') {
            document.querySelectorAll('a[href^="/"]').forEach(link => {
                const href = link.getAttribute('href');
                let target = resolvePath(href);
                if (target.endsWith('/')) {
                    target += 'index.html';
                }
                link.setAttribute('href', target);
            });

            document.querySelectorAll('img[src^="/"], video[src^="/"], source[src^="/"]').forEach(media => {
                const src = media.getAttribute('src');
                media.setAttribute('src', resolvePath(src));
            });
        }
    }

    // ─── 11. Inicialización en Carga Defer ───────────────────────────────────
    function init() {
        initFileProtocolCompatibility();
        if (document.getElementById('orderItemsContainer') || document.getElementById('orderBadge')) {
            loadOrder();
            updateBadge();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
