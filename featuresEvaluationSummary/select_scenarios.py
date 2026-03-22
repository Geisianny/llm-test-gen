

import os
import re
import csv
import random
from pathlib import Path
from dotenv import load_dotenv

def load_environment():
   
    load_dotenv()
    
    entrada_dir = os.getenv('LLM_US_TO_TEST_OUTPUT_DIR')
    saida_dir = os.getenv('OUTPUT_SELECTED_SCENARIOS')
    
    if not entrada_dir or not saida_dir:
        raise ValueError("As variáveis ENTRADA_DIR e SAIDA_DIR devem ser definidas no arquivo .env")
    
    return Path(entrada_dir), Path(saida_dir)

def extract_scenarios(content):
   
    scenarios = []
    
    lines = content.strip().split('\n')
    
    current_scenario = []
    in_scenario = False
    
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        
        if stripped_line.startswith('Scenario:') or stripped_line.startswith('Scenario Outline:'):
           
            if in_scenario and current_scenario:
                scenarios.append('\n'.join(current_scenario))
                current_scenario = []
            
            in_scenario = True
            current_scenario.append(line)
        
        
        elif in_scenario:
           
            if stripped_line == '':
               
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line.startswith('Scenario:') or next_line.startswith('Scenario Outline:'):
                       
                        if current_scenario:
                            scenarios.append('\n'.join(current_scenario))
                            current_scenario = []
                        in_scenario = False
                    else:
                        current_scenario.append(line)
                else:
                    
                    if current_scenario:
                        scenarios.append('\n'.join(current_scenario))
            else:
               
                current_scenario.append(line)
    
    if current_scenario:
        scenarios.append('\n'.join(current_scenario))
    
    cleaned_scenarios = []
    for scenario in scenarios:
        lines = scenario.strip().split('\n')
        cleaned = '\n'.join(lines)
        if cleaned:
            cleaned_scenarios.append(cleaned)
    
    return cleaned_scenarios

def get_scenario_name(scenario_content):
    
    first_line = scenario_content.strip().split('\n')[0]
    
    match = re.search(r'Scenario(?: Outline)?:\s*(.+)', first_line)
    if match:
        return match.group(1).strip()
    
    return "Cenário sem nome"

def process_file(file_path, relative_path, entrada_dir, saida_dir, csv_writer):
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        scenarios = extract_scenarios(content)
        
        if not scenarios:
            print(f"Nenhum cenário encontrado em {file_path}")
            return
        
        selected_scenario = random.choice(scenarios)
        scenario_number = scenarios.index(selected_scenario) + 1
        
        scenario_name = get_scenario_name(selected_scenario)
        
        output_file_path = saida_dir / relative_path
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(selected_scenario)
        
        csv_writer.writerow({
            'arquivo': file_path.name,
            'repositorio': relative_path.parent.name if relative_path.parent.name else 'raiz',
            'cenario_numero': f'cenário {scenario_number}',
            'nome_cenario': scenario_name,
            'caminho_completo': str(relative_path)
        })
        
        print(f"Processado: {relative_path} | Cenário selecionado: {scenario_number}")
        
    except Exception as e:
        print(f"Erro ao processar {file_path}: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    try:
        entrada_dir, saida_dir = load_environment()
        
        if not entrada_dir.exists():
            raise FileNotFoundError(f"Diretório de entrada não encontrado: {entrada_dir}")
        
        saida_dir.mkdir(parents=True, exist_ok=True)
        
        csv_path = saida_dir / 'cenarios_selecionados.csv'
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['arquivo', 'repositorio', 'cenario_numero', 'nome_cenario', 'caminho_completo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            txt_files = list(entrada_dir.rglob('*.txt'))
            
            if not txt_files:
                print(f"Nenhum arquivo .txt encontrado em {entrada_dir}")
                return
            
            print(f"Encontrados {len(txt_files)} arquivos .txt para processar")
            
            for txt_file in txt_files:
                relative_path = txt_file.relative_to(entrada_dir)
                process_file(txt_file, relative_path, entrada_dir, saida_dir, writer)
        
        print(f"\nProcessamento concluído!")
        print(f"Diretório de saída: {saida_dir}")
        print(f"CSV gerado: {csv_path}")
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())