"""
Richsonic Shop — Full Image Downloader
=======================================
Downloads ALL product images from richsonic.lk/shop/ (177 products, 15 pages)
into a folder called "richsonic_images".

Run: python download_richsonic_images.py
"""

import urllib.request
import urllib.parse
import os
import re
import time

SAVE_FOLDER = "richsonic_images"
BASE_URL = "https://richsonic.lk/shop/"
TOTAL_PAGES = 15

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0",
    "Referer": "https://richsonic.lk/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="ignore")

def get_image_urls(html):
    # Match WooCommerce product images (any size)
    imgs = re.findall(r'https://richsonic\.lk/wp-content/uploads/[^\s"\'<>]+?\.(?:jpg|jpeg|png|webp)', html)
    # Filter to product images only (exclude logos, icons, brands)
    filtered = []
    skip = ["logo", "Logo", "Brand", "brand", "icon", "banner", "Banner", "scaled"]
    for url in imgs:
        if not any(s in url for s in skip):
            # Prefer full-size or 700x (product images), not tiny thumbnails
            filtered.append(url)
    # Remove duplicates keeping order
    seen = set()
    result = []
    for url in filtered:
        if url not in seen:
            seen.add(url)
            result.append(url)
    return result

def download_image(url, folder):
    filename = url.split("/")[-1]
    # Clean up filename
    filename = urllib.parse.unquote(filename)
    save_path = os.path.join(folder, filename)
    if os.path.exists(save_path) and os.path.getsize(save_path) > 2000:
        return filename, "skip"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
        if len(data) > 2000:
            with open(save_path, "wb") as f:
                f.write(data)
            return filename, "ok"
        return filename, "empty"
    except Exception as e:
        return filename, f"fail:{e}"

def main():
    os.makedirs(SAVE_FOLDER, exist_ok=True)
    print(f"=== Richsonic Image Downloader ===")
    print(f"Saving to: {os.path.abspath(SAVE_FOLDER)}\n")

    all_image_urls = set()

    # Step 1: Scrape all 15 pages to collect image URLs
    for page in range(1, TOTAL_PAGES + 1):
        url = BASE_URL if page == 1 else f"{BASE_URL}page/{page}/"
        print(f"Scanning page {page}/{TOTAL_PAGES}: {url}")
        try:
            html = fetch(url)
            imgs = get_image_urls(html)
            print(f"  Found {len(imgs)} images")
            all_image_urls.update(imgs)
        except Exception as e:
            print(f"  ERROR: {e}")
        time.sleep(0.5)

    all_image_urls = sorted(all_image_urls)
    print(f"\nTotal unique images found: {len(all_image_urls)}")
    print("Downloading...\n")

    # Step 2: Download all images
    ok = skip = fail = 0
    for i, url in enumerate(all_image_urls, 1):
        filename, status = download_image(url, SAVE_FOLDER)
        if status == "ok":
            print(f"[{i}/{len(all_image_urls)}] ✓ {filename}")
            ok += 1
        elif status == "skip":
            print(f"[{i}/{len(all_image_urls)}] — Already exists: {filename}")
            skip += 1
        else:
            print(f"[{i}/{len(all_image_urls)}] ✗ {filename} ({status})")
            fail += 1
        time.sleep(0.15)

    print(f"\n{'='*40}")
    print(f"Done! Downloaded: {ok}  Skipped: {skip}  Failed: {fail}")
    print(f"Images saved in: {os.path.abspath(SAVE_FOLDER)}")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
