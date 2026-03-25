import sys
import subprocess

try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image

# Load the image
img_path = r"c:\Projetos\ZHC\website\assets\logo_opcao_1.png"
out_path = r"c:\Projetos\ZHC\website\assets\logo_icon.png"

try:
    img = Image.open(img_path)
    width, height = img.size
    
    # We want to crop from the center to capture the main icon and omit text at the bottom.
    # Typically text is in the lower 30%. Let's grab the central 60% square.
    left = width * 0.15
    top = height * 0.15
    right = width * 0.85
    bottom = height * 0.75  # Crop out bottom 25% where text usually is
    
    img_cropped = img.crop((left, top, right, bottom))
    img_cropped.save(out_path)
    print("Logo cropped successfully!")
except Exception as e:
    print(f"Error: {e}")
