import re

filepath = r"z:\aeterna.website\index.html"
with open(filepath, "r", encoding="utf-16-le") as f:
    text = f.read()

# Let's search for some of the nav keywords
keywords = ["ONCOLOGY HUD", "DIABETES HUD", "UKAME SOLAR"]
for kw in keywords:
    matches = [m.start() for m in re.finditer(kw, text)]
    print(f"Keyword: '{kw}', Matches: {len(matches)}")
    for m in matches:
        # print surrounding text (100 chars before and after)
        start = max(0, m - 100)
        end = min(len(text), m + 100)
        print(f"Context (Index {m}):\n{text[start:end]}\n" + "-"*50)
