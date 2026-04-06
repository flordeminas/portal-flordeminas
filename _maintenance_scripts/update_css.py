import os
import re

folder = '.'
pattern1 = re.compile(r'href="css/index\.css(\?v=[a-zA-Z0-9\.]+)?\"')
pattern2 = re.compile(r'href="\.\./css/index\.css(\?v=[a-zA-Z0-9\.]+)?\"')

for root, dirs, files in os.walk(folder):
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = pattern1.sub('href="css/index.css?v=2026.0406"', content)
                new_content = pattern2.sub('href="../css/index.css?v=2026.0406"', new_content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {filepath}")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
