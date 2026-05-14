# Especificación Técnica: Modal "Ver Carta" + Responsive Mobile
**Extraído de:** `gastronomia.html` — Proyecto GameOver MdP  
**Propósito:** Replicar al pie de la letra en otro proyecto vía IA

---

## 🧠 Concepto Central: Modal 100% CSS (sin JavaScript para abrir/cerrar)

El modal funciona con el patrón **checkbox oculto + label como trigger**. No se usa JS para abrir ni cerrar: el estado del `<input type="checkbox">` controla la visibilidad mediante el selector CSS `:checked + .modal-overlay`.

El JS **solo se usa** para bloquear el scroll del `<body>` cuando el modal está abierto.

---

## 1. VARIABLES CSS NECESARIAS

```css
:root {
  --navy: #0f172a;
  --black: #050505;
  --gold: #d4af37;
  --white: #ffffff;
}
```

---

## 2. FUENTES REQUERIDAS (Google Fonts)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Orbitron:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
```

---

## 3. HTML — ESTRUCTURA COMPLETA

### 3a. Botón disparador (Barra Promocional)

La barra es una sección dorada **encima del contenido principal**, debajo del header fijo. El botón es un `<label>` cuyo `for` apunta al `id` del checkbox del modal.

```html
<section class="promo-bar">
    <div class="promo-content">
        <span class="promo-text">
            Nuestra carta digital
            <!-- Flecha SVG decorativa (opcional) -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                 fill="none" stroke="currentColor" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round"
                 style="margin-left: 10px; vertical-align: middle;">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
        </span>
        <!-- ESTE LABEL ABRE EL MODAL. Su "for" debe coincidir con el id del checkbox -->
        <label for="modal-menu" class="btn-menu-consult" style="display:inline-block; text-align:center;">
            CONSULTAR LA CARTA
        </label>
    </div>
</section>
```

### 3b. El Modal (checkbox + overlay)

Colocar **fuera del `<main>`**, preferentemente antes del `<footer>` o al final del `<body>`.  
El `<input>` debe ser **hermano inmediatamente anterior** al `.modal-overlay` (el selector CSS `+` lo requiere).

```html
<!-- Checkbox oculto que actúa como interruptor -->
<input type="checkbox" id="modal-menu" class="modal-toggle">

<!-- Overlay que se activa cuando el checkbox está checked -->
<div class="modal-overlay">
    <div class="modal-content" style="max-width: 600px;">
        
        <!-- Header pegajoso con botón X de cierre -->
        <div class="sticky-header">
            <!-- Este label CIERRA el modal (desmarca el checkbox) -->
            <label for="modal-menu" class="close-modal">&times;</label>
        </div>

        <!-- Cuerpo del modal (personalizable) -->
        <div class="modal-body" style="padding: 0; text-align: center;">
            <h2 style="padding: 20px; color: var(--gold); background: #111; margin: 0;">
                MENÚ
            </h2>
            
            <!-- Aquí van las imágenes de la carta (una debajo de la otra, scrolleable) -->
            <img src="menu-pagina-1.png" alt="Pagina 1" style="width: 100%; display: block; border-bottom: 2px solid #333;">
            <img src="menu-pagina-2.png" alt="Pagina 2" style="width: 100%; display: block; border-bottom: 2px solid #333;">
            <!-- ...más imágenes según sea necesario... -->

            <!-- Botón de cierre al final del scroll -->
            <div style="padding: 20px; background: #111;">
                <label for="modal-menu" class="btn-submit-gamer" style="display:block; text-align:center;">
                    CERRAR MENÚ
                </label>
            </div>
        </div>
    </div>
</div>
```

**Regla crítica de posicionamiento HTML:**  
```
<input type="checkbox" id="modal-menu" class="modal-toggle">   ← PRIMERO
<div class="modal-overlay"> ...                                 ← INMEDIATAMENTE DESPUÉS
```
Si hay cualquier elemento HTML entre ambos, el selector CSS `:checked + .modal-overlay` NO funcionará.

---

## 4. CSS — MODAL (Sección completa)

```css
/* =============================================
   MODAL CSS-PURO (Patrón checkbox + label)
   ============================================= */

/* El checkbox siempre oculto */
.modal-toggle {
  display: none;
}

/* Cuando el checkbox está marcado, muestra el overlay */
.modal-toggle:checked + .modal-overlay {
  display: flex;
  opacity: 1;
  pointer-events: auto;
}

/* Overlay de fondo: negro semitransparente + blur */
.modal-overlay {
  display: none;            /* Oculto por defecto */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.85);  /* Oscurece el fondo */
  backdrop-filter: blur(8px);             /* Difumina el fondo */
  z-index: 2000;                          /* Por encima de todo (header z-index: 1000) */
  justify-content: center;
  align-items: center;
  padding: 20px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

/* Caja del modal */
.modal-content {
  background-color: #0f0f0f;
  border: 1px solid var(--gold);          /* Borde dorado característico */
  border-radius: 12px;
  width: 100%;
  max-width: 800px;                       /* Ajustar según necesidad */
  max-height: 90vh;                       /* Nunca más alto que la pantalla */
  overflow-y: auto;                       /* Scroll interno para contenido largo */
  position: relative;
  box-shadow: 0 0 50px rgba(212, 175, 55, 0.2);  /* Halo dorado sutil */
}

/* Header pegajoso para la X (siempre visible al scrollear) */
.sticky-header {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  justify-content: flex-end;             /* X alineada a la derecha */
  padding: 10px;
  /* Degradado para que la X se vea sobre cualquier contenido */
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.8), transparent);
}

/* Botón X de cierre */
.close-modal {
  color: var(--white);
  font-size: 30px;
  font-weight: bold;
  cursor: pointer;
  background: rgba(0, 0, 0, 0.5);
  padding: 0 12px;
  border-radius: 5px;
  line-height: 1.5;
  transition: 0.3s;
}

.close-modal:hover {
  color: var(--gold);
  background: rgba(0, 0, 0, 1);
}

/* Cuerpo del modal */
.modal-body {
  padding: 30px;
  color: var(--white);
}

/* Botón de acción dentro del modal (CTA / Cerrar) */
.btn-submit-gamer {
  width: 100%;
  padding: 15px;
  background-color: var(--black);
  color: var(--white);
  border: 1px solid #333;
  font-family: "Orbitron", sans-serif;   /* Si usás Orbitron */
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: block;
}

.btn-submit-gamer:hover {
  background: var(--gold);
  color: var(--black);
  border-color: var(--gold);
}

/* Bloqueo de scroll del body cuando el modal está abierto */
body.no-scroll {
  overflow: hidden;
}

/* Responsive modal en mobile */
@media (max-width: 768px) {
  .modal-content {
    max-height: 85vh;  /* Un poco menos de espacio para que no tape la barra del navegador */
  }
}
```

---

## 5. CSS — BARRA PROMOCIONAL (Trigger de la carta)

```css
/* --- BARRA PROMOCIONAL (donde está el botón de abrir) --- */
.promo-bar {
  background-color: var(--gold);
  height: 175px;                        /* Altura fija en desktop */
  width: 100%;
  margin-top: 90px;                     /* Compensa el header fijo (ajustar al alto de tu header) */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 10%;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.promo-content {
  display: flex;
  justify-content: space-between;       /* Texto a la izq, botón a la der */
  align-items: center;
  width: 100%;
  max-width: 1200px;
}

.promo-text {
  font-family: "Playfair Display", serif;
  font-size: 2rem;
  color: var(--white);
  font-weight: bold;
  font-style: italic;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Botón que dispara el modal (es un label, no un button) */
.btn-menu-consult {
  background-color: var(--black);
  color: var(--white);
  padding: 15px 30px;
  font-family: "Orbitron", sans-serif;
  font-size: 0.9rem;
  border: 2px solid var(--black);
  cursor: pointer;
  text-transform: uppercase;
  transition: 0.3s;
  letter-spacing: 1px;
}

.btn-menu-consult:hover {
  background-color: var(--white);
  color: var(--black);
}
```

---

## 6. CSS — RESPONSIVE MOBILE (breakpoint 900px)

```css
/* Responsive para la sección de gastronomía/carta */
@media (max-width: 900px) {

  /* La barra promocional pasa de altura fija a auto */
  .promo-bar {
    height: auto;
    padding: 30px 5%;
  }

  /* El contenido de la barra se apila verticalmente */
  .promo-content {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }

  /* Los artículos (texto + imagen) también se apilan */
  /* Funciona tanto para el orden normal como para el invertido (night-focus) */
  .cookbook-article,
  .cookbook-article.night-focus {
    flex-direction: column;
    gap: 30px;
  }

  /* En mobile: imagen arriba, texto abajo (independientemente del orden desktop) */
  .article-text {
    order: 2;  /* Texto va al fondo */
  }
  .article-image {
    order: 1;  /* Imagen va arriba */
    width: 100%;
  }

  /* Las imágenes de artículo reducen su altura */
  .img-placeholder {
    height: 250px;
  }
}
```

---

## 7. JAVASCRIPT — Bloqueo de scroll

El JS es **mínimo**: solo escucha el cambio de estado del checkbox para bloquear/desbloquear el scroll del body.

```javascript
document.addEventListener("DOMContentLoaded", function() {
    
    // Bloqueo de scroll cuando el modal está abierto
    const toggles = document.querySelectorAll('.modal-toggle');
    const body = document.body;

    toggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            if (this.checked) {
                body.classList.add('no-scroll');      // Modal abierto → bloquear scroll
            } else {
                body.classList.remove('no-scroll');   // Modal cerrado → restaurar scroll
            }
        });
    });

});
```

Si la página ya tiene un archivo JS cargado, simplemente agregar este listener dentro del `DOMContentLoaded` existente.

---

## 8. CÓMO FUNCIONA — Flujo completo

```
1. Usuario hace clic en <label for="modal-menu"> (.btn-menu-consult)
      ↓
2. El <input id="modal-menu"> cambia a :checked
      ↓
3. CSS selector: .modal-toggle:checked + .modal-overlay { display: flex; opacity: 1; }
      ↓
4. El overlay aparece: fondo negro 85% opacidad + blur(8px) detrás
      ↓
5. JS detecta el 'change' del toggle → añade body.classList.add('no-scroll') → bloquea scroll
      ↓
6. El usuario cierra haciendo clic en:
   a) <label for="modal-menu" class="close-modal"> (X en el sticky-header)
   b) <label for="modal-menu" class="btn-submit-gamer"> (botón "CERRAR" al final)
      ↓
7. Ambos labels desmarcan el checkbox → CSS oculta el overlay → JS quita 'no-scroll'
```

---

## 9. NOTAS IMPORTANTES para implementación

- **El `max-width` del modal se controla inline** en el HTML: `style="max-width: 600px;"`. Cambiar según el ancho deseado.
- **El `z-index` del overlay es 2000**, por encima del header (1000). Asegurarse que nada más tenga z-index mayor.
- **La X usa `&times;`** (entidad HTML), no una imagen ni ícono externo.
- **No hay animación de entrada del modal**: la transición `opacity 0.3s` hace un fade-in suave. Si se desea slide-in, agregar `transform: translateY(-20px)` en el estado oculto y `transform: translateY(0)` en el estado activo.
- **El `.sticky-header` tiene `position: sticky; top: 0`**: esto hace que la X de cierre se quede siempre visible aunque el usuario haga scroll dentro del modal. Es clave para menus de carta que son largos.
- **El `.modal-content` tiene `overflow-y: auto`**: el scroll está dentro del modal, no en el body. El body tiene `overflow: hidden` (via `.no-scroll`) cuando el modal está abierto.
- **El `margin-top: 90px` en `.promo-bar`** corresponde al alto del header fijo (100px). Ajustar este valor según el header del proyecto destino.
