
import os

# Read generated items
with open("c:/git/MariaPaulaConfiteria/menu_items.html", "r", encoding="utf-8") as f:
    new_items_html = f.read()

# Read Menu.html
with open("c:/git/MariaPaulaConfiteria/views/Menu.html", "r", encoding="utf-8") as f:
    menu_html = f.read()

# 1. Update Filters with ALL Submenus
new_filters = """
        <div class="filter-sticky-container">
            <div class="filter-pills">
                <!-- Main Filters -->
                <button class="filter-pill main-filter active" onclick="filterMenu('all')">Todos</button>
                <button class="filter-pill main-filter" onclick="filterMenu('comidas', true)">🍽️ Comidas</button>
                <button class="filter-pill main-filter" onclick="filterMenu('desayuno', true)">☕🥐 Desayuno</button>
                <button class="filter-pill main-filter" onclick="filterMenu('pasteleria', true)">🍰 Pastelería</button>
                <button class="filter-pill main-filter" onclick="filterMenu('bebidas', true)">🥤 Bebidas</button>
                
                <!-- Submenu Bebidas -->
                <button class="filter-pill sub-filter sub-bebidas hidden" onclick="filterMenu('back')">⬅️ Volver</button>
                <button class="filter-pill sub-filter sub-bebidas hidden" onclick="filterMenu('bebidas-calientes')">☕ Calientes</button>
                <button class="filter-pill sub-filter sub-bebidas hidden" onclick="filterMenu('bebidas-frias')">❄️ Frías</button>
                <button class="filter-pill sub-filter sub-bebidas hidden" onclick="filterMenu('bebidas-gaseosas')">🥤 Gaseosas</button>

                <!-- Submenu Comidas -->
                <button class="filter-pill sub-filter sub-comidas hidden" onclick="filterMenu('back')">⬅️ Volver</button>
                <button class="filter-pill sub-filter sub-comidas hidden" onclick="filterMenu('burgers')">🍔 Burgers</button>
                <button class="filter-pill sub-filter sub-comidas hidden" onclick="filterMenu('pastas')">🍝 Pastas</button>
                <button class="filter-pill sub-filter sub-comidas hidden" onclick="filterMenu('pizzas')">🍕 Pizzas</button>
                <button class="filter-pill sub-filter sub-comidas hidden" onclick="filterMenu('entradas')">🍢 Entradas</button>
                <button class="filter-pill sub-filter sub-comidas hidden" onclick="filterMenu('principales')">🥘 Principales</button>
                <button class="filter-pill sub-filter sub-comidas hidden" onclick="filterMenu('grilladas')">🍖 Grill</button>
                <button class="filter-pill sub-filter sub-comidas hidden" onclick="filterMenu('milanesas')">🍽️ Milanesas</button>
                <button class="filter-pill sub-filter sub-comidas hidden" onclick="filterMenu('ensaladas')">🥗 Ensaladas</button>

                <!-- Submenu Desayuno -->
                <button class="filter-pill sub-filter sub-desayuno hidden" onclick="filterMenu('back')">⬅️ Volver</button>
                <button class="filter-pill sub-filter sub-desayuno hidden" onclick="filterMenu('combos')">🥐 Combos</button>
                <button class="filter-pill sub-filter sub-desayuno hidden" onclick="filterMenu('tostados')">🥪 Tostados</button>
                <button class="filter-pill sub-filter sub-desayuno hidden" onclick="filterMenu('promos')">🏷️ Promos</button>

                <!-- Submenu Pastelería -->
                <button class="filter-pill sub-filter sub-pasteleria hidden" onclick="filterMenu('back')">⬅️ Volver</button>
                <button class="filter-pill sub-filter sub-pasteleria hidden" onclick="filterMenu('tortas')">🍰 Tortas y Dulces</button>
                <button class="filter-pill sub-filter sub-pasteleria hidden" onclick="filterMenu('adicionales')">🧀 Adicionales</button>
            </div>
        </div>
"""

# Replace the existing filter container
start_marker = '<div class="filter-sticky-container">'
end_marker = '<div class="masonry-grid">'

start_idx = menu_html.find(start_marker)
end_idx = menu_html.find(end_marker)

if start_idx != -1 and end_idx != -1:
    pre_grid = menu_html[:start_idx]
    post_grid_start = menu_html[end_idx:] 
    
    # 2. Update Grid Content
    main_end_idx = post_grid_start.find('</main>')
    grid_content_end = post_grid_start.rfind('</div>', 0, main_end_idx)

    if grid_content_end != -1:
        new_grid = '<div class="masonry-grid">\n' + new_items_html + '\n        </div>\n    '
        rest_of_file = post_grid_start[main_end_idx:] 
        final_html = pre_grid + new_filters + new_grid + rest_of_file
else:
    print("Could not find filters")
    exit(1)

# 3. Update Script
new_script = """
    <script>
        function filterMenu(category, isSubmenu = false) {
            const allItems = document.querySelectorAll('.menu-card-rich');
            const mainFilters = document.querySelectorAll('.main-filter');
            const subFilters = document.querySelectorAll('.sub-filter');
            
            const subBebidas = document.querySelectorAll('.sub-bebidas');
            const subComidas = document.querySelectorAll('.sub-comidas');
            const subDesayuno = document.querySelectorAll('.sub-desayuno');
            const subPasteleria = document.querySelectorAll('.sub-pasteleria');
            
            // Scroll to top of filters
            const filterContainer = document.querySelector('.filter-sticky-container');
            if(filterContainer) {
                window.scrollTo({
                    top: filterContainer.offsetTop - 100,
                    behavior: 'smooth'
                });
            }

            // --- Submenu Logic ---
            if (isSubmenu) {
                mainFilters.forEach(el => el.classList.add('hidden'));
                subFilters.forEach(el => el.classList.add('hidden')); // Hide all subs first

                if (category === 'bebidas') {
                    subBebidas.forEach(el => el.classList.remove('hidden')); 
                    filterItems(['bebidas-calientes', 'bebidas-frias', 'bebidas-gaseosas']);
                } else if (category === 'comidas') {
                    subComidas.forEach(el => el.classList.remove('hidden'));
                    filterItems(['comidas']); 
                } else if (category === 'desayuno') {
                    subDesayuno.forEach(el => el.classList.remove('hidden'));
                    filterItems(['desayuno']); 
                } else if (category === 'pasteleria') {
                    subPasteleria.forEach(el => el.classList.remove('hidden'));
                    filterItems(['pasteleria']); 
                }
                return;
            }
            
            // --- Back Logic ---
            if (category === 'back') {
                subFilters.forEach(el => el.classList.add('hidden'));
                mainFilters.forEach(el => el.classList.remove('hidden'));
                
                filterMenu('all');
                document.querySelector("button[onclick*='all']").classList.add('active');
                return;
            }

            // --- Visual Active State ---
            document.querySelectorAll('.filter-pill').forEach(btn => btn.classList.remove('active'));
            const clickedBtn = event.target; 
            if (clickedBtn) clickedBtn.classList.add('active');
            
            // --- Actual Filtering ---
            if (category === 'all') {
                allItems.forEach(item => item.classList.remove('hidden'));
            } else {
                filterItems([category]);
            }
        }

        function filterItems(categories) {
            const allItems = document.querySelectorAll('.menu-card-rich');
            allItems.forEach(item => {
                let match = false;
                categories.forEach(cat => {
                    // Check if item has the specific category class
                    // We check for 'category-' + cat. 
                    // Note: 'comidas' class is present on all food, but we also have 'category-burgers' etc.
                    if (item.classList.contains('category-' + cat)) match = true;
                });
                
                if (match) item.classList.remove('hidden');
                else item.classList.add('hidden');
            });
        }
    </script>
"""

# Replace script
script_start = final_html.find('<script>')
script_end = final_html.find('</script>') + 9
if script_start != -1:
    final_html = final_html[:script_start] + new_script + final_html[script_end:]

with open("c:/git/MariaPaulaConfiteria/views/Menu.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Menu.html updated successfully")
