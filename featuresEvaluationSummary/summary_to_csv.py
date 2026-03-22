import os
import re
import csv
from pathlib import Path
from dotenv import load_dotenv

def extract_parser_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    status_match = re.search(r'Status:\s*(VÁLIDO|INVÁLIDO)', content)
    erro_parser = 0 if status_match and status_match.group(1) == 'VÁLIDO' else 1
    
    erros_descricao = "-"
    if erro_parser == 1:
        erros_section = re.search(r'ERROS ENCONTRADOS:\s*-+([\s\S]*?)(?=\n\n|\Z)', content)
        if erros_section:
            erros = re.findall(r'\d+\.\s*(.*)', erros_section.group(1))
            erros_descricao = "\n".join([f"{i+1}. {erro}" for i, erro in enumerate(erros)])
    
    return erro_parser, erros_descricao

def extract_lint_info(file_path):
  
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    

    status_valid = "VÁLIDO (sem problemas encontrados)" in content
    status_encontrados = "ENCONTRADOS" in content and "PROBLEMAS" in content
    
    erro_lint = 0
    erros_descricao = "-"
    quantidade_problemas = 0
    
    if status_encontrados and not status_valid:
        erro_lint = 1
        
        problemas_section = re.search(r'PROBLEMAS ENCONTRADOS:\s*-+\s*(.*?)(?=AVISOS/INFORMAÇÕES ADICIONAIS:|RESUMO DOS PROBLEMAS POR TIPO:|$)', content, re.DOTALL)
        
        if problemas_section:
            problemas_text = problemas_section.group(1).strip()
            problemas_lines = problemas_text.split('\n')
            
            problemas_filtrados = []
            for line in problemas_lines:
                line_clean = line.strip()

               
                if (line_clean and 
                    not line_clean.startswith('---') and 
                    not line_clean.startswith('===') and
                    '[0;4m' not in line_clean):  
                    
                    match = re.search(r'\[38;5;243m(\d+)\s*\[0m\s*(.+?)\s*\[', line_clean)
                    if match:
                        linha_num = match.group(1)
                        mensagem = match.group(2).strip()
                        problemas_filtrados.append(f"linha {linha_num}: {mensagem}")
            
            if problemas_filtrados:
                erros_descricao = "\n".join(problemas_filtrados)
                quantidade_problemas = len(problemas_filtrados)
    
    return erro_lint, erros_descricao, quantidade_problemas

def encontrar_arquivos_relatorios(diretorio_base):
    
    arquivos_txt = []
    
    for raiz, _, arquivos in os.walk(diretorio_base):
        for arquivo in arquivos:
            if arquivo.endswith('.txt'):
                caminho_completo = os.path.join(raiz, arquivo)
               
                caminho_relativo = os.path.relpath(caminho_completo, diretorio_base)
                arquivos_txt.append((caminho_completo, caminho_relativo))
    
    return arquivos_txt

def process_directories(parser_dir, lint_dir, output_csv):
   
    results = []
    
    parser_files = encontrar_arquivos_relatorios(parser_dir)
    
    lint_files = encontrar_arquivos_relatorios(lint_dir)
    
    
    lint_map = {}
    for lint_path, lint_relativo in lint_files:
        nome_base = lint_relativo.replace('_relatorio.txt', '.txt')
        lint_map[nome_base] = (lint_path, lint_relativo)
    
   
    for parser_path, parser_relativo in parser_files:
        
        nome_base_parser = parser_relativo
        
        lint_correspondente = None
        lint_relativo_correspondente = None
        
        if nome_base_parser in lint_map:
            lint_correspondente, lint_relativo_correspondente = lint_map[nome_base_parser]
        else:
        
            nome_sem_feature = nome_base_parser.replace('.feature.txt', '.txt')
            if nome_sem_feature in lint_map:
                lint_correspondente, lint_relativo_correspondente = lint_map[nome_sem_feature]
            else:
               
                nome_arquivo = os.path.basename(nome_base_parser)
                for lint_key in lint_map.keys():
                    if os.path.basename(lint_key) == nome_arquivo:
                        lint_correspondente, lint_relativo_correspondente = lint_map[lint_key]
                        break
        
        erro_parser, erros_parser_desc = extract_parser_info(parser_path)
        
        if lint_correspondente and os.path.exists(lint_correspondente):
            erro_lint, erros_lint_desc, qtd_problemas = extract_lint_info(lint_correspondente)
        else:
            erro_lint, erros_lint_desc, qtd_problemas = 0, "-", 0
            print(f"Aviso: Arquivo lint correspondente não encontrado para {parser_relativo}")
        
        if nome_base_parser.endswith('.feature.txt'):
            nome_feature = nome_base_parser[:-12]  
        elif nome_base_parser.endswith('.txt'):
            nome_feature = nome_base_parser[:-4]  
        else:
            nome_feature = nome_base_parser
        
        results.append({
            'arquivo': nome_feature,
            'caminho_relativo': os.path.dirname(parser_relativo) if os.path.dirname(parser_relativo) else '.',
            'erro_parser': erro_parser,
            'erro_lint': erro_lint,
            'erros_parser_descricao': erros_parser_desc,
            'erros_lint_descricao': erros_lint_desc,
            'quantidade_problemas_lint': qtd_problemas,
            'arquivo_parser': parser_relativo,
            'arquivo_lint': lint_relativo_correspondente if lint_relativo_correspondente else "NÃO ENCONTRADO"
        })
    
    results.sort(key=lambda x: (x['caminho_relativo'], x['arquivo']))
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['arquivo', 'caminho_relativo', 'erro_parser', 'erro_lint', 
                     'erros_parser_descricao', 'erros_lint_descricao', 
                     'quantidade_problemas_lint', 'arquivo_parser', 'arquivo_lint']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in results:
            
            row_escaped = {
                'arquivo': row['arquivo'],
                'caminho_relativo': row['caminho_relativo'],
                'erro_parser': row['erro_parser'],
                'erro_lint': row['erro_lint'],
                'erros_parser_descricao': row['erros_parser_descricao'].replace('\n', '\\n'),
                'erros_lint_descricao': row['erros_lint_descricao'].replace('\n', '\\n'),
                'quantidade_problemas_lint': row['quantidade_problemas_lint'],
                'arquivo_parser': row['arquivo_parser'],
                'arquivo_lint': row['arquivo_lint']
            }
            writer.writerow(row_escaped)
    
    total_parser = len(parser_files)
    total_lint = len(lint_files)
    total_match = sum(1 for r in results if r['arquivo_lint'] != "NÃO ENCONTRADO")
    
    print(f"\n=== RELATÓRIO GERADO COM SUCESSO ===")
    print(f"Arquivo CSV: {output_csv}")
    print(f"Total de arquivos de parser encontrados: {total_parser}")
    print(f"Total de arquivos de lint encontrados: {total_lint}")
    print(f"Total de correspondências encontradas: {total_match}")
    print(f"Total de arquivos processados no CSV: {len(results)}")

if __name__ == "__main__":
    
    load_dotenv()

    PARSER_DIR = os.getenv('PARSER_GHERKIN_SCENARIO_ORIGINAIS')      
    LINT_DIR = os.getenv('GHERKIN_LINT_SCENARIO_ORIGINAIS')         
    OUTPUT_CSV = os.getenv('FEATURES_ORIGINAIS_CSV')
    

    if not os.path.exists(PARSER_DIR):
        print(f"Erro: Diretório {PARSER_DIR} não encontrado!")
    elif not os.path.exists(LINT_DIR):
        print(f"Erro: Diretório {LINT_DIR} não encontrado!")
    else:
        process_directories(PARSER_DIR, LINT_DIR, OUTPUT_CSV)