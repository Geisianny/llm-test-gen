import os
import csv
import argparse
from pathlib import Path
from dotenv import load_dotenv



def process_csv_and_stories(csv_path, base_dir):
    mapping = {}
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
           
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                row = {k.strip(): v for k, v in row.items()}
                
                repositorio = row.get('repositorio', '').strip()
                arquivo = row.get('arquivo', '').strip()
                descricao_ingles = row.get('Descrição em inglês', '').strip()
                
                if repositorio and arquivo and descricao_ingles:
                    
                    mapping[(repositorio, arquivo)] = descricao_ingles
                
        print(f"Processado CSV: {len(mapping)} entradas carregadas")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo CSV não encontrado: {csv_path}")
        return
    except Exception as e:
        print(f"Erro ao processar CSV: {e}")
        return
    
    base_path = Path(base_dir)
    
    if not base_path.exists():
        print(f"Erro: Diretório base não encontrado: {base_dir}")
        return
    
    total_stories = 0
    desc_created = 0
    desc_skipped = 0
    
    for story_file in base_path.rglob('*_story.txt'):
        total_stories += 1
        
        repositorio_name = story_file.parent.name
        file_name = story_file.name
        
        key = (repositorio_name, file_name)
        
        if key in mapping:
            
            desc_file_name = file_name.replace('_story.txt', '_desc.txt')
            desc_file_path = story_file.parent / desc_file_name
            
            if desc_file_path.exists():
                print(f"Aviso: {desc_file_path} já existe. Sobrescrevendo.")
            
            try:
                with open(desc_file_path, 'w', encoding='utf-8') as desc_file:
                    desc_file.write(mapping[key])
                desc_created += 1
                print(f"Criado: {desc_file_path}")
                
            except Exception as e:
                print(f"Erro ao criar {desc_file_path}: {e}")
        else:
            desc_skipped += 1
            print(f"Aviso: Nenhuma descrição encontrada para {repositorio_name}/{file_name}")
    
    print(f"\n=== RESUMO ===")
    print(f"Total de arquivos _story.txt encontrados: {total_stories}")
    print(f"Arquivos _desc.txt criados: {desc_created}")
    print(f"Arquivos sem correspondência no CSV: {desc_skipped}")
    
    unused_keys = set(mapping.keys())
    for story_file in base_path.rglob('*_story.txt'):
        repositorio_name = story_file.parent.name
        file_name = story_file.name
        key = (repositorio_name, file_name)
        unused_keys.discard(key)
    
    if unused_keys:
        print(f"\nEntradas no CSV não utilizadas: {len(unused_keys)}")
        for key in unused_keys:
            print(f"  - {key[0]}/{key[1]}")

def main():
   
    load_dotenv()

    CSV_FILE = os.getenv("US_description_CSV_FILE")

    BASE_DIR = os.getenv("LLM_US_TO_TEST_INPUT_DIR")
    
    process_csv_and_stories(CSV_FILE, BASE_DIR)

if __name__ == '__main__':
    main()