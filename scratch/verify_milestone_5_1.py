import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HTML_FILES = [
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

VIDEO_PAGES = [
    'index.html',
    'nuestra-cocina/index.html'
]

E164_REGEX = re.compile(r'^\+[1-9]\d{7,14}$')

def audit_html_file(rel_path):
    full_path = os.path.join(BASE_DIR, rel_path.replace('/', os.sep))
    if not os.path.exists(full_path):
        return [f"File {rel_path} does not exist"]

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []

    # 1. Verify closing body exists
    if '</body>' not in content:
        return [f"{rel_path}: Missing </body> tag"]

    # 2. Extract script tags of type application/ld+json
    ld_json_blocks = re.findall(r'<script\s+type=["\']application/ld\+json["\']\s*>([\s\S]*?)</script>', content)

    if not ld_json_blocks:
        return [f"{rel_path}: No application/ld+json script tags found"]

    # 3. Verify they appear inside <head> (before </head>)
    head_idx = content.find('</head>')
    if head_idx == -1:
        return [f"{rel_path}: Missing </head> tag"]

    for match in re.finditer(r'<script\s+type=["\']application/ld\+json["\']\s*>', content):
        script_idx = match.start()
        if script_idx > head_idx:
            errors.append(f"{rel_path}: JSON-LD script appears AFTER </head> tag, expected inside <head>")

    # 4. Parse JSON blocks
    schemas = []
    for idx, block in enumerate(ld_json_blocks):
        try:
            parsed = json.loads(block.strip())
            schemas.append(parsed)
        except json.JSONDecodeError as e:
            errors.append(f"{rel_path}: JSON-LD block #{idx+1} has invalid JSON syntax: {e}")

    # 5. Check LocalBusiness Schema
    local_business = None
    video_objects = []

    for s in schemas:
        stype = s.get('@type')
        if stype == 'LocalBusiness':
            local_business = s
        elif stype == 'VideoObject':
            video_objects.append(s)

    if not local_business:
        errors.append(f"{rel_path}: Missing '@type': 'LocalBusiness' schema")
    else:
        # Check required fields
        if local_business.get('@context') != 'https://schema.org':
            errors.append(f"{rel_path}: LocalBusiness @context must be 'https://schema.org'")

        for req in ['name', 'image', 'telephone', 'email', 'url', 'logo', 'address', 'sameAs']:
            if not local_business.get(req):
                errors.append(f"{rel_path}: LocalBusiness missing '{req}'")

        # Validate Telephone E.164
        tel = local_business.get('telephone')
        if tel and not E164_REGEX.match(str(tel)):
            errors.append(f"{rel_path}: LocalBusiness telephone '{tel}' is not in valid E.164 format (+54...)")

        # Validate URLs
        for url_field in ['image', 'url', 'logo']:
            val = local_business.get(url_field, '')
            if val and not val.startswith('http'):
                errors.append(f"{rel_path}: LocalBusiness '{url_field}' must be an absolute URL (starts with http): {val}")

        # Validate PostalAddress
        addr = local_business.get('address')
        if isinstance(addr, dict):
            if addr.get('@type') != 'PostalAddress':
                errors.append(f"{rel_path}: Address @type must be 'PostalAddress'")
            for addr_req in ['streetAddress', 'addressLocality', 'addressRegion', 'postalCode', 'addressCountry']:
                if not addr.get(addr_req):
                    errors.append(f"{rel_path}: PostalAddress missing '{addr_req}'")
        else:
            errors.append(f"{rel_path}: LocalBusiness address must be an object (PostalAddress)")

        # Validate sameAs
        same_as = local_business.get('sameAs')
        if not isinstance(same_as, list) or len(same_as) < 2:
            errors.append(f"{rel_path}: LocalBusiness sameAs must be a list with at least 2 social profiles")

    # 6. Check VideoObject Schema for pages with video
    if rel_path in VIDEO_PAGES:
        if not video_objects:
            errors.append(f"{rel_path}: Expected VideoObject schema for page with video")
        else:
            for vo in video_objects:
                if vo.get('@context') != 'https://schema.org':
                    errors.append(f"{rel_path}: VideoObject @context must be 'https://schema.org'")
                for v_req in ['name', 'description', 'thumbnailUrl', 'uploadDate', 'contentUrl', 'embedUrl']:
                    val = vo.get(v_req)
                    if not val:
                        errors.append(f"{rel_path}: VideoObject missing '{v_req}'")
                # Thumbnail absolute
                thumb = vo.get('thumbnailUrl', '')
                if thumb and not thumb.startswith('http'):
                    errors.append(f"{rel_path}: VideoObject thumbnailUrl must be an absolute URL")
    else:
        if video_objects:
            errors.append(f"{rel_path}: Unexpected VideoObject on page without video")

    return errors

def main():
    print("=" * 60)
    print("AUDITING MILESTONE 5.1: SEO ESTRUCTURADO SCHEMA JSON-LD")
    print("=" * 60)

    total_errors = []
    for rel_path in HTML_FILES:
        errs = audit_html_file(rel_path)
        if errs:
            print(f"❌ {rel_path}:")
            for e in errs:
                print(f"   - {e}")
            total_errors.extend(errs)
        else:
            is_video = " [+VideoObject]" if rel_path in VIDEO_PAGES else ""
            print(f"✓ {rel_path}: Valid LocalBusiness Schema{is_video} inside <head>")

    print("\n" + "=" * 60)
    if total_errors:
        print(f"FAILED WITH {len(total_errors)} ERROR(S)!")
        sys.exit(1)
    else:
        print("🎉 ALL 10 HTML FILES PASSED MILESTONE 5.1 AUDIT PERFECTLY!")
        print("Schema JSON-LD LocalBusiness & VideoObject 100% compliant.")
        sys.exit(0)

if __name__ == '__main__':
    main()
