import os
import re

# ── Set your exact paths here ──
HTML_FILE = r"C:\Users\danus\Downloads\kks\kksshopping.html"
IMG_FOLDER = r"C:\Users\danus\Downloads\kks\richsonic_images"

# Auto-detect HTML filename if above doesn't work
if not os.path.exists(HTML_FILE):
    folder = r"C:\Users\danus\Downloads\kks"
    for f in os.listdir(folder):
        if f.endswith(".html"):
            HTML_FILE = os.path.join(folder, f)
            print(f"Found HTML: {f}")
            break

def main():
    print(f"HTML : {HTML_FILE}")
    print(f"IMGS : {IMG_FOLDER}")

    if not os.path.exists(HTML_FILE):
        print("ERROR: HTML file not found!"); input(); return
    if not os.path.exists(IMG_FOLDER):
        print("ERROR: Images folder not found!"); input(); return

    local_images = set(os.listdir(IMG_FOLDER))
    print(f"Found {len(local_images)} images\n")

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    img_folder_rel = "richsonic_images"
    html = re.sub(
        r"function proxyImg\(path\) \{[\s\S]*?\}",
        f"function proxyImg(path) {{\n  const filename = path.split('/').pop();\n  return '{img_folder_rel}/' + filename;\n}}",
        html
    )

    def replace_url(m):
        filename = m.group(0).split("/")[-1]
        return f"{img_folder_rel}/{filename}" if filename in local_images else m.group(0)

    html = re.sub(
        r"https://(?:www\.)?richsonic\.lk/wp-content/uploads/[^\s\"'<>]+\.(?:jpg|jpeg|png|webp)",
        replace_url, html
    )

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ Done! Open kksshopping.html in your browser.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
