import pandas as pd
import os

source_xlsx = r"c:\Projetos\ZHC\App\strains_database.xlsx"

def check_excel():
    if not os.path.exists(source_xlsx):
        print("Planilha não encontrada!")
        return
        
    try:
        # Forçamos a leitura sem cache e verificamos a 24k Gold
        df = pd.read_excel(source_xlsx, engine='openpyxl')
        row_24k = df[df['name'].str.lower() == '24k gold']
        
        if not row_24k.empty:
            lineage = row_24k.iloc[0]['lineage']
            print(f"VALOR NA PLANILHA: {lineage}")
        else:
            print("24k Gold não encontrada na planilha!")
    except Exception as e:
        print(f"Erro ao ler: {e}")

if __name__ == "__main__":
    check_excel()
