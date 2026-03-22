import os
import re
from pathlib import Path
from dotenv import load_dotenv

def load_env_variables():

    load_dotenv()
    
    dir_a = os.getenv('DIRETORIO_DESTINO_CONSOLIDADOS')
    dir_b = os.getenv('LLM_US_TO_TEST_OUTPUT_DIR')
    output_dir = os.getenv('CONVERSOR_FEATURES_OUTPUT')
    
    if not all([dir_a, dir_b, output_dir]):
        raise ValueError("Todas as variáveis DIR_A, DIR_B e OUTPUT_DIR devem estar definidas no arquivo .env")
    
    return Path(dir_a), Path(dir_b), Path(output_dir)

def create_output_structure(base_output_dir, dir_a_name, dir_b_name):
   
    output_dir_a = base_output_dir / dir_a_name
    output_dir_b = base_output_dir / dir_b_name
    
    output_dir_a.mkdir(parents=True, exist_ok=True)
    output_dir_b.mkdir(parents=True, exist_ok=True)
    
    return output_dir_a, output_dir_b

def sanitize_filename(filename, max_length=200):

    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    filename = re.sub(r'\s+', ' ', filename).strip()
    
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        name = name[:max_length - len(ext)]
        filename = name + ext
    
    return filename

def find_common_files(dir_a, dir_b):
    
    common_files = []
    
    if not dir_a.exists():
        print(f"Erro: Diretório A não encontrado: {dir_a}")
        return common_files
    
    if not dir_b.exists():
        print(f"Erro: Diretório B não encontrado: {dir_b}")
        return common_files
    
    files_a = {file.relative_to(dir_a).with_suffix(''): file 
               for file in dir_a.rglob('*.txt')}
    
    files_b = {file.relative_to(dir_b).with_suffix(''): file 
               for file in dir_b.rglob('*.txt')}
    
    print(f"Encontrados {len(files_a)} arquivos no diretório A")
    print(f"Encontrados {len(files_b)} arquivos no diretório B")
    
    common_keys = set(files_a.keys()) & set(files_b.keys())
    
    print(f"Encontrados {len(common_keys)} arquivos em comum")
    
    for key in common_keys:
        file_a = files_a[key].with_suffix('.txt')
        file_b = files_b[key].with_suffix('.txt')
        common_files.append((key.with_suffix('.txt'), file_a, file_b))
    
    return common_files

def convert_txt_to_feature(txt_content, original_filename):
    feature_name = original_filename.replace('.txt', '')
    feature_content = f"Feature: {feature_name}\n\n"
    
    lines = txt_content.split('\n')
    in_scenario = False
    
    for line in lines:
        trimmed_line = line.rstrip()
        
        if trimmed_line.startswith('Scenario'):
            in_scenario = True
            scenario_match = re.match(r'Scenario\s*(\d+)?\s*:?\s*(.*)', trimmed_line)
            if scenario_match:
                scenario_title = scenario_match.group(2).strip()
                if scenario_title.startswith(':'):
                    scenario_title = scenario_title[1:].strip()
                feature_content += f"Scenario: {scenario_title}\n"
            else:
                feature_content += f"{trimmed_line}\n"
        
        elif trimmed_line and in_scenario:
            if trimmed_line.strip().startswith(('Given', 'When', 'Then', 'And')):
                feature_content += f"  {trimmed_line}\n"
            else:
                feature_content += f"  {trimmed_line}\n"
        
        elif not trimmed_line and in_scenario:
            feature_content += "\n"
            in_scenario = False
        
        elif not trimmed_line and not in_scenario:
            feature_content += "\n"
    
    return feature_content

def sanitize_path_component(component, max_length=100):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        component = component.replace(char, '_')
    
    component = re.sub(r'\s+', ' ', component).strip()
    
    if len(component) > max_length:
        component = component[:max_length]
    
    return component

def process_common_files(common_files, output_dir_a, output_dir_b):
    
    processed_count = 0
    skipped_count = 0
    
    for relative_path, file_a_path, file_b_path in common_files:
        try:
           
            with open(file_a_path, 'r', encoding='utf-8', errors='ignore') as f:
                txt_content_a = f.read()
            
            output_path_parts_a = []
            for part in relative_path.parent.parts:
                sanitized_part = sanitize_path_component(part)
                output_path_parts_a.append(sanitized_part)
            
            output_file_dir_a = output_dir_a / Path(*output_path_parts_a)
            output_file_dir_a.mkdir(parents=True, exist_ok=True)
            
            sanitized_filename = sanitize_filename(relative_path.name)
            output_file_path_a = output_file_dir_a / sanitized_filename.replace('.txt', '.feature')
            
            if len(str(output_file_path_a)) > 250:
                name, ext = os.path.splitext(output_file_path_a.name)
                name = name[:50]
                output_file_path_a = output_file_path_a.with_name(f"{name}{ext}")
            
            feature_content_a = convert_txt_to_feature(txt_content_a, file_a_path.stem)
            with open(output_file_path_a, 'w', encoding='utf-8') as f:
                f.write(feature_content_a)
            
            with open(file_b_path, 'r', encoding='utf-8', errors='ignore') as f:
                txt_content_b = f.read()
            
            output_path_parts_b = []
            for part in relative_path.parent.parts:
                sanitized_part = sanitize_path_component(part)
                output_path_parts_b.append(sanitized_part)
            
            output_file_dir_b = output_dir_b / Path(*output_path_parts_b)
            output_file_dir_b.mkdir(parents=True, exist_ok=True)
            
            output_file_path_b = output_file_dir_b / sanitized_filename.replace('.txt', '.feature')
            
            if len(str(output_file_path_b)) > 250:
                name, ext = os.path.splitext(output_file_path_b.name)
                name = name[:50]
                output_file_path_b = output_file_path_b.with_name(f"{name}{ext}")
            
            feature_content_b = convert_txt_to_feature(txt_content_b, file_b_path.stem)
            with open(output_file_path_b, 'w', encoding='utf-8') as f:
                f.write(feature_content_b)
            
            processed_count += 1
            print(f"Processado: {relative_path} (arquivos A e B)")
            
        except OSError as e:
            print(f"Erro de sistema ao processar {relative_path}: {e}")
            skipped_count += 1
            continue
        except Exception as e:
            print(f"Erro inesperado ao processar {relative_path}: {e}")
            skipped_count += 1
            continue
    
    return processed_count, skipped_count

def main():
    try:
        
        dir_a, dir_b, output_dir = load_env_variables()
        
        print(f"Diretório A: {dir_a}")
        print(f"Diretório B: {dir_b}")
        print(f"Diretório de saída: {output_dir}")
        
        output_dir_a, output_dir_b = create_output_structure(output_dir, "Originais", "LLM")
        
        print("\nBuscando arquivos comuns entre diretório A e B...")
        common_files = find_common_files(dir_a, dir_b)
        
        if not common_files:
            print("Nenhum arquivo em comum encontrado entre os diretórios A e B.")
            return
        
        print(f"\nProcessando {len(common_files)} arquivos comuns...")
        processed_count, skipped_count = process_common_files(common_files, output_dir_a, output_dir_b)
        
        print(f"\nConversão concluída!")
        print(f"Arquivos processados com sucesso: {processed_count}")
        print(f"Arquivos ignorados devido a erros: {skipped_count}")
        print(f"Arquivos do diretório A salvos em: {output_dir_a}")
        print(f"Arquivos do diretório B salvos em: {output_dir_b}")
        
        all_files_a = {file.relative_to(dir_a).with_suffix('') for file in dir_a.rglob('*.txt')}
        all_files_b = {file.relative_to(dir_b).with_suffix('') for file in dir_b.rglob('*.txt')}
        
        only_in_a = all_files_a - all_files_b
        only_in_b = all_files_b - all_files_a
        
        if only_in_a:
            print(f"\nArquivos encontrados apenas no diretório A (não processados): {len(only_in_a)}")
            if len(only_in_a) <= 10: 
                for file in sorted(only_in_a):
                    print(f"  - {file.with_suffix('.txt')}")
            else:
                print(f"  (Lista muito grande para exibir)")
        
        if only_in_b:
            print(f"\nArquivos encontrados apenas no diretório B (não processados): {len(only_in_b)}")
            if len(only_in_b) <= 10:
                for file in sorted(only_in_b):
                    print(f"  - {file.with_suffix('.txt')}")
            else:
                print(f"  (Lista muito grande para exibir)")
        
    except ValueError as e:
        print(f"Erro de configuração: {e}")
        print("Certifique-se de que o arquivo .env contém:")
        print("DIR_A=/caminho/para/diretorio_A")
        print("DIR_B=/caminho/para/diretorio_B")
        print("OUTPUT_DIR=/caminho/para/output")
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()