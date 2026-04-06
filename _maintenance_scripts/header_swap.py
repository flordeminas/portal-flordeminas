import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Fix duplicate headers (found in some articles)
    # Usually the first one is correct (top of body), the one inside <article> is redundant.
    header_blocks = list(re.finditer(r'<header class="site-header">.*?</header>', content, re.DOTALL))
    if len(header_blocks) > 1:
        print(f"Fixing duplicate headers in: {filepath}")
        # Keep only the first one, remove others
        first_header = header_blocks[0].group(0)
        # Replace all headers with a placeholder, then put the first one back
        content = re.sub(r'<header class="site-header">.*?</header>', 'HEADER_PLACEHOLDER', content, flags=re.DOTALL)
        content = content.replace('HEADER_PLACEHOLDER', first_header, 1)
        content = content.replace('HEADER_PLACEHOLDER', '') # remove extras

    # Step 2: Swap "Entrar" and "Clube"
    # Find the nav link for Entrar and the CTA for Clube
    entrar_re = re.compile(r'<li><a class="nav-link login-link" href="([^"]*)entrar.html">🔒 Entrar</a></li>', re.DOTALL)
    clube_re = re.compile(r'<a class="header-cta" href="([^"]*)clube.html">Clube</a>', re.DOTALL)

    entrar_match = entrar_re.search(content)
    clube_match = clube_re.search(content)

    if entrar_match and clube_match:
        prefix_entrar = entrar_match.group(1)
        prefix_clube = clube_match.group(1)
        
        # New "Clube" as NAV LINK (replaces Entrar nav link)
        new_clube_nav = f'<li><a class="nav-link" href="{prefix_entrar}clube.html">Clube</a></li>'
        # New "Entrar" as CTA BUTTON (replaces Clube CTA)
        new_entrar_cta = f'<a class="header-cta" href="{prefix_clube}entrar.html">🔒 Entrar</a>'
        
        # We need to be careful with the order of sub. 
        # Since we have unique matches, we can use string replace on the full match strings.
        content = content.replace(entrar_match.group(0), new_clube_nav)
        content = content.replace(clube_match.group(0), new_entrar_cta)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

def main():
    root_dir = r"c:\Projetos\ZHC\website"
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip some folders if necessary (e.g. .git)
        if '.git' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.html'):
                process_file(os.path.join(dirpath, filename))

if __name__ == "__main__":
    main()
