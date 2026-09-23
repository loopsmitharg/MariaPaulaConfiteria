import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_CSS = os.path.join(BASE_DIR, 'css', 'styles.css')
DIST_CSS = os.path.join(BASE_DIR, 'css', 'dist.css')

def minify_css(css_content):
    # 1. Remove comments
    css = re.sub(r'/\*[\s\S]*?\*/', '', css_content)
    # 2. Normalize newlines and whitespace
    css = re.sub(r'\s+', ' ', css)
    # 3. Remove space around symbols
    css = re.sub(r'\s*([\{\}:;,>])\s*', r'\1', css)
    # 4. Restore space around 'and' in media queries: e.g. @media (min-width:640px) and (max-width:1024px)
    css = re.sub(r'\band\(', 'and (', css)
    css = re.sub(r'\)and\b', ') and', css)
    # 5. Remove trailing semicolons before closing brace
    css = re.sub(r';\}', '}', css)
    # 6. Ensure .hidden has !important and clean format
    return css.strip()

if __name__ == '__main__':
    with open(SRC_CSS, 'r', encoding='utf-8') as f:
        src = f.read()
    minified = minify_css(src)
    with open(DIST_CSS, 'w', encoding='utf-8') as f:
        f.write(minified)
    print(f"Compiled {SRC_CSS} ({len(src)} bytes) -> {DIST_CSS} ({len(minified)} bytes)")
