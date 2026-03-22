from gherkin.parser import Parser
import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv

def parse_feature_file(file_path):

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        parser = Parser()
        gherkin_document = parser.parse(content)
        gherkin_document["uri"] = file_path
        
        return gherkin_document
        
    except Exception as e:
        print(f"Erro ao processar arquivo {file_path}: {e}")
        return None

def has_valid_content(elements):

    if not elements:
        return False
    
    if not elements['feature']:
        return False
    
    has_scenarios = len(elements['scenarios']) > 0
    has_scenario_outlines = len(elements['scenario_outlines']) > 0
    
    return has_scenarios or has_scenario_outlines

def extract_elements(gherkin_document):

    if not gherkin_document:
        return None
    
    elements = {
        'feature': None,
        'background': None,
        'scenarios': [],
        'scenario_outlines': [],
        'examples': [],
        'tags': [],
        'comments': []
    }
    
    feature = gherkin_document.get('feature')
    if not feature:
        return elements
    
    elements['feature'] = {
        'keyword': feature.get('keyword', ''),
        'name': feature.get('name', ''),
        'description': feature.get('description', ''),
        'language': feature.get('language', 'en'),
        'tags': extract_tags(feature.get('tags', []))
    }
    
    children = feature.get('children', [])
    for child in children:
        if 'background' in child:
            elements['background'] = extract_background(child['background'])
        elif 'scenario' in child:
            scenario = child['scenario']
            if scenario.get('examples'):
                scenario_outline = extract_scenario_outline(scenario)
                elements['scenario_outlines'].append(scenario_outline)
            else:
                scenario_data = extract_scenario(scenario)
                elements['scenarios'].append(scenario_data)
    
    elements['comments'] = extract_comments(gherkin_document.get('comments', []))
    
    return elements

def extract_tags(tags):

    return [{
        'name': tag.get('name', ''),
        'location': tag.get('location', {})
    } for tag in tags]

def extract_background(background):
    
    return {
        'keyword': background.get('keyword', ''),
        'name': background.get('name', ''),
        'steps': extract_steps(background.get('steps', [])),
        'location': background.get('location', {})
    }

def extract_scenario(scenario):
    
    return {
        'type': 'scenario',
        'keyword': scenario.get('keyword', ''),
        'name': scenario.get('name', ''),
        'description': scenario.get('description', ''),
        'steps': extract_steps(scenario.get('steps', [])),
        'tags': extract_tags(scenario.get('tags', [])),
        'location': scenario.get('location', {})
    }

def extract_scenario_outline(scenario):
    
    examples = []
    for example in scenario.get('examples', []):
        examples.append({
            'keyword': example.get('keyword', ''),
            'name': example.get('name', ''),
            'description': example.get('description', ''),
            'table_header': extract_table_row(example['tableHeader']),
            'table_body': [extract_table_row(row) for row in example.get('tableBody', [])],
            'tags': extract_tags(example.get('tags', [])),
            'location': example.get('location', {})
        })
    
    return {
        'type': 'scenario_outline',
        'keyword': scenario.get('keyword', ''),
        'name': scenario.get('name', ''),
        'description': scenario.get('description', ''),
        'steps': extract_steps(scenario.get('steps', [])),
        'tags': extract_tags(scenario.get('tags', [])),
        'examples': examples,
        'location': scenario.get('location', {})
    }

def extract_steps(steps):
   
    return [{
        'keyword': step.get('keyword', ''),
        'text': step.get('text', ''),
        'argument': extract_argument(step.get('argument')),
        'location': step.get('location', {})
    } for step in steps]

def extract_argument(argument):
   
    if not argument:
        return None
    
    if 'dataTable' in argument:
        return {
            'type': 'data_table',
            'rows': [extract_table_row(row) for row in argument['dataTable']['rows']]
        }
    elif 'docString' in argument:
        return {
            'type': 'doc_string',
            'content': argument['docString']['content'],
            'contentType': argument['docString'].get('contentType', '')
        }
    
    return None

def extract_table_row(row):
   
    return {
        'cells': [cell.get('value', '') for cell in row.get('cells', [])],
        'location': row.get('location', {})
    }

def extract_comments(comments):
  
    return [{
        'text': comment.get('text', ''),
        'location': comment.get('location', {})
    } for comment in comments]

def sanitize_filename(name):
    
    sanitized = re.sub(r'[^\w\s-]', '', name)
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    return sanitized.lower()

def save_feature_to_single_file(elements, feature_filename, output_dir):
    
    os.makedirs(output_dir, exist_ok=True)
    
    feature = elements['feature']
    if not feature:
        print("Nenhuma feature encontrada no arquivo")
        return 0
    
    base_filename = Path(feature_filename).stem
    output_file = os.path.join(output_dir, f"{base_filename}.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
       
        f.write(f"Feature: {feature['name']}\n")
        if feature['description']:
            
            description = feature['description'].strip()
            f.write(f"Description: {description}\n")
        if feature['tags']:
            f.write(f"Tags: {[tag['name'] for tag in feature['tags']]}\n")
        f.write("\n")
        
        if elements['background']:
            background = elements['background']
            f.write(f"Background: {background['name']}\n")
            for step in background['steps']:
                f.write(f"  {step['keyword']} {step['text']}\n")
                if step['argument']:
                    if step['argument']['type'] == 'data_table':
                        for row in step['argument']['rows']:
                            f.write("    | " + " | ".join(row['cells']) + " |\n")
                    elif step['argument']['type'] == 'doc_string':
                        f.write(f'    """{step["argument"]["contentType"]}\n')
                        f.write(f'{step["argument"]["content"]}\n')
                        f.write('    """\n')
            f.write("\n")
        
        scenario_count = 1
        for scenario in elements['scenarios']:
            f.write(f"Scenario {scenario_count}: {scenario['name']}\n")
            if scenario['description']:
                description = scenario['description'].strip()
                f.write(f"  Description: {description}\n")
            if scenario['tags']:
                f.write(f"  Tags: {[tag['name'] for tag in scenario['tags']]}\n")
            
            for step in scenario['steps']:
                f.write(f"  {step['keyword']} {step['text']}\n")
                if step['argument']:
                    if step['argument']['type'] == 'data_table':
                        for row in step['argument']['rows']:
                            f.write("    | " + " | ".join(row['cells']) + " |\n")
                    elif step['argument']['type'] == 'doc_string':
                        f.write(f'    """{step["argument"]["contentType"]}\n')
                        f.write(f'{step["argument"]["content"]}\n')
                        f.write('    """\n')
            f.write("\n")
            scenario_count += 1
        
        for outline in elements['scenario_outlines']:
            for example_index, example in enumerate(outline['examples'], 1):
                f.write(f"Scenario Outline {scenario_count}: {outline['name']} - Example {example_index}\n")
                if outline['description']:
                    description = outline['description'].strip()
                    f.write(f"  Description: {description}\n")
                if outline['tags'] or example['tags']:
                    all_tags = outline['tags'] + example['tags']
                    f.write(f"  Tags: {[tag['name'] for tag in all_tags]}\n")
                
                for step in outline['steps']:
                    step_text = step['text']

                    if example['table_body']:
                        for row in example['table_body']:
                            for header_cell, value_cell in zip(example['table_header']['cells'], row['cells']):
                                step_text = step_text.replace(f'<{header_cell}>', value_cell)
                    
                    f.write(f"  {step['keyword']} {step_text}\n")
                
                f.write("\n  Examples:\n")
                f.write("    | " + " | ".join(example['table_header']['cells']) + " |\n")
                for row in example['table_body']:
                    f.write("    | " + " | ".join(row['cells']) + " |\n")
                f.write("\n")
                scenario_count += 1
    
    print(f"Salvo: {output_file}")
    return scenario_count - 1  


def process_single_file(file_path, output_dir):

    print(f"Processando arquivo: {file_path}")
   
    gherkin_document = parse_feature_file(file_path)
    
    if not gherkin_document:
        print("Falha ao processar o arquivo")
        return 0, False  
    
    elements = extract_elements(gherkin_document)
    
    if not has_valid_content(elements):
        print(f"Arquivo {file_path} não contém feature ou cenários válidos. Pulando...")
        return 0, True  
    
    scenarios_count = save_feature_to_single_file(elements, os.path.basename(file_path), output_dir)
    
    print(f"Resumo do arquivo {file_path}:")
    print(f"Feature: {elements['feature']['name']}")
    print(f"Total de cenários extraídos: {scenarios_count}")
    print("-" * 50)
    
    return scenarios_count, True 

def find_feature_files(directory):

    feature_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.feature'):
                feature_files.append(os.path.join(root, file))
    return feature_files


def generate_report(report_data, output_base_dir):

    report_file = os.path.join(output_base_dir, "relatorio_geral.txt")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("RELATÓRIO GERAL DE PROCESSAMENTO DE FEATURES\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Data do processamento: {report_data['timestamp']}\n")
        f.write(f"Diretório de entrada: {report_data['input_directory']}\n")
        f.write(f"Diretório de saída: {report_data['output_directory']}\n\n")
        
        f.write("RESUMO POR DIRETÓRIO:\n")
        f.write("-" * 30 + "\n")
        
        for dir_info in report_data['directory_stats']:
            f.write(f"\nDiretório: {dir_info['directory']}\n")
            f.write(f"  - Histórias de usuário (features): {dir_info['features']}\n")
            f.write(f"  - Cenários totais: {dir_info['scenarios']}\n")
            f.write(f"  - Arquivos processados com sucesso: {dir_info['successful_files']}\n")
            f.write(f"  - Arquivos com falha no parser: {dir_info['failed_files']}\n")
            f.write(f"  - Arquivos ignorados (sem feature/cenários válidos): {dir_info['skipped_files']}\n")
        
        f.write("\n" + "=" * 50 + "\n")
        f.write("RESUMO GERAL:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total de diretórios processados: {report_data['total_directories']}\n")
        f.write(f"Total de histórias de usuário: {report_data['total_features']}\n")
        f.write(f"Total de cenários: {report_data['total_scenarios']}\n")
        f.write(f"Total de arquivos processados com sucesso: {report_data['total_successful_files']}\n")
        f.write(f"Total de arquivos com falha no parser: {report_data['total_failed_files']}\n")
        f.write(f"Total de arquivos ignorados: {report_data['total_skipped_files']}\n")
        f.write(f"Total de arquivos .feature encontrados: {report_data['total_feature_files']}\n")
    
    print(f"\nRelatório geral salvo em: {report_file}")
 


def process_directory(input_dir, output_base_dir="output"):
   
    if not os.path.exists(input_dir):
        print(f"Diretório de entrada não encontrado: {input_dir}")
        return
    
    os.makedirs(output_base_dir, exist_ok=True)
    
    report_data = {
        'timestamp': str(os.path.getctime(input_dir)),
        'input_directory': input_dir,
        'output_directory': output_base_dir,
        'directory_stats': [],
        'total_directories': 0,
        'total_features': 0,
        'total_scenarios': 0,
        'total_successful_files': 0,
        'total_failed_files': 0,
        'total_skipped_files': 0,
        'total_feature_files': 0
    }
    
    total_features = 0
    total_scenarios = 0
    total_successful_files = 0
    total_failed_files = 0
    total_skipped_files = 0
    total_feature_files = 0
    
    for root, dirs, files in os.walk(input_dir):
        
        feature_files = [f for f in files if f.endswith('.feature')]
        
        if feature_files:
           
            rel_path = os.path.relpath(root, input_dir)
            if rel_path == '.':
                output_dir = output_base_dir
            else:
                
                output_dir = os.path.join(output_base_dir, rel_path)
                os.makedirs(output_dir, exist_ok=True)
            
            repository_files = ['repository_info.json']
            for repo_file in repository_files:
                source_file = os.path.join(root, repo_file)
                if os.path.exists(source_file):
                    import shutil
                    dest_file = os.path.join(output_dir, repo_file)
                    shutil.copy2(source_file, dest_file)
                    print(f"Copiado: {source_file} -> {dest_file}")

            print(f"\nProcessando diretório: {root}")
            print(f"Arquivos .feature encontrados: {len(feature_files)}")
            print(f"Diretório de saída: {output_dir}")
            print("-" * 60)
            
            dir_features = 0
            dir_scenarios = 0
            dir_successful_files = 0
            dir_failed_files = 0
            dir_skipped_files = 0
            
            for feature_file in feature_files:
                file_path = os.path.join(root, feature_file)
                scenarios_count, success = process_single_file(file_path, output_dir)
                
                if success and scenarios_count > 0:
                    dir_features += 1
                    dir_scenarios += scenarios_count
                    dir_successful_files += 1
                elif not success:
                    dir_failed_files += 1
                else:
                    dir_skipped_files += 1
            
            total_features += dir_features
            total_scenarios += dir_scenarios
            total_successful_files += dir_successful_files
            total_failed_files += dir_failed_files
            total_skipped_files += dir_skipped_files
            total_feature_files += len(feature_files)
            
            dir_stats = {
                'directory': root,
                'features': dir_features,
                'scenarios': dir_scenarios,
                'successful_files': dir_successful_files,
                'failed_files': dir_failed_files,
                'skipped_files': dir_skipped_files,
                'total_files': len(feature_files)
            }
            report_data['directory_stats'].append(dir_stats)
            
            print(f"Resumo do diretório {root}:")
            print(f"Features processadas: {dir_features}")
            print(f"Cenários extraídos: {dir_scenarios}")
            print(f"Arquivos processados com sucesso: {dir_successful_files}")
            print(f"Arquivos com falha no parser: {dir_failed_files}")
            print(f"Arquivos ignorados (sem feature/cenários): {dir_skipped_files}")
            print("=" * 60)
    
    report_data.update({
        'total_directories': len(report_data['directory_stats']),
        'total_features': total_features,
        'total_scenarios': total_scenarios,
        'total_successful_files': total_successful_files,
        'total_failed_files': total_failed_files,
        'total_skipped_files': total_skipped_files,
        'total_feature_files': total_feature_files
    })
    
    generate_report(report_data, output_base_dir)
    
    print(f"\nRESUMO FINAL:")
    print(f"Total de diretórios processados: {len(report_data['directory_stats'])}")
    print(f"Total de features processadas: {total_features}")
    print(f"Total de cenários extraídos: {total_scenarios}")
    print(f"Total de arquivos processados com sucesso: {total_successful_files}")
    print(f"Total de arquivos com falha no parser: {total_failed_files}")
    print(f"Total de arquivos ignorados: {total_skipped_files}")
    print(f"Total de arquivos .feature encontrados: {total_feature_files}")
    print(f"Arquivos salvos em: {output_base_dir}")



if __name__ == "__main__":

    load_dotenv()

    DOWNLOADER_OUTPUT = os.getenv("DOWNLOADER_OUTPUT")

    GHERKIN_OFFICIAL_OUTPUT = os.getenv("GHERKIN_OFFICIAL_OUTPUT")

    input_directory = DOWNLOADER_OUTPUT  
    output_directory = GHERKIN_OFFICIAL_OUTPUT 
    
    process_directory(input_directory, output_directory)
    
  