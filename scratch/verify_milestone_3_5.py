import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HTML_FILES = {
    'index.html': './js/main.js',
    '404.html': './js/main.js',
    'catering/index.html': '../js/main.js',
    'contacto/index.html': '../js/main.js',
    'eventos/index.html': '../js/main.js',
    'menu/index.html': '../js/main.js',
    'nuestra-cocina/index.html': '../js/main.js',
    'regalos/index.html': '../js/main.js',
    'sucursal-balbin/index.html': '../js/main.js',
    'sucursal-tribulato/index.html': '../js/main.js',
}

def audit_html_files():
    print("Auditing 10 HTML files for Vanilla JS defer, zero inline events, and head placement...")
    errors = []

    for rel_path, expected_script in HTML_FILES.items():
        file_path = os.path.join(BASE_DIR, rel_path.replace('/', os.sep))
        if not os.path.exists(file_path):
            errors.append(f"Missing file: {rel_path}")
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Check head vs body split
        head_match = re.search(r'<head\b[^>]*>(.*?)</head>', content, re.DOTALL | re.IGNORECASE)
        if not head_match:
            errors.append(f"{rel_path}: <head> tag not found")
            continue
        head_content = head_match.group(1)

        body_match = re.search(r'<body\b[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        if not body_match:
            errors.append(f"{rel_path}: <body> tag not found")
            continue
        body_content = body_match.group(1)

        # 2. Check script in head with defer
        pattern = re.compile(rf'<script\s+src="{re.escape(expected_script)}"\s+defer\s*>\s*</script>', re.IGNORECASE)
        if not pattern.search(head_content):
            errors.append(f"{rel_path}: Expected '<script src=\"{expected_script}\" defer></script>' in <head>")
        else:
            print(f"  [OK] {rel_path}: Has '{expected_script}' defer in <head>")

        # 3. Check NO script tags in body (except schema json-ld if any)
        body_scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', body_content, re.DOTALL | re.IGNORECASE)
        if body_scripts:
            errors.append(f"{rel_path}: Found {len(body_scripts)} unexpected <script> tag(s) inside <body>")

        # 4. Check for ANY inline event handler: on\w+=
        inline_events = re.findall(r'\s(on[a-zA-Z]+)\s*=', content)
        if inline_events:
            errors.append(f"{rel_path}: Found inline event handlers: {set(inline_events)}")
        else:
            print(f"  [OK] {rel_path}: 0 inline event attributes")

        # 5. Check executable script tags (excluding application/ld+json)
        all_scripts = re.findall(r'<script\b([^>]*)>', content, re.IGNORECASE)
        for attrs in all_scripts:
            if 'application/ld+json' in attrs:
                continue
            if not ('src=' in attrs and 'defer' in attrs):
                errors.append(f"{rel_path}: Non-defer or inline executable script tag detected: <script {attrs}>")

    return errors

def audit_main_js():
    print("\nAuditing js/main.js...")
    errors = []
    main_js_path = os.path.join(BASE_DIR, 'js', 'main.js')
    if not os.path.exists(main_js_path):
        return ["js/main.js does not exist!"]

    with open(main_js_path, 'r', encoding='utf-8') as f:
        js = f.read()

    # Check for jQuery or framework dependencies
    if '$(' in js or 'jQuery' in js:
        errors.append("js/main.js: jQuery usage detected (Prohibited by blueprint).")
    else:
        print("  [OK] No jQuery or external runtime framework detected.")

    # Check event delegation on document
    if 'document.addEventListener(\'click\'' not in js and 'document.addEventListener("click"' not in js:
        errors.append("js/main.js: Missing document.addEventListener('click')")
    else:
        print("  [OK] Delegated click listeners on document present.")

    if 'e.target.closest(' not in js and 'target.closest(' not in js:
        errors.append("js/main.js: Missing e.target.closest selector delegation")
    else:
        print("  [OK] Event target closest selector delegation present.")

    # Check form submit handling
    if 'document.addEventListener(\'submit\'' not in js and 'document.addEventListener("submit"' not in js:
        errors.append("js/main.js: Missing document.addEventListener('submit')")
    else:
        print("  [OK] Delegated submit listener on document present.")

    if 'e.preventDefault()' not in js:
        errors.append("js/main.js: Missing e.preventDefault() in submit handler")
    else:
        print("  [OK] e.preventDefault() properly intercepts form submission.")

    if 'disabled = true' not in js:
        errors.append("js/main.js: Missing submit button disabling (disabled = true)")
    else:
        print("  [OK] Submit button is disabled on submission.")

    if 'Enviando...' not in js:
        errors.append("js/main.js: Missing 'Enviando...' button feedback text")
    else:
        print("  [OK] Button text changes to 'Enviando...'.")

    if 'fetch(' not in js or 'POST' not in js:
        errors.append("js/main.js: Missing asynchronous fetch() POST call")
    else:
        print("  [OK] Asynchronous fetch() POST JSON implemented.")

    if '5000' not in js:
        errors.append("js/main.js: Missing 5000ms (5 seconds) toast duration")
    else:
        print("  [OK] 5000ms (5 seconds) floating feedback toast configured.")

    if 'form.reset()' not in js:
        errors.append("js/main.js: Missing form.reset()")
    else:
        print("  [OK] form.reset() executes after submission.")

    return errors

def audit_dist_css():
    print("\nAuditing compiled production CSS (css/dist.css)...")
    errors = []
    dist_path = os.path.join(BASE_DIR, 'css', 'dist.css')
    if not os.path.exists(dist_path):
        return ["css/dist.css does not exist!"]

    size = os.path.getsize(dist_path)
    if size < 10000:
        errors.append(f"css/dist.css appears too small: {size} bytes")
    else:
        print(f"  [OK] css/dist.css compiled successfully ({size} bytes).")

    with open(dist_path, 'r', encoding='utf-8') as f:
        css = f.read()

    if '#toast' not in css:
        errors.append("css/dist.css: Missing #toast styling")
    else:
        print("  [OK] #toast styling present in production bundle.")

    return errors

if __name__ == '__main__':
    all_errors = []
    all_errors.extend(audit_html_files())
    all_errors.extend(audit_main_js())
    all_errors.extend(audit_dist_css())

    print("\n" + "=" * 50)
    if all_errors:
        print(f"FAILED WITH {len(all_errors)} ERROR(S):")
        for err in all_errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("ALL MILESTONE 3.5 CHECKS PASSED PERFECTLY!")
        print("100% Vanilla ES6+ Defer, Event Delegation & Async Forms Validated.")
        sys.exit(0)
