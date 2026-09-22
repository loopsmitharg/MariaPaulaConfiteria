import glob, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')
from html.parser import HTMLParser

class A11yAuditor(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.h1_count = 0
        self.inline_styles = 0
        self.has_dist_css = False
        self.inputs_without_label = 0
        self.buttons_without_accessible_name = 0
        self.current_tag = None
        self.current_button_text = ""
        self.in_button = False
        self.button_has_aria = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        
        if tag == 'h1':
            self.h1_count += 1
            
        if 'style' in attr_dict:
            self.inline_styles += 1
            print(f"  [WARN] Inline style in <{tag}>: {attr_dict['style'][:40]}...")
            
        if tag == 'link' and attr_dict.get('rel') == 'stylesheet':
            href = attr_dict.get('href', '')
            if 'dist.css' in href:
                self.has_dist_css = True
                
        if tag == 'input' and attr_dict.get('type') not in ['hidden', 'submit', 'button']:
            has_id = bool(attr_dict.get('id'))
            has_aria = bool(attr_dict.get('aria-label') or attr_dict.get('aria-labelledby'))
            if not has_id and not has_aria:
                self.inputs_without_label += 1
                
        if tag == 'button':
            self.in_button = True
            self.current_button_text = ""
            self.button_has_aria = bool(attr_dict.get('aria-label') or attr_dict.get('aria-labelledby'))

    def handle_data(self, data):
        if self.in_button:
            self.current_button_text += data.strip()

    def handle_endtag(self, tag):
        if tag == 'button':
            if not self.button_has_aria and not self.current_button_text:
                self.buttons_without_accessible_name += 1
            self.in_button = False

html_files = sorted(glob.glob('**/*.html', recursive=True))
print(f"Auditing {len(html_files)} HTML files:")

all_passed = True
for hf in html_files:
    if 'node_modules' in hf or '.git' in hf or 'brain' in hf:
        continue
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    auditor = A11yAuditor(hf)
    auditor.feed(content)
    
    # Ignore verification page
    if 'google' in hf:
        continue
        
    status = "OK"
    issues = []
    if auditor.h1_count != 1:
        issues.append(f"h1 count = {auditor.h1_count}")
    if auditor.inline_styles > 0:
        issues.append(f"{auditor.inline_styles} inline styles")
    if not auditor.has_dist_css:
        issues.append("missing dist.css")
        
    if issues:
        all_passed = False
        print(f"❌ {hf}: {', '.join(issues)}")
    else:
        print(f"✓ {hf}: 1 H1, 0 inline styles, linked to dist.css")

print("\n--- Verifying css/dist.css tokens ---")
with open('css/dist.css', 'r', encoding='utf-8') as f:
    dist_content = f.read()

tokens_to_check = [
    '--fluid-title-hero',
    '--fluid-title-xl',
    '--fluid-title-lg',
    '--fluid-title-md',
    '--fluid-title-sm',
    '--fluid-subtitle',
    '--fluid-body',
    '--fluid-pad-section',
    '--fluid-pad-container',
    '--fluid-gap-lg',
    'clamp('
]

for t in tokens_to_check:
    if t in dist_content:
        print(f"✓ Found {t} in css/dist.css")
    else:
        print(f"❌ Missing {t} in css/dist.css")
        all_passed = False

if all_passed:
    print("\n🎉 ALL AUDITS PASSED PERFECTLY!")
