import re

files = [
    'index.html',
    '404.html',
    'catering/index.html',
    'contacto/index.html',
    'eventos/index.html',
    'menu/index.html',
    'nuestra-cocina/index.html',
    'regalos/index.html',
    'sucursal-balbin/index.html',
    'sucursal-tribulato/index.html'
]

pattern = re.compile(
    r'([ \t]*<!-- ═+ -->\s*\n[ \t]*<!--  DATOS ESTRUCTURADOS SCHEMA\.ORG \(JSON-LD\)   -->\s*\n[ \t]*<!-- ═+ -->\s*\n[\s\S]*?)(?=\s*</body>)',
    re.MULTILINE
)

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = pattern.search(content)
    if not match:
        print(f"ERROR: Could not find JSON-LD block in {path}")
        continue

    schema_block = match.group(1).rstrip()
    
    # Remove schema block from body
    new_content = content[:match.start()] + "\n" + content[match.end():]
    
    # Insert schema block in <head> right before <!-- Main Project Styles -->
    styles_idx = new_content.find('<!-- Main Project Styles -->')
    if styles_idx == -1:
        print(f"ERROR: Could not find '<!-- Main Project Styles -->' in {path}")
        continue
    
    # Find indentation of '<!-- Main Project Styles -->'
    line_start = new_content.rfind('\n', 0, styles_idx) + 1
    indent = new_content[line_start:styles_idx]
    
    insertion = schema_block + "\n\n" + indent
    new_content = new_content[:line_start] + indent + insertion + new_content[styles_idx:]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"SUCCESS: Moved JSON-LD to <head> in {path}")

