import glob, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

html_files = sorted(glob.glob('**/*.html', recursive=True))
print(f"Auditing data-root attributes across {len(html_files)} HTML files:\n")

expected = {
    '404.html': './',
    'index.html': './',
    os.path.normpath('catering/index.html'): '../',
    os.path.normpath('contacto/index.html'): '../',
    os.path.normpath('eventos/index.html'): '../',
    os.path.normpath('menu/index.html'): '../',
    os.path.normpath('nuestra-cocina/index.html'): '../',
    os.path.normpath('regalos/index.html'): '../',
    os.path.normpath('sucursal-balbin/index.html'): '../',
    os.path.normpath('sucursal-tribulato/index.html'): '../'
}

all_ok = True
for hf in html_files:
    if 'node_modules' in hf or '.git' in hf or 'brain' in hf or 'google' in hf:
        continue
    norm = os.path.normpath(hf)
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'<body\s+([^>]*?)>', content, re.IGNORECASE)
    if not match:
        print(f"❌ {hf}: No <body ...> tag found!")
        all_ok = False
        continue
    
    attrs = match.group(1)
    data_root_match = re.search(r'data-root=["\']([^"\']+)["\']', attrs)
    if not data_root_match:
        print(f"❌ {hf}: No data-root attribute on <body>!")
        all_ok = False
        continue
    
    actual_root = data_root_match.group(1)
    exp_root = expected.get(norm)
    if actual_root == exp_root:
        print(f"✓ {hf}: data-root=\"{actual_root}\" (Correct)")
    else:
        print(f"❌ {hf}: Expected data-root=\"{exp_root}\", got \"{actual_root}\"")
        all_ok = False

if all_ok:
    print("\n🎉 ALL HTML FILES HAVE CORRECT DATA-ROOT ATTRIBUTES!")
else:
    sys.exit(1)
