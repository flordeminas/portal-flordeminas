import os
import re

def fix_site_wide(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 1. REMOVE YOUTUBE MENTION
                # Remove the YouTube <li> from the footer contact list
                content = re.sub(r'<li><a href="https://www.youtube.com/@flordeminas".*?</li>', '', content, flags=re.DOTALL)
                
                # Double check for any other youtube mentions in contact sections
                content = re.sub(r'<li><a href="[^"]*youtube.com[^"]*".*?</li>', '', content, flags=re.DOTALL)

                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Removed YouTube from: {path}")

if __name__ == "__main__":
    fix_site_wide(r"c:\Projetos\ZHC\website")
