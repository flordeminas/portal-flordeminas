import json
import ast

def get_empty_strains():
    with open(r"c:\Projetos\ZHC\App\update_all.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    start_marker = "DATABASE = {"
    end_marker = "# 1. Gerar strains.js"
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    db_str = content[start_idx + len("DATABASE = "):end_idx].strip()
    if not db_str.endswith("}"): db_str = db_str[:db_str.rfind("}")+1]
    
    db = ast.literal_eval(db_str)
    
    empty_list = []
    for k, v in db.items():
        if "thc" not in v or not v["thc"]:
            empty_list.append(k)
    
    return empty_list

empty = get_empty_strains()
print(f"Total de strains para preencher: {len(empty)}")
print(json.dumps(empty))
