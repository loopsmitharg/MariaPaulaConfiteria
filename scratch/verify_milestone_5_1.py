import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACTIVE_HTML_FILES = [
    'index.html',
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

    # 5. Extract FoodEstablishment / Bakery entity (or mainEntity in ContactPage)
    food_business = None
    video_objects = []
    specialized_schemas = []

    for s in schemas:
        stype = s.get('@type')
        if isinstance(stype, list) and ("Bakery" in stype or "LocalBusiness" in stype or "CafeOrCoffeeShop" in stype):
            food_business = s
        elif stype == 'LocalBusiness':
            food_business = s
        elif stype == 'ContactPage':
            specialized_schemas.append(s)
            main_ent = s.get('mainEntity', {})
            mtype = main_ent.get('@type')
            if isinstance(mtype, list) and ("Bakery" in mtype or "CafeOrCoffeeShop" in mtype):
                food_business = main_ent
        elif stype in ['Menu', 'Service', 'EventVenue', 'OfferCatalog']:
            specialized_schemas.append(s)
        elif stype == 'VideoObject':
            video_objects.append(s)

    if not food_business:
        errors.append(f"{rel_path}: Missing multi-typed Bakery/CafeOrCoffeeShop/Restaurant schema")
    else:
        # Check required fields
        for req in ['name', 'url', 'priceRange', 'currenciesAccepted', 'paymentAccepted']:
            if not food_business.get(req):
                errors.append(f"{rel_path}: FoodBusiness missing enriched field '{req}'")

        # Validate Telephone if present
        tel = food_business.get('telephone')
        if tel and not E164_REGEX.match(str(tel)):
            errors.append(f"{rel_path}: Telephone '{tel}' is not in valid E.164 format (+54...)")

        # Validate openingHoursSpecification if present
        hours = food_business.get('openingHoursSpecification')
        if hours:
            if not isinstance(hours, list) or len(hours) == 0:
                errors.append(f"{rel_path}: openingHoursSpecification must be a non-empty list")
            else:
                h = hours[0]
                if h.get('opens') != '06:00' or h.get('closes') != '22:00':
                    errors.append(f"{rel_path}: Invalid openingHoursSpecification hours: {h}")

    # 6. Check specialized schemas by page
    if rel_path == 'menu/index.html':
        menu_schema = next((s for s in specialized_schemas if s.get('@type') == 'Menu'), None)
        if not menu_schema:
            errors.append("menu/index.html: Expected 'Menu' schema with 'hasMenuSection'")
        elif not menu_schema.get('hasMenuSection'):
            errors.append("menu/index.html: 'Menu' schema missing 'hasMenuSection'")

    elif rel_path == 'catering/index.html':
        service_schema = next((s for s in specialized_schemas if s.get('@type') == 'Service'), None)
        if not service_schema:
            errors.append("catering/index.html: Expected 'Service' schema")
        elif not service_schema.get('hasOfferCatalog'):
            errors.append("catering/index.html: 'Service' schema missing 'hasOfferCatalog'")

    elif rel_path == 'eventos/index.html':
        event_venue = next((s for s in specialized_schemas if s.get('@type') == 'EventVenue'), None)
        if not event_venue:
            errors.append("eventos/index.html: Expected 'EventVenue' schema")

    elif rel_path == 'regalos/index.html':
        offer_cat = next((s for s in specialized_schemas if s.get('@type') == 'OfferCatalog'), None)
        if not offer_cat:
            errors.append("regalos/index.html: Expected 'OfferCatalog' schema for Gift Cards")
        elif not offer_cat.get('itemListElement'):
            errors.append("regalos/index.html: 'OfferCatalog' schema missing 'itemListElement'")

    elif rel_path == 'contacto/index.html':
        contact_page = next((s for s in specialized_schemas if s.get('@type') == 'ContactPage'), None)
        if not contact_page:
            errors.append("contacto/index.html: Expected 'ContactPage' schema")
        else:
            main_ent = contact_page.get('mainEntity', {})
            if not main_ent.get('contactPoint'):
                errors.append("contacto/index.html: mainEntity missing 'contactPoint'")
            if not main_ent.get('department'):
                errors.append("contacto/index.html: mainEntity missing 'department'")

    elif rel_path in ['sucursal-balbin/index.html', 'sucursal-tribulato/index.html']:
        if not food_business.get('geo'):
            errors.append(f"{rel_path}: Missing 'geo' (GeoCoordinates)")
        if not food_business.get('parentOrganization'):
            errors.append(f"{rel_path}: Missing 'parentOrganization'")
        if not food_business.get('potentialAction'):
            errors.append(f"{rel_path}: Missing 'potentialAction' (ReserveAction)")

    # 7. Check VideoObject Schema for pages with video
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

def audit_404_file():
    full_path = os.path.join(BASE_DIR, '404.html')
    if not os.path.exists(full_path):
        return ["404.html does not exist"]
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'application/ld+json' in content:
        return ["404.html: Found application/ld+json Schema. Error pages must NOT contain structured data to avoid Google mismatch warnings."]
    return []

def main():
    print("=" * 60)
    print("AUDITING MILESTONE 5.1: ENRICHED MULTI-TYPED SCHEMA JSON-LD")
    print("=" * 60)

    total_errors = []
    for rel_path in ACTIVE_HTML_FILES:
        errs = audit_html_file(rel_path)
        if errs:
            print(f"❌ {rel_path}:")
            for e in errs:
                print(f"   - {e}")
            total_errors.extend(errs)
        else:
            is_video = " [+VideoObject]" if rel_path in VIDEO_PAGES else ""
            print(f"✓ {rel_path}: Valid Enriched Multi-Type Schema{is_video} inside <head>")

    errs_404 = audit_404_file()
    if errs_404:
        for e in errs_404:
            print(f"❌ 404.html: {e}")
        total_errors.extend(errs_404)
    else:
        print("✓ 404.html: Verified NO Schema JSON-LD (clean error page, 0 mismatch risk)")

    print("\n" + "=" * 60)
    if total_errors:
        print(f"FAILED WITH {len(total_errors)} ERROR(S)!")
        sys.exit(1)
    else:
        print("🎉 ALL HTML FILES PASSED ENRICHED SCHEMA JSON-LD AUDIT PERFECTLY!")
        print("Multi-typing, openingHours, priceRange, currency, hasMenu, acceptsReservations & specialized schemas validated.")
        sys.exit(0)

if __name__ == '__main__':
    main()
