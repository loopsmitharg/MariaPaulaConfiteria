import re

with open('menu/index.html', encoding='utf-8') as f:
    text = f.read()

cards = re.findall(r'<div class="menu-card-rich\s+([^"]+)"', text)
main_cats = {'category-comidas', 'category-desayuno', 'category-pasteleria', 'category-bebidas', 'category-bebidas-calientes', 'category-bebidas-frias'}

for i, c in enumerate(cards):
    classes = set(c.split())
    has_main = any(mc in classes for mc in main_cats)
    if not has_main:
        print(f"Card {i} has NO main category: {classes}")
