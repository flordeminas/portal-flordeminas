import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Detect if already has the entrar CTA inside nav-links
    # Pattern: inside <ul class="nav-links"> ... </ul>, after Clube li
    # We add a <li> with the header-cta "Entrar" ONLY if not already there
    
    # Match the nav-links ul and check if it already has header-cta inside
    nav_ul_re = re.compile(r'<ul class="nav-links">(.*?)</ul>', re.DOTALL)
    nav_match = nav_ul_re.search(content)
    
    if not nav_match:
        return
    
    nav_content = nav_match.group(1)
    
    # Already has a header-cta inside nav-links? Skip.
    if 'header-cta' in nav_content:
        print(f"Already updated: {filepath}")
        return
    
    # Find the Clube li (last li in the nav) to append after it
    # We can detect the relative prefix from the clube.html link already in the nav
    clube_li_re = re.compile(r'(<li><a class="nav-link" href="([^"]*)clube\.html">Clube</a></li>)')
    clube_li_match = clube_li_re.search(nav_content)
    
    if not clube_li_match:
        print(f"Could not find Clube li in: {filepath}")
        return
    
    prefix = clube_li_match.group(2)  # e.g. "" or "../"
    
    entrar_li = f'\n                    <li><a class="header-cta nav-entrar-mobile" href="{prefix}entrar.html">🔒 Entrar</a></li>'
    
    # Insert after the Clube li
    old_clube_li = clube_li_match.group(0)
    new_clube_block = old_clube_li + entrar_li
    
    content = content.replace(old_clube_li, new_clube_block, 1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {filepath}")

def main():
    root_dir = r"c:\Projetos\ZHC\website"
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '.git' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.html'):
                process_file(os.path.join(dirpath, filename))

if __name__ == "__main__":
    main()
