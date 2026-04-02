import os
import time
import subprocess
import datetime

# CONFIGURAÇÕES
file_to_watch = r"c:\Projetos\ZHC\App\strains_database.xlsx"
script_to_run = r"c:\Projetos\ZHC\App\update_all.py"
project_path  = r"c:\Projetos\ZHC\App"

def get_mtime():
    try:
        if "~$" in file_to_watch: return 0
        return os.path.getmtime(file_to_watch)
    except OSError:
        return 0

def start_watch():
    print(f"👀 VIGILANTE WEB PRO V4 ATIVO: Sincronizando Local + Web...")
    last_mtime = get_mtime()
    
    while True:
        current_mtime = get_mtime()
        
        if current_mtime != last_mtime and current_mtime > 0:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] 📝 Mudança no Excel detectada!")
            
            # 1. Aguardar Excel soltar o arquivo
            time.sleep(5)
            
            try:
                # 2. Rodar o Sincronismo Local
                subprocess.run(["python", script_to_run], check=True, capture_output=True, text=True)
                print(f"[{now}] ✅ App Local atualizado!")
                
                # 3. Mandar para o GitHub (Web)
                print(f"[{now}] 🚀 Enviando para o GitHub...")
                msg = f"Auto-Sync Excel: {now}"
                subprocess.run(["git", "add", "."], cwd=project_path, check=True)
                subprocess.run(["git", "commit", "-m", msg], cwd=project_path, check=True)
                subprocess.run(["git", "push", "origin", "main"], cwd=project_path, check=True)
                
                print(f"[{now}] ✨ WEB ATUALIZADA! (Aguarde 2 min para o GitHub publicar)")
                
            except Exception as e:
                print(f"[{now}] ❌ Erro na automação: {e}")
            
            last_mtime = current_mtime
            
        time.sleep(3)

if __name__ == "__main__":
    start_watch()
