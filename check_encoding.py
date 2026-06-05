filepath = r"z:\aeterna.website\index.html"
with open(filepath, "rb") as f:
    raw_data = f.read(20000)

print(f"Total raw bytes read: {len(raw_data)}")

encodings = ["utf-8", "utf-16-le", "utf-16-be", "cp1251", "latin1"]
for enc in encodings:
    try:
        text = raw_data.decode(enc)
        text_lower = text.lower()
        if "hud" in text_lower or "ukame" in text_lower or "pricing" in text_lower:
            print(f"[✓] Successfully decoded with: {enc}!")
            # Find snippet
            for kw in ["hud", "ukame", "pricing"]:
                idx = text_lower.find(kw)
                if idx != -1:
                    print(f"   Key '{kw}' context:\n{text[max(0, idx-100):idx+150]}\n")
            break
    except Exception as e:
        print(f"[❌] Failed with {enc}: {e}")
