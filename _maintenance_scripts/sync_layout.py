import os
import re

def sync_layout():
    # 1. Read source blocks from index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    footer_match = re.search(r'<footer class="site-footer">(.*?)</footer>', index_content, re.DOTALL)
    header_match = re.search(r'<header class="site-header">(.*?)</header>', index_content, re.DOTALL)
    ga_match = re.search(r'<!-- Google tag.*?/script>', index_content, re.DOTALL)
    og_favicon_match = re.search(r'<!-- Open Graph / Social Media -->.*?<!-- Favicon -->.*?<link.*?>', index_content, re.DOTALL)
    
    if not footer_match or not header_match:
        print("Could not find header or footer in index.html")
        return

    footer_source = footer_match.group(1)
    header_source = header_match.group(1)
    ga_source = ga_match.group(0) if ga_match else ""
    og_favicon_source = og_favicon_match.group(0) if og_favicon_match else ""

    # 2. Files to update
    directories = ['', 'artigos', 'guia']
    
    for directory in directories:
        prefix = '../' if directory != '' else ''
        target_dir = directory if directory != '' else '.'
        
        for filename in os.listdir(target_dir):
            if filename.endswith('.html') and filename != 'index.html' and filename != 'sync_layout.py':
                filepath = os.path.join(target_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Prepare adjusted blocks
                adj_footer = footer_source
                adj_header = header_source
                adj_ga = ga_source
                adj_og = og_favicon_source
                
                # Fix relative paths in source
                if prefix:
                    adj_footer = adj_footer.replace('src="assets/', f'src="{prefix}assets/')
                    adj_footer = adj_footer.replace('href="index.html', f'href="{prefix}index.html')
                    adj_footer = adj_footer.replace('href="noticias.html', f'href="{prefix}noticias.html')
                    adj_footer = adj_footer.replace('href="apoio-associacoes.html', f'href="{prefix}apoio-associacoes.html')
                    adj_footer = adj_footer.replace('href="eventos.html', f'href="{prefix}eventos.html')
                    adj_footer = adj_footer.replace('href="sobre-nos.html', f'href="{prefix}sobre-nos.html')
                    adj_footer = adj_footer.replace('href="parceiros.html', f'href="{prefix}parceiros.html')
                    adj_footer = adj_footer.replace('href="recursos.html', f'href="{prefix}recursos.html')

                    adj_header = adj_header.replace('src="assets/', f'src="{prefix}assets/')
                    adj_header = adj_header.replace('href="index.html', f'href="{prefix}index.html')
                    adj_header = adj_header.replace('href="noticias.html', f'href="{prefix}noticias.html')
                    adj_header = adj_header.replace('href="apoio-associacoes.html', f'href="{prefix}apoio-associacoes.html')
                    adj_header = adj_header.replace('href="eventos.html', f'href="{prefix}eventos.html')
                    adj_header = adj_header.replace('href="sobre-nos.html', f'href="{prefix}sobre-nos.html')
                    adj_header = adj_header.replace('href="parceiros.html', f'href="{prefix}parceiros.html')
                    adj_header = adj_header.replace('href="recursos.html', f'href="{prefix}recursos.html')
                    adj_header = adj_header.replace('href="#"', f'href="{prefix}index.html"')

                    adj_og = adj_og.replace('href="assets/favicon.png"', f'href="{prefix}assets/favicon.png"')
                
                # Replace Footer and Header
                content = re.sub(r'<footer>.*?</footer>', f'<footer>{adj_footer}</footer>', content, flags=re.DOTALL)
                content = re.sub(r'<header class="site-header">.*?</header>', f'<header class="site-header">{adj_header}</header>', content, flags=re.DOTALL)
                
                # Replace OG/Favicon
                if adj_og:
                    if "<!-- Open Graph" in content:
                        content = re.sub(r'<!-- Open Graph.*?<link.*?>', adj_og, content, flags=re.DOTALL)
                    else:
                        content = content.replace('</title>', f'</title>\n    {adj_og}')
                
                # Replace GA
                if adj_ga:
                    if "<!-- Google tag" in content:
                        content = re.sub(r'<!-- Google tag.*?/script>', adj_ga, content, flags=re.DOTALL)
                    else:
                        content = content.replace('</title>', f'</title>\n    {adj_ga}')
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Synced {filepath}")

sync_layout()
