import os
import re
import urllib.request

HTML_FILE = r"C:\Users\danus\Downloads\kks\kksshopping (12).html"
IMG_DIR = r"C:\Users\danus\Downloads\kks\richsonic_images"
IMG_REL = "richsonic_images"

os.makedirs(IMG_DIR, exist_ok=True)

def read_products(html):
    m = re.search(r"const PRODUCTS = \[([\s\S]*?)\];", html)
    if not m:
        return []
    block = m.group(1)
    # crude parse: find model and cat pairs
    items = re.findall(r"\{[^}]*?model:\'([^']+)'[^}]*?cat:\'([^']+)'[^}]*?\}", block)
    return [{'model':mod,'cat':cat} for mod,cat in items]

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# load IMG_MAP block
m = re.search(r"const IMG_MAP = \{([\s\S]*?)\};", html)
if not m:
    print('IMG_MAP not found'); raise SystemExit(1)
block = m.group(1)

entries = re.findall(r"'([^']+)'\s*:\s*'([^']+)'", block)
img_exists = set(os.listdir(IMG_DIR))

products = read_products(html)
cats_needed = {}

for key,val in entries:
    fname = os.path.basename(val)
    if fname in img_exists:
        continue
    # mark this model missing
    # find its category
    cat = next((p['cat'] for p in products if p['model']==key), 'Generic')
    cats_needed.setdefault(cat, []).append(key)

if not cats_needed:
    print('No missing images detected.')
    raise SystemExit(0)

print('Missing images for categories:', ', '.join(cats_needed.keys()))

# Download one representative image per category using source.unsplash.com
for cat in cats_needed:
    query = cat.split()[0]
    safe_name = re.sub(r'[^A-Za-z0-9]', '_', cat).lower()
    out_name = f"cat_{safe_name}.jpg"
    out_path = os.path.join(IMG_DIR, out_name)
    if not os.path.exists(out_path):
        url = f'https://source.unsplash.com/800x800/?{urllib.request.quote(query)}'
        print('Downloading', url, '->', out_name)
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read()
            with open(out_path, 'wb') as f:
                f.write(data)
            print('Saved', out_name)
        except Exception as e:
            print('Failed to download for', cat, e)

# Update IMG_MAP entries for missing models to point to the category image
new_block = block
for cat, models in cats_needed.items():
    safe_name = re.sub(r'[^A-Za-z0-9]', '_', cat).lower()
    out_name = f"cat_{safe_name}.jpg"
    rel = IMG_REL + '/' + out_name
    for model in models:
        # replace the value for model in block
        new_block = re.sub(r"('"+re.escape(model)+r"'\s*:\s*')([^']*)(')", r"'"+model+r"': '"+rel+r"'", new_block)

new_html = html[:m.start(1)] + new_block + html[m.end(1):]
with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(new_html)

print('Patched IMG_MAP for missing images. Please reload the page (hard refresh).')
