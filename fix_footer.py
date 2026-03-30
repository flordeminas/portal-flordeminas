import os
import glob
import re

directory = 'c:/Projetos/ZHC/website'
html_files = glob.glob(os.path.join(directory, '**/*.html'), recursive=True)

updated_count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Update text under logo
    content = re.sub(
        r'<p>\s*Facilitando o acesso à medicina canabinoide através de informação, apoio jurídico e conexão com especialistas em todo o Brasil\.?\s*</p>',
        '<p>Facilitando o acesso à medicina canabinoide.</p>',
        content,
        flags=re.IGNORECASE | re.DOTALL
    )

    # 2. Remove 'App & Ferramentas' column in footer left over in some pages
    content = re.sub(
        r'<div class="footer-links">\s*<h4>App\s+(?:&amp;|&|E)\s+Ferramentas</h4>\s*<ul>.*?</ul>\s*</div>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    if original != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
        updated_count += 1

print(f'\nFinished sweeping {len(html_files)} files. Updated {updated_count} files.')
