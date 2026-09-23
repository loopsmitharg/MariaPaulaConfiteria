import re
from collections import Counter

with open('menu/index.html', encoding='utf-8') as f:
    text = f.read()

cards = re.findall(r'class="menu-card-rich\s+([^"]+)"', text)
counts = Counter()
for c in cards:
    for cat in c.split():
        if cat.startswith('category-'):
            counts[cat] += 1

print("--- CATEGORY COUNTS ---")
for k, v in sorted(counts.items()):
    print(f"{k}: {v} cards")
