"""
KKS Shopping Store — Image Downloader
======================================
Put this script in the SAME folder as your kksshopping.html file.
Then double-click it (or run: python download_images.py)

It will:
  1. Create an "images" folder next to the HTML file
  2. Download all ~120 product images from richsonic.lk
  3. Update the HTML file to use the local images
"""

import urllib.request
import os
import re
import time

HTML_FILE = r"C:\Users\danus\Downloads\kks\kksshopping (12).html"
# Save images next to the HTML file so the script can run from any cwd
IMG_FOLDER = os.path.join(os.path.dirname(HTML_FILE), "images")
BASE_URL = "https://www.richsonic.lk/wp-content/uploads/2025"

# All product image paths
IMAGE_PATHS = [
    "/09/RPFS-1554--300x300.png",
    "/09/RPFS-1592-300x300.jpg",
    "/10/1131-300x300.jpg",
    "/10/1141-300x300.jpg",
    "/10/1143-300x300.jpg",
    "/10/1144-1-300x300.jpg",
    "/10/1145-300x300.jpg",
    "/10/1146-1147-1-300x300.jpg",
    "/10/1146-1147-300x300.jpg",
    "/10/2020-1-300x300.jpg",
    "/10/2024-300x300.jpg",
    "/10/2032-300x300.png",
    "/10/4677-300x300.jpg",
    "/10/48-300x300.jpg",
    "/10/5717-300x300.jpg",
    "/10/5762-300x300.jpg",
    "/10/5784-300x300.jpg",
    "/10/5796-300x300.jpg",
    "/10/597-LCD-300x300.jpg",
    "/10/6063-6064-1-300x300.jpeg",
    "/10/6063-6064-300x300.jpeg",
    "/10/6074-75-76-1-300x300.jpeg",
    "/10/6074-75-76-2-300x300.jpeg",
    "/10/6074-75-76-300x300.jpeg",
    "/10/6094-6095-6096-6097-1-300x300.jpeg",
    "/10/6094-6095-6096-6097-300x300.jpeg",
    "/10/7171-300x300.jpg",
    "/10/770-2.0-LTR-300x300.jpg",
    "/10/869-300x300.jpeg",
    "/10/877-1-300x300.jpeg",
    "/10/RH-3530-300x300.png",
    "/10/RH-3548-300x300.png",
    "/10/RH-779-G-300x300.jpg",
    "/10/RHK-1136-300x300.png",
    "/10/RHPC-770-3.0-LTR-5.0LTR-1-300x300.jpg",
    "/10/RHPC-770-3.0-LTR-5.0LTR-300x300.jpg",
    "/10/RPBL-789-300x300.jpg",
    "/10/RPBL-790-300x300.jpg",
    "/10/RPBL-791-300x300.png",
    "/10/RPCF-1577-300x300.jpeg",
    "/10/RPCK-1160-300x300.jpg",
    "/10/RPCK-1163-300x300.jpg",
    "/10/RPCK-1164-2.0L-300x300.jpg",
    "/10/RPCK-1165-300x300.jpg",
    "/10/RPCK-1169-300x300.jpg",
    "/10/RPCK-1172-300x300.jpg",
    "/10/RPCK-1173-300x300.jpg",
    "/10/RPFS-1592-300x300.jpeg",
    "/10/RPFT-639-BLUE-300x300.jpg",
    "/10/RPFW-1574-300x300.jpg",
    "/10/RPFW-1575R-300x300.jpg",
    "/10/RPGC-592-300x300.jpg",
    "/10/RPGC-596SS-300x300.jpg",
    "/10/RPGC-597T-300x300.jpg",
    "/10/RPGC-598SS-300x300.jpg",
    "/10/RPGC-599T-1-300x300.jpg",
    "/10/RPGC-602SS-300x300.png",
    "/10/RPI-3562D-300x300.png",
    "/10/RPI-3563-300x300.png",
    "/10/RPMG-2041-1-300x300.jpeg",
    "/10/RPOF-1565-300x300.jpeg",
    "/10/RPRC-6077-0.6L-300x300.jpg",
    "/10/RPRC-6078-1.0L-300x300.jpg",
    "/10/RPRC-6079-1.5L-300x300.jpg",
    "/10/RPRC-6086-1.8L-300x300.jpg",
    "/10/RPRC-6087-1.8L-300x300.jpg",
    "/10/RPRC-6088-2.8L-300x300.jpg",
    "/10/RPRD-849-300x300.jpg",
    "/10/RPRD-859BT--300x300.jpg",
    "/10/RPRD-860--300x300.jpg",
    "/10/RPRD-861BT-300x300.jpg",
    "/10/RPRD-862--300x300.jpeg",
    "/10/RPSM-198-300x300.jpg",
    "/10/RPSM-199-300x300.jpg",
    "/10/RPSM-201-300x300.jpg",
    "/10/RPSM-209-300x300.png",
    "/10/RPSW-856-300x300.png",
    "/10/RSBL-788-300x300.jpg",
    "/10/RSBM-508-300x300.png",
    "/10/RSBM-510-300x300.png",
    "/10/RSCF-1572-300x300.jpg",
    "/10/RSFE-1587-300x300.jpeg",
    "/10/RSFS-1569-BLACK-300x300.jpg",
    "/10/RSFS-1579-300x300.jpg",
    "/10/RSFS-1580-300x300.jpg",
    "/10/RSFS-1581-BLUE-300x300.jpg",
    "/10/RSFS-15821583-1-1-300x300.jpg",
    "/10/RSFS-15821583-1-300x300.jpg",
    "/10/RSGC-522-300x300.jpg",
    "/10/RSGC-610G-WT-300x300.jpg",
    "/10/RSGC-611G-300x300.jpeg",
    "/10/RSHM-507-BLACK-300x300.png",
    "/10/RSHM-511-product-logo-300x300.jpg",
    "/10/RSHM-512-product-logo-300x300.jpg",
    "/10/RSI-3578-GREEN-300x300.jpg",
    "/10/RSO-50-300x300.png",
    "/10/RSO-51-1-1-300x300.jpg",
    "/10/RSO-52-300x300.png",
    "/10/RSO-53-300x300.png",
    "/10/RSO-55-300x300.jpg",
    "/10/RSO-56-300x300.jpg",
    "/10/RSPS-878-300x300.jpeg",
    "/10/RSPT-270-300x300.jpeg",
    "/10/RSPT-271-300x300.jpeg",
    "/10/RSRC-6091-300x300.png",
    "/10/RSRC-6092-300x300.jpg",
    "/10/RSTV-874-300x300.jpeg",
    "/10/RSTV-875-300x300.jpeg",
    "/10/RSTV-876-300x300.jpeg",
    "/10/RSTV-879-300x300.jpeg",
    "/10/RSTV-880-300x300.jpeg",
    "/10/RSTV-881-300x300.jpeg",
    "/10/Richsonic-888-300x300.jpeg",
    "/10/Richsonic-8891-300x300.jpeg",
    "/10/SK-10-01-300x300.png",
    "/10/SK-10-02-300x300.png",
    "/10/SK-10-03-300x300.jpg",
    "/10/SKGC-600SS-300x300.jpg",
    "/10/SKI-3577-2-300x300.png",
    "/10/SQ-284-300x300.jpg",
    "/10/SQ-31-300x300.jpg",
    "/10/SQ-361-300x300.jpg",
    "/10/SQ-373-300x300.jpg",
    "/10/SQ-38-300x300.jpg",
    "/10/SQ-50-300x300.jpg",
    "/10/SQ-51-300x300.jpg",
    "/10/SQ-53-300x300.jpg",
]

def main():
    # Check HTML file exists
    if not os.path.exists(HTML_FILE):
        print(f"ERROR: '{HTML_FILE}' not found!")
        print("Make sure this script is in the same folder as kksshopping.html")
        input("Press Enter to exit...")
        return

    # Create images folder
    os.makedirs(IMG_FOLDER, exist_ok=True)
    print(f"Saving images to '{IMG_FOLDER}/' folder...\n")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.richsonic.lk/"
    }

    downloaded = 0
    failed = 0

    for i, path in enumerate(IMAGE_PATHS, 1):
        filename = path.split("/")[-1]
        save_path = os.path.join(IMG_FOLDER, filename)

        # Skip if already downloaded
        if os.path.exists(save_path) and os.path.getsize(save_path) > 1000:
            print(f"[{i}/{len(IMAGE_PATHS)}] Already exists: {filename}")
            downloaded += 1
            continue

        url = BASE_URL + path
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
            if len(data) > 1000:  # valid image
                with open(save_path, "wb") as f:
                    f.write(data)
                print(f"[{i}/{len(IMAGE_PATHS)}] ✓ {filename}")
                downloaded += 1
            else:
                print(f"[{i}/{len(IMAGE_PATHS)}] ✗ Empty: {filename}")
                failed += 1
        except Exception as e:
            print(f"[{i}/{len(IMAGE_PATHS)}] ✗ Failed: {filename} ({e})")
            failed += 1

        time.sleep(0.1)  # be polite

    print(f"\nDownloaded: {downloaded}  Failed: {failed}")

    # Patch the HTML to use local images
    print("\nUpdating HTML file to use local images...")
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Replace the proxyImg function to return local path
    html = re.sub(
        r"function proxyImg\(path\) \{[^}]+\}",
        "function proxyImg(path) {\n  const filename = path.split('/').pop();\n  return 'images/' + filename;\n}",
        html
    )

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("✓ HTML updated!")
    print("\nAll done! Open kksshopping.html in your browser.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
