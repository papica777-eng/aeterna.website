import os
import re
from PIL import Image, ImageDraw, ImageFilter

REPO_DIR = r"C:\Users\papic\Desktop\_PROJECTS_AND_WORKSPACES\AETERNA-WEBSITE-REPO"
ASSETS_DIR = os.path.join(REPO_DIR, "assets")
BRAIN_LOGO = r"C:\Users\papic\.gemini\antigravity-ide\brain\13c57ed3-80ab-4175-893a-9920da570067\aeterna_phoenix_quantum_glass_1787215553355.jpg"
BRAIN_WIDE = r"C:\Users\papic\VIRTUAL-HUMAN-TWIN\facebook_covers_clean\PHOENIX_COSMIC_REBIRTH_WIDE_16x9.jpg"

os.makedirs(ASSETS_DIR, exist_ok=True)

# 1. Process Master Logo Image
master_img = Image.open(BRAIN_LOGO).convert("RGBA")

# Save master PNG
master_img.save(os.path.join(ASSETS_DIR, "aeterna_logo.png"), quality=99)
master_img.save(os.path.join(ASSETS_DIR, "aeterna_official_logo.png"), quality=99)
master_img.convert("RGB").save(os.path.join(ASSETS_DIR, "aeterna_logo.jpg"), quality=99)

# Save Favicons
fav512 = master_img.resize((512, 512), Image.Resampling.LANCZOS)
fav512.save(os.path.join(ASSETS_DIR, "favicon.png"))
fav512.save(os.path.join(ASSETS_DIR, "favicon_512.png"))

fav192 = master_img.resize((192, 192), Image.Resampling.LANCZOS)
fav192.save(os.path.join(ASSETS_DIR, "favicon_192.png"))

fav32 = master_img.resize((32, 32), Image.Resampling.LANCZOS)
fav32.save(os.path.join(ASSETS_DIR, "favicon_32.png"))
fav32.save(os.path.join(ASSETS_DIR, "favicon.ico"), format="ICO")

# Also save in root directory of repo for standard web crawlers
fav512.save(os.path.join(REPO_DIR, "favicon.png"))
fav32.save(os.path.join(REPO_DIR, "favicon.ico"), format="ICO")

# Update OpenGraph preview (1200 x 630) with wide phoenix artwork
if os.path.exists(BRAIN_WIDE):
    wide_img = Image.open(BRAIN_WIDE).convert("RGBA")
    og_img = wide_img.resize((1200, 630), Image.Resampling.LANCZOS)
    og_img.convert("RGB").save(os.path.join(ASSETS_DIR, "aeterna_og_preview.png"), quality=98)
    print("[SUCCESS] aeterna_og_preview.png updated!")

print("[SUCCESS] All asset images, favicons, and OG previews generated!")

# 2. Update HTML Files across repository
html_files = []
for root, dirs, files in os.walk(REPO_DIR):
    if ".git" in root or "node_modules" in root:
        continue
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

print(f"Scanning {len(html_files)} HTML files for logo and favicon integration...")

count_updated = 0
for hpath in html_files:
    with open(hpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    orig = content
    # Replace favicon references
    content = re.sub(
        r'<link\s+rel=["\']icon["\']\s+type=["\']image/svg\+xml["\']\s+href=["\'](\.\/)?assets/aeterna_logo\.svg["\']\s*\/?>',
        r'<link rel="icon" type="image/png" href="\1assets/favicon.png" />',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'<link\s+rel=["\']icon["\']\s+type=["\']image/svg\+xml["\']\s+href=["\']\.\./assets/aeterna_logo\.svg["\']\s*\/?>',
        r'<link rel="icon" type="image/png" href="../assets/favicon.png" />',
        content,
        flags=re.IGNORECASE
    )
    
    # Replace logo img references
    content = re.sub(
        r'src=["\'](\.\/)?assets/aeterna_logo\.svg["\']',
        r'src="\1assets/aeterna_logo.png"',
        content
    )
    content = re.sub(
        r'src=["\']\.\./assets/aeterna_logo\.svg["\']',
        r'src="../assets/aeterna_logo.png"',
        content
    )
    
    if content != orig:
        with open(hpath, "w", encoding="utf-8") as f:
            f.write(content)
        count_updated += 1
        print(f"  -> Updated: {os.path.relpath(hpath, REPO_DIR)}")

print(f"[SUCCESS] Updated {count_updated} HTML files!")

# 3. Update manifest.json
manifest_p = os.path.join(REPO_DIR, "manifest.json")
if os.path.exists(manifest_p):
    with open(manifest_p, "r", encoding="utf-8") as f:
        mcontent = f.read()
    mcontent = mcontent.replace("./assets/aeterna_logo.svg", "./assets/favicon.png")
    mcontent = mcontent.replace("image/svg+xml", "image/png")
    with open(manifest_p, "w", encoding="utf-8") as f:
        f.write(mcontent)
    print("[SUCCESS] manifest.json updated!")

# 4. Update sw.js
sw_p = os.path.join(REPO_DIR, "sw.js")
if os.path.exists(sw_p):
    with open(sw_p, "r", encoding="utf-8") as f:
        scontent = f.read()
    scontent = scontent.replace("./assets/aeterna_logo.svg", "./assets/aeterna_logo.png")
    with open(sw_p, "w", encoding="utf-8") as f:
        f.write(scontent)
    print("[SUCCESS] sw.js updated!")
