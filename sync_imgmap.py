import os
import re

HTML_FILE = r"C:\Users\danus\Downloads\kks\kksshopping (12).html"
IMG_DIR = r"C:\Users\danus\Downloads\kks\richsonic_images"
IMG_REL = "richsonic_images"

def normalize(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

files = os.listdir(IMG_DIR)
norm_map = {normalize(f): f for f in files}

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r"const IMG_MAP = \{([\s\S]*?)\};", html)
if not m:
    print('IMG_MAP block not found')
    raise SystemExit(1)

block = m.group(1)
lines = block.split('\n')
new_lines = []
updated = 0

for line in lines:
    lm = re.match(r"\s*'([^']+)'\s*:\s*'([^']+)'\s*,?", line)
    if not lm:
        new_lines.append(line)
        continue
    key, val = lm.group(1), lm.group(2)
    key_norm = normalize(key)
    # search for file that contains the model code
    found = None
    for nf, fname in norm_map.items():
        if key_norm in nf:
            found = fname
            break
    if not found:
        # try partial match by splitting at hyphen
        short = re.sub(r'-[^-]+$', '', key).lower()
        short_norm = normalize(short)
        for nf, fname in norm_map.items():
            if short_norm and short_norm in nf:
                found = fname
                break
    if found:
        new_val = f"{IMG_REL}/{found}"
        new_line = re.sub(r"('(?:[^']+)')\s*:\s*'[^']+'", f"'{key}': '{new_val}'", line)
        new_lines.append(new_line)
        updated += 1
    else:
        new_lines.append(line)

new_block = '\n'.join(new_lines)
new_html = html[:m.start(1)] + new_block + html[m.end(1):]

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f'Updated {updated} IMG_MAP entries in {HTML_FILE}')
