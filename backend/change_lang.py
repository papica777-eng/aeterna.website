import os
import glob
import re

def main():
    repo_dir = r"c:\Users\papic\Desktop\AETERNA-WEBSITE-REPO"
    
    # Process HTML and JS files
    target_files = glob.glob(os.path.join(repo_dir, "*.html")) + \
                   glob.glob(os.path.join(repo_dir, "js", "*.js")) + \
                   glob.glob(os.path.join(repo_dir, "docs", "*.html"))

    for file_path in target_files:
        if not os.path.exists(file_path):
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # 1. State objects (Vue/React patterns)
        new_content = re.sub(r'language:\s*"bg"', 'language: "en"', new_content)
        new_content = re.sub(r"language:\s*'bg'", "language: 'en'", new_content)
        
        # 2. Vanilla JS state variables
        new_content = re.sub(r"let\s+currentLang\s*=\s*'bg';", "let currentLang = 'en';", new_content)
        new_content = re.sub(r'let\s+currentLang\s*=\s*"bg";', 'let currentLang = "en";', new_content)
        
        # 3. Fallbacks
        new_content = re.sub(r"\|\|\s*'bg'", "|| 'en'", new_content)
        new_content = re.sub(r'\|\|\s*"bg"', '|| "en"', new_content)
        
        # 4. Initialization calls
        new_content = re.sub(r"setLanguage\('bg'\);", "setLanguage('en');", new_content)
        new_content = re.sub(r'setLanguage\("bg"\);', 'setLanguage("en");', new_content)
        
        # 5. HTML lang attribute
        new_content = re.sub(r'<html lang="bg">', '<html lang="en">', new_content)
        
        # 6. Active language buttons
        new_content = new_content.replace('id="lang-bg" class="lang-btn active"', 'id="lang-bg" class="lang-btn"')
        new_content = new_content.replace("id='lang-bg' class='lang-btn active'", "id='lang-bg' class='lang-btn'")
        new_content = new_content.replace('id="lang-en" class="lang-btn"', 'id="lang-en" class="lang-btn active"')
        new_content = new_content.replace("id='lang-en' class='lang-btn'", "id='lang-en' class='lang-btn active'")
        
        if content != new_content:
            print(f"Updated {os.path.basename(file_path)}")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

if __name__ == "__main__":
    main()
