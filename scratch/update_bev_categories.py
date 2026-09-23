with open('menu/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace menu-card-rich category-bebidas-calientes to include category-bebidas
def add_category_bebidas(match):
    full = match.group(0)
    classes = match.group(1).split()
    if 'category-bebidas' not in classes:
        classes.insert(0, 'category-bebidas')
        return f'class="menu-card-rich {" ".join(classes)}"'
    return full

import re
new_content = re.sub(r'class="menu-card-rich\s+([^"]*(?:category-bebidas-calientes|category-bebidas-frias|category-bebidas-gaseosas)[^"]*)"', add_category_bebidas, content)

with open('menu/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated beverage cards in menu/index.html")
