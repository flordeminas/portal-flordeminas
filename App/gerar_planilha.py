import json
import pandas as pd
import re

# Caminho do arquivo
js_file = r"c:\Projetos\ZHC\App\strains.js"
output_xlsx = r"c:\Projetos\ZHC\App\strains_database.xlsx"

try:
    with open(js_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Extrair o objeto JSON do arquivo JS
    json_match = re.search(r'const STRAIN_DB = ({.*?});', content, re.DOTALL)
    if json_match:
        json_data = json.loads(json_match.group(1))
        
        # Transformar em lista de dicionários para o Pandas
        strains_list = []
        for key, info in json_data.items():
            strains_list.append(info)

        # Criar DataFrame e ordenar por nome
        df = pd.DataFrame(strains_list)
        df = df.sort_values(by="name")

        # Salvar em Excel
        df.to_excel(output_xlsx, index=False)
        print(f"SUCESSO: Planilha gerada em {output_xlsx}!")
    else:
        print("ERRO: Não foi possível encontrar a base de dados no arquivo.")
except Exception as e:
    print(f"ERRO: {e}")
