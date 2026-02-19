
import re
import os

menu_text = """
Burger y sandwich (con papas o batatas fritas)
Burger clásica (hamburguesa casera, cheddar, lechuga y tomate) — $16.500
Burger María Paula (casera, cheddar, bacon crocante, lechuga, tomate y huevo a la plancha) — $19.500
Doble burger (doble carne, cheddar y bacon crocante) — $19.500
Sandwich (carne braseada desmenuzada, queso derretido; aderezo opcional Bdq) — $18.500
Sandwich (pollo frito, bacon crocante, tomate y queso) — $18.500
Sandwich (rúcula, jamón crudo, tomates asados, queso crema) — $18.500
Sandwich clásico (jamón cocido, queso, lechuga y tomate) — $12.500

Pastas
Fetuccinis — $11.500
Ñoquis — $13.500
Sorrentinos — $14.000
Canelones — $14.500
Lasagna — $17.500
Ravioles (JyQ o RyV) — $13.000

Salsas
Bolognesa — $5.200
Estofado — $5.600
Alfredo (crema, jamón y parmesano) — $4.800
Alfredo con tiras de pollo grillado — $5.200

Pizzas (Individual / Grande)
Muzzarella — $14.000 / $19.000
Jamón y muzzarella — $15.000 / $26.500
Napolitana — $16.500 / $27.000
Fugazza — $13.000 / $18.000
Fugazzeta con muzzarella — $16.000 / $21.000
Roquefort — $18.000 / $28.000
Italiana — $18.500 / $26.000

Entradas
Bastones de muzzarella con salsa de tomate — $10.500
Finger de pollo (sal Bdq + salsa miel y mostaza) — $15.000
Nachos con 3 aderezos (guacamole, picante y cheddar) — $10.500
Papas fritas con cheddar, panceta y verdeo — $12.000
Dúo de empanadas (jyq / carne / verdura + salsa de tomates) — $6.500
Tortilla de papas (individual) — $9.200

Principales
Lomo (dos medallones envueltos en panceta) — $28.000
Puré rústico de papas y rúcula con parmesano — $9.500
Rondiola (a la cerveza, con Bdq + puré de batatas) — $19.000
Yamani al wok (arroz yamani, verduras al wok y soja) — $15.500
Pesca del día (grillada con vegetales salteados y puré de papas) — $20.500
Milanesa María Paula (ternera con cheddar, panceta y verdeo + fritas) — $25.000

Grilladas (con guarnición: ensalada, puré o fritas)
Bife de chorizo — $26.000
Bife de lomo — $24.000
Bife de costilla — $18.500
Costillitas de cerdo — $18.000
Pollo grillé — $17.000

Milanesas (con ensalada, puré o fritas)
Milanesa de ternera — $20.500
Milanesa de pollo — $19.500
Milanesa de ternera napolitana — $24.000
Milanesa de pollo napolitana — $23.000

Acompañamientos
Papas fritas — $9.000
Papas fritas c/ cheddar y bacon — $12.000
Batatas fritas — $9.000
Puré de papas — $7.500
Puré de batatas — $5.300
Puré de calabaza — $4.500
Ensalada verde — $9.500
Arroz blanco — $7.000

Ensaladas
César (lechuga, aderezo césar, parmesano y croutons) — $16.000
César con pollo — $16.800
César con lagostino — $17.500
Tuna salad (mix verdes, zanahoria, huevo, choclo, atún y cherry) — $17.500
Veggie salad (arroz yamani, calabaza, palta, choclo, tomate y semillas) — $17.000
Mediterránea (rúcula, lechuga, muzzarella, jamón crudo, cebolla morada, cherry y aceitunas negras) — $18.000
Ensalada 3 ingredientes a elección — $10.500

Cafetería
Cafés (Pocillo / Jarrito / Doble)
Café — $3.800 / $4.200 / $4.800
Café con crema — (Jarrito) $4.800 / (Doble) $5.200
Cortado — $3.800 / $4.200 / $4.800
Lágrima — (Jarrito) $4.200 / (Doble) $5.200
Descafeinado — (Doble) $4.800
Café con leche
Doble — $4.500
XL — $5.900

Capuchinos
Capuchino (Chico / Grande) — $4.500 / $5.200
Capuchino italiano (Chico / Grande) — $4.900 / $5.900

Otras bebidas calientes
Café especial — $9.500
Submarino — $4.800
Chocolatada — $4.500
Vaso de leche — $1.900
Té / mate cocido — $3.800
Té / mate cocido con leche — $4.100
Té saborizado — $4.100

Adicionales
Queso crema — $1.200
Mermelada / Dulce de leche — $1.200
Tostadas — $1.000
Facturas — $1.200
Libritos — $700
Chipá — $800
Jarrito de leche — $1.200
Crema — $1.200
Plato de frutas — $5.900
Masas finas y secas (x unid) — $1.300
Galletitas (6 unid) — $5.500

Promociones (cafetería)
Café con leche + 2 facturas — $5.900
Café con leche + 3 facturas — $6.500
Café con leche + medio tostado — $8.200

Mañanas y tardes (combos)
2 tostadas + mermelada + queso blanco + café c/leche + exprimido chico — $10.500
Tazón yogurt/granola/frutas + 2 tostadas + queso blanco + mermelada + exprimido chico — $15.500
Brunch (tostada con huevos revueltos y bacon) + café + exprimido chico — $15.500
Brunch para dos (2 tostadas + 2 medialunas jyq + mix frutas + 2 cafés + 2 exprimidos chicos) — $36.500
María Paula (2 infusiones + porción torta + 2 scons + 2 muffins + masas + 2 de miga + 2 exprimidos chicos) — $45.000
Tostado jyq (2 sandwich) + limonada menta/jengibre (vaso) — $15.000
Waffle (ddl o crema y frutos rojos) + milk shake (a elección) — $17.000

Sandwich
Triple tradicional — $2.600
Triple especial — $3.210
Pan a elección jamón y queso — $9.800
Pan a elección crudo y queso — $13.500
Pan a elección salame y queso — $9.800
Tostados en pan de miga — $8.200
Medio tostado en pan de miga — $4.600
Tostados en pan de molde / pan árabe
Crudo, queso y tomate — $14.200
Jamón cocido, queso y tomate — $9.800
Cheddar, panceta y huevo a la plancha — $14.200

Recargo
Huevo — $900
Tomate — $800
Crudo — $1.600
Jamón cocido — $1.300
Palmitos — $1.600

Bakery / Pastelería
Apple crumble — $8.200
Cheesecake con frutos rojos — $8.500
Lemon pie — $8.200
Selva negra — $8.200
Oreo torta — $8.200
Chocotorta — $8.200
Torta brownie — $8.900
Rogel — $8.200
Tiramisu — $8.200
Brownie — $8.500
Pastafrola con membrillo — $6.500
Torta de ricota — $8.200
Alfajor cordobés — $4.200
Alfajor de chocolate — $4.800
Alfajor de maicena — $4.200
Alfajor de coco — $4.800
Macarrón — $3.500
Muffin’s — $4.600
Pastelitos — $2.400
Facturas / medialunas — $1.200
Budín — $5.200

Bebidas (frías)
Limonada menta y jengibre (Jarra) — $13.500
Limonada menta y jengibre (Vaso) — $4.200
Pomelada (vaso) Chico/Grande — $4.600 / $8.500
Exprimido de naranja (vaso) Chico/Grande — $4.600 / $8.500

Gaseosas y Agua
Gaseosa línea Coca Cola 500 ml — $3.900
Agua saborizada 500 ml — $3.000
Agua con o sin gas 500 ml — $3.000

Licuados
Licuados al agua (Ananá/Durazno) — $9.500
Licuados al agua (Otras frutas) — $9.000
Licuados de leche (Ananá/Durazno) — $10.000
Licuados de leche (Otras frutas) — $9.500

Milk shake
Americana con Oreo — $8.900
Frutilla — $8.900
Choco — $8.900
Dulce de leche — $8.900
Chocotorta (helado de americana + ddl artesanal + chocolinas) — $8.900

Promos 
Milkshake + Waffle — $17.000
2 licuados (al agua) + tostado — $22.000
Exprimido grande + tostado queso y huevo — $10.500
6 triples + 1 jarra (limonada/pomelada) — $27.900
2 croissants jyq + 1 jarra (limonada/pomelada) — $26.000
Jarra (limonada/pomelada) + tostado — $25.000
"""

html_output = ""
current_main_category = "comidas" # Default
current_sub_category = "burgers" # Default

# Mappings for user categories to CSS classes and Main Category
# (Header String) -> (Main Category, Sub Category)
category_map = {
    "Burger y sandwich": ("comidas", "burgers"),
    "Pastas": ("comidas", "pastas"),
    "Salsas": ("comidas", "pastas"), 
    "Pizzas": ("comidas", "pizzas"),
    "Entradas": ("comidas", "entradas"),
    "Principales": ("comidas", "principales"),
    "Grilladas": ("comidas", "grilladas"),
    "Milanesas": ("comidas", "milanesas"),
    "Acompañamientos": ("comidas", "guarniciones"),
    "Ensaladas": ("comidas", "ensaladas"),
    
    "Cafetería": ("bebidas-calientes", "cafeteria"),
    "Capuchinos": ("bebidas-calientes", "cafeteria"),
    "Otras bebidas calientes": ("bebidas-calientes", "cafeteria"),
    
    "Promociones": ("desayuno", "promos"),
    "Mañanas y tardes": ("desayuno", "combos"),
    "Sandwich": ("desayuno", "tostados"),
    "Tostados en pan de miga": ("desayuno", "tostados"),
    "Tostados en pan de molde / pan árabe": ("desayuno", "tostados"),
    "Recargo": ("comidas", "extras"),
    
    "Bakery / Pastelería": ("pasteleria", "tortas"), # Split Bakery
    "Adicionales": ("pasteleria", "adicionales"),   # Split Adicionales
    
    "Bebidas": ("bebidas-frias", "bebidas-frias"),
    "Gaseosas y Agua": ("bebidas", "bebidas-gaseosas"),
    "Licuados": ("bebidas-frias", "licuados"),
    "Milk shake": ("bebidas-frias", "licuados"),
    "Promos": ("desayuno", "promos")
}

def clean_line(line):
    return line.strip()

lines = menu_text.strip().split('\n')

for line in lines:
    line = clean_line(line)
    if not line: continue
    
    is_header = False
    
    # Heuristic for header: no ($Price)
    if "— $" not in line and " + " not in line and line.count("$") < 1:
        is_header = True
        
    if is_header:
        # It's a header
        header = line.split('(')[0].strip()
        
        # Determine categories
        if header in category_map:
            current_main_category = category_map[header][0]
            current_sub_category = category_map[header][1]
        elif "Café" in header or "Cafes" in header:
            current_main_category = "bebidas-calientes"
            current_sub_category = "cafeteria"
        
        # NO HEADER HTML GENERATED HERE - AS REQUESTED (Disordered look)
        
    else:
        # It's an item
        parts = line.split("—")
        title = parts[0].strip()
        price = parts[1].strip() if len(parts) > 1 else ""
        
        desc_text = ""
        if "(" in title and ")" in title:
             match = re.search(r'\((.*?)\)', title)
             if match:
                 if len(match.group(1)) > 3:
                     desc_text = match.group(1)
                     title = title.replace(f"({desc_text})", "").strip()

        html_output += f"""
        <div class="menu-card-rich category-{current_main_category} category-{current_sub_category}">
            <div class="card-img-container placeholder-img" style="height: 15rem; background-color: var(--white-pink); display: flex; align-items: center; justify-content: center; overflow: hidden;">
                 <img src="../images/MariaPaulaLogo.png" alt="{title}" style="opacity: 0.15; width: 60%; transform: grayscale(1);">
            </div>
            <div class="card-content">
                <div class="card-header">
                    <h3 class="card-title">{title}</h3>
                    <span class="card-price">{price}</span>
                </div>
                <p class="card-desc" style="min-height: 40px;">{desc_text}</p>
                <button class="btn-icon-only">
                    <span class="material-icons">add</span>
                </button>
            </div>
        </div>
        """

with open("c:/git/MariaPaulaConfiteria/menu_items.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("HTML Generated")
