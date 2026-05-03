import os, re
HTML = r"C:\Users\danus\Downloads\kks\kksshopping (12).html"
IMG_DIR = r"C:\Users\danus\Downloads\kks\richsonic_images"
PLACEHOLDER = 'richsonic_images/woocommerce-placeholder-700x798.webp'

with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r"const IMG_MAP = \{([\s\S]*?)\};", html)
if not m:
    print('IMG_MAP not found'); raise SystemExit(1)
block = m.group(1)

def repl(match):
    key = match.group(1)
    val = match.group(2)
    fname = os.path.basename(val)
    if os.path.exists(os.path.join(IMG_DIR, fname)):
        return f"'{key}': '{val}'"
    else:
        return f"'{key}': '{PLACEHOLDER}'"

new_block = re.sub(r"'([^']+)'\s*:\s*'([^']+)'", repl, block)
new_html = html[:m.start(1)] + new_block + html[m.end(1):]
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(new_html)
print('Replaced missing IMG_MAP entries with placeholder')
