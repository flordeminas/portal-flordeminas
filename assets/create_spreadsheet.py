import xlsxwriter
from datetime import datetime, timedelta

def create_top_spreadsheet():
    file_path = 'planilha_mestra_cultivo.xlsx'
    workbook = xlsxwriter.Workbook(file_path)
    
    # 1. Formatting
    header_fmt = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#2e7d32', 'border': 1, 'align': 'center'})
    date_fmt = workbook.add_format({'num_format': 'dd/mm/yyyy', 'border': 1, 'align': 'center'})
    input_fmt = workbook.add_format({'bg_color': '#e8f5e9', 'border': 1, 'bold': True, 'align': 'center'})
    locked_fmt = workbook.add_format({'bg_color': '#f5f5f5', 'border': 1, 'font_color': '#757575'})
    
    # --- Tab 1: Configuração e Automátização ---
    sheet1 = workbook.add_worksheet('Configuração Inicial')
    sheet1.set_column('A:A', 30)
    sheet1.set_column('B:B', 20)
    
    sheet1.write('A1', 'PLANILHA MESTRA: CONFIGURAÇÃO', header_fmt)
    sheet1.merge_range('A1:B1', 'PLANILHA MESTRA: CONFIGURAÇÃO', header_fmt)
    
    sheet1.write('A3', 'Data de Início (Clone/Semente):')
    today = datetime.now().strftime('%d/%m/%Y')
    sheet1.write('B3', today, input_fmt)
    
    sheet1.write('A5', 'DURAÇÃO ESTIMADA (SEMANAS)', header_fmt)
    sheet1.merge_range('A5:B5', 'DURAÇÃO ESTIMADA (SEMANAS)', header_fmt)
    sheet1.write('A6', 'Fase Clone/Plântula:')
    sheet1.write('B6', 2, input_fmt)
    sheet1.write('A7', 'Fase Vegetativa:')
    sheet1.write('B7', 6, input_fmt)
    sheet1.write('A8', 'Fase Floração:')
    sheet1.write('B8', 8, input_fmt)
    
    sheet1.write('A10', 'CRONOGRAMA AUTOMATIZADO', header_fmt)
    sheet1.merge_range('A10:B10', 'CRONOGRAMA AUTOMATIZADO', header_fmt)
    sheet1.write('A11', 'Fim do Clone:')
    sheet1.write_formula('B11', '=B3+(B6*7)', date_fmt)
    sheet1.write('A12', 'Fim da Vega:')
    sheet1.write_formula('B12', '=B11+(B7*7)', date_fmt)
    sheet1.write('A13', 'Data Provável da Colheita:')
    sheet1.write_formula('B13', '=B12+(B8*7)', date_fmt)

    # --- Tab 2: Diário de Cultivo Semanal ---
    sheet2 = workbook.add_worksheet('Diário Semanal')
    sheet2.set_column('A:A', 15)
    sheet2.set_column('B:B', 15)
    sheet2.set_column('C:C', 20)
    sheet2.set_column('D:D', 40)
    sheet2.set_column('E:E', 15)
    
    headers = ['Data Início', 'Semana', 'Fase', 'Lembrete Nutrição/Ação', 'Status']
    for col, head in enumerate(headers):
        sheet2.write(0, col, head, header_fmt)
        
    for row in range(1, 21):
        sheet2.write_formula(row, 0, f"='Configuração Inicial'!$B$3+({row}-1)*7", date_fmt)
        sheet2.write(row, 1, f"Semana {row}")
        fase_formula = (
            f"=IF({row}<='Configuração Inicial'!$B$6, \"Clone\", "
            f"IF({row}<='Configuração Inicial'!$B$6+'Configuração Inicial'!$B$7, \"Vegetativo\", \"Floração\"))"
        )
        sheet2.write_formula(row, 2, fase_formula)
        reminder_formula = (
            f"=IF(C{row+1}=\"Clone\", \"Umidade Alta (70%), Luz Suave\", "
            f"IF(C{row+1}=\"Vegetativo\", \"Nitrogênio Alto, LST/Poda\", "
            f"IF(C{row+1}=\"Floração\", \"Fósforo/Potássio, Reduzir Umidade\", \"Aguardar\")))"
        )
        sheet2.write_formula(row, 3, reminder_formula)
        sheet2.data_validation(row, 4, row, 4, {'validate': 'list', 'source': ['Pendente', 'Concluído', 'Ajustar']})
        sheet2.write(row, 4, 'Pendente')

    # --- Tab 3: Manejo Orgânico (IPM) ---
    sheet3 = workbook.add_worksheet('Manejo Orgânico (IPM)')
    
    # Hidden sheet for lookup data
    sheet_data = workbook.add_worksheet('Database')
    
    pest_solutions = [
        ['Pulgão', 'Óleo de Neem (1%), Sabão de Potássio'],
        ['Mosca Branca', 'Armadilhas Amarelas, Sabão de Potássio'],
        ['Spider Mite', 'Calda Sulfocálcica, Ácaros Predadores, Óleo de Neem'],
        ['Tripes', 'Óleo de Neem, Armadilhas Azuis'],
        ['Fungos', 'Calda Bordalesa, Bicarbonato de Sódio, Vinagre Diluído'],
        ['Nenhum', 'Manter monitoramento preventivo']
    ]
    
    for row, data in enumerate(pest_solutions):
        sheet_data.write(row, 0, data[0])
        sheet_data.write(row, 1, data[1])
    
    sheet3.set_column('A:A', 15)
    sheet3.set_column('B:B', 20)
    sheet1.set_column('C:C', 50)
    sheet3.set_column('C:C', 50) # Redundancy to ensure 50
    sheet3.set_column('D:D', 20)
    
    headers3 = ['Data Incidência', 'Praga Identificada', 'Ação Sugerida (Automática)', 'Status da Ação']
    for col, head in enumerate(headers3):
        sheet3.write(0, col, head, header_fmt)
    
    for row in range(1, 11):
        # Dropdown
        sheet3.data_validation(row, 1, row, 1, {'validate': 'list', 'source': '=Database!$A$1:$A$6'})
        sheet3.write(row, 1, 'Nenhum')
        formula = f'=VLOOKUP(B{row+1}, Database!$A$1:$B$6, 2, FALSE)'
        sheet3.write_formula(row, 2, formula, locked_fmt)
        sheet3.data_validation(row, 3, row, 3, {'validate': 'list', 'source': ['Em andamento', 'Resolvido', 'Crítico']})
        sheet3.write(row, 3, 'Em andamento')

    workbook.close()
    print(f"Planilha Mestra Automática criada: {file_path}")

if __name__ == "__main__":
    create_top_spreadsheet()
