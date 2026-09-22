import glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from html.parser import HTMLParser

class ComponentAuditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get('class', '')
        if any(term in classes for term in ['hidden', 'd-none', 'mobile-only', 'desktop-only', 'md:', 'sm:', 'lg:']):
            self.elements.append((tag, classes, attr_dict.get('id', '')))

html_files = sorted(glob.glob('**/*.html', recursive=True))
print(f"Auditing {len(html_files)} HTML files for duplicate or hidden components:")

for hf in html_files:
    if 'node_modules' in hf or '.git' in hf or 'brain' in hf:
        continue
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    auditor = ComponentAuditor()
    auditor.feed(content)
    print(f"\nFile: {hf}")
    if not auditor.elements:
        print("  OK: No hidden/duplicate visibility classes found.")
    else:
        for tag, cls, el_id in auditor.elements:
            print(f"  - <{tag} id=\"{el_id}\" class=\"{cls}\">")
