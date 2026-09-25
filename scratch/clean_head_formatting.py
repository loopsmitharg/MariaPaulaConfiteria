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

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean extra spaces before <!-- ═══════════════════════════════════════════ --> in head
    content = re.sub(
        r'^\s*<!-- ═══════════════════════════════════════════ -->\n\s*<!--  DATOS ESTRUCTURADOS SCHEMA\.ORG \(JSON-LD\)   -->\n\s*<!-- ═══════════════════════════════════════════ -->',
        '    <!-- ═══════════════════════════════════════════ -->\n    <!--  DATOS ESTRUCTURADOS SCHEMA.ORG (JSON-LD)   -->\n    <!-- ═══════════════════════════════════════════ -->',
        content,
        flags=re.MULTILINE
    )

    # 2. Clean blank lines between </footer> and </body>
    content = re.sub(r'</footer>\s*\n+([ \t]*</body>)', r'</footer>\n\1', content)

    # 3. Clean up multiple empty lines in <head>
    content = re.sub(r'\n{3,}    <!-- Main Project Styles -->', '\n\n    <!-- Main Project Styles -->', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned formatting in {path}")
