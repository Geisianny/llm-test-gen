import os
import csv
import argparse
from pathlib import Path
from dotenv import load_dotenv

def contar_arquivos_por_repositorio(diretorio, extensao=None):
   
    contagem = {}
    
    for item in Path(diretorio).iterdir():
        if item.is_dir():
            if extensao:
                arquivos = [f for f in item.iterdir() if f.is_file() and f.suffix == extensao]
            else:
                arquivos = [f for f in item.iterdir() if f.is_file()]
            contagem[item.name] = len(arquivos)
    
    return contagem

def processar_contagens(env_file):
    
    load_dotenv(env_file)
    
    user_stories_dir = os.getenv('DIRETORIO_DESTINO_HISTORIAS')
    scenarios_dir = os.getenv('DIRETORIO_DESTINO_CENARIOS')
    csv_input = os.getenv('CHARACTERIZATION_CSV_OUTPUT')
    csv_output = os.getenv('CSV_OUTPUT', csv_input)  
    user_stories_ext = os.getenv('USER_STORIES_EXTENSION', '.txt')
    scenarios_ext = os.getenv('SCENARIOS_EXTENSION', '.txt')
    
    if not user_stories_dir or not scenarios_dir or not csv_input:
        raise ValueError("USER_STORIES_DIR, SCENARIOS_DIR e CSV_INPUT devem estar definidos no arquivo .env")
    
    if not os.path.exists(user_stories_dir):
        raise FileNotFoundError(f"Diretório de user stories não encontrado: {user_stories_dir}")
    
    if not os.path.exists(scenarios_dir):
        raise FileNotFoundError(f"Diretório de cenários não encontrado: {scenarios_dir}")
    
    if not os.path.exists(csv_input):
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_input}")
    
    print(f"Contando user stories em: {user_stories_dir}")
    user_stories_count = contar_arquivos_por_repositorio(user_stories_dir, user_stories_ext)
    
    print(f"Contando cenários em: {scenarios_dir}")
    scenarios_count = contar_arquivos_por_repositorio(scenarios_dir, scenarios_ext)
    
    print(f"\nContagens encontradas:")
    print(f"User stories: {user_stories_count}")
    print(f"Cenários: {scenarios_count}")
    
    linhas_atualizadas = []
    
    with open(csv_input, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        
        novas_colunas = ['user_stories_count', 'scenarios_count']
        for coluna in novas_colunas:
            if coluna not in fieldnames:
                fieldnames.append(coluna)
        
        for linha in reader:

            repo_encontrado = False
            
            if 'github_full_name' in linha and linha['github_full_name']:
                github_full = linha['github_full_name']

                repo_dir_name = github_full.replace('/', '_')
                
                if repo_dir_name in user_stories_count or repo_dir_name in scenarios_count:
                    linha['user_stories_count'] = user_stories_count.get(repo_dir_name, 0)
                    linha['scenarios_count'] = scenarios_count.get(repo_dir_name, 0)
                    repo_encontrado = True
                    print(f"Encontrado: {github_full} -> {repo_dir_name}")
            
            if not repo_encontrado and 'local_name' in linha and linha['local_name']:
                local_name = linha['local_name']
               
                for dir_name in user_stories_count.keys():
                    if local_name.lower() in dir_name.lower():
                        linha['user_stories_count'] = user_stories_count.get(dir_name, 0)
                        linha['scenarios_count'] = scenarios_count.get(dir_name, 0)
                        repo_encontrado = True
                        print(f"Encontrado (aproximado): {local_name} -> {dir_name}")
                        break
            
            if not repo_encontrado:
                linha['user_stories_count'] = 0
                linha['scenarios_count'] = 0
                print(f"Não encontrado: {linha.get('github_full_name', linha.get('local_name', 'Desconhecido'))}")
            
            linhas_atualizadas.append(linha)
    
    with open(csv_output, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(linhas_atualizadas)
    
    print(f"\nCSV atualizado salvo em: {csv_output}")
    
    repos_com_user_stories = sum(1 for linha in linhas_atualizadas if int(linha['user_stories_count']) > 0)
    repos_com_cenarios = sum(1 for linha in linhas_atualizadas if int(linha['scenarios_count']) > 0)
    
    print(f"\nResumo:")
    print(f"Total de repositórios no CSV: {len(linhas_atualizadas)}")
    print(f"Repositórios com user stories encontrados: {repos_com_user_stories}")
    print(f"Repositórios com cenários encontrados: {repos_com_cenarios}")

def main():
    parser = argparse.ArgumentParser(description='Contar user stories e cenários por repositório e atualizar CSV')
    parser.add_argument('--env', default='.env', help='Caminho para o arquivo .env (padrão: .env)')
    
    args = parser.parse_args()
    
    try:
        processar_contagens(args.env)
        print("\nProcessamento concluído com sucesso!")
    except Exception as e:
        print(f"\nErro durante o processamento: {e}")
        exit(1)

if __name__ == "__main__":
    main()