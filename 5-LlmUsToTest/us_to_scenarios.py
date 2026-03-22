import os
import csv
from pathlib import Path
from groq import Groq
import time
import argparse
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def load_prompt_template():

    prompt_file = os.getenv('PROMPT_TEMPLATE_FILE')
    
    try:
        with open(prompt_file, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"⚠️  Arquivo de prompt não encontrado: {prompt_file}")
        return ""

def load_processed_files(log_file):
   
    processed = {"success": set(), "error": set()}
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['status'] == 'sucesso':
                    processed["success"].add((row['repo'], row['arquivo']))
                elif row['status'] == 'erro':
                    processed["error"].add((row['repo'], row['arquivo']))
    return processed

def save_to_log(log_file, repo, arquivo, status, error_msg="", start_dir=0, end_dir=0):
   
    file_exists = log_file.exists()
    
    with open(log_file, 'a', encoding='utf-8', newline='') as f:
        fieldnames = ['timestamp', 'repo', 'arquivo', 'status', 'error', 'batch_start', 'batch_end']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'timestamp': datetime.now().isoformat(),
            'repo': repo,
            'arquivo': arquivo,
            'status': status,
            'error': error_msg,
            'batch_start': start_dir,
            'batch_end': end_dir
        })


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("LLM_MODEL")
TEMPERATURE = float(os.getenv("TEMPERATURE"))
TOP_P = float(os.getenv("TOP_P"))
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
PROMPT_TEMPLATE = load_prompt_template()
INPUT_DIR = os.getenv("LLM_US_TO_TEST_INPUT_DIR")
OUTPUT_DIR = os.getenv("LLM_US_TO_TEST_OUTPUT_DIR")
LOG_FILE = Path(os.getenv("LOG_FILE", "processamento_log.csv"))


def processar_historias(start_dir=0, end_dir=None, reprocess_errors=False):
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY", GROQ_API_KEY))
    base_path = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)
    
    processed_files = load_processed_files(LOG_FILE)
    
    all_dirs = sorted([d for d in base_path.iterdir() if d.is_dir()])
    
    if end_dir is None:
        end_dir = len(all_dirs)
    dirs_to_process = all_dirs[start_dir:end_dir]
    
    print(f"Processando batch: diretórios {start_dir} a {end_dir-1}")
    print(f"Total de diretórios a processar: {len(dirs_to_process)}")
    print(f"Já processados com sucesso: {len(processed_files['success'])}")
    print(f"Com erro anterior: {len(processed_files['error'])}")
    print(f"Modelo utilizado: {MODEL}")
    print("-" * 50)
    
    for idx, repo_path in enumerate(dirs_to_process):
        repo_name = repo_path.name
        print(f"Processando repositório [{start_dir + idx}] {repo_name}")
        
        for arquivo in repo_path.glob("*_story.txt"):
            arquivo_nome = arquivo.name
            
            if (repo_name, arquivo_nome) in processed_files["success"]:
                print(f"  ⏩ Pulando (já processado): {arquivo_nome}")
                continue
            
            if not reprocess_errors and (repo_name, arquivo_nome) in processed_files["error"]:
                print(f"  ⚠️  Pulando (erro anterior): {arquivo_nome}")
                continue
            
            desc_file = arquivo.with_name(arquivo.stem.replace("_story", "_desc") + ".txt")
            
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    user_story = f.read().strip()
            except Exception as e:
                error_msg = f"Erro ao ler arquivo: {str(e)}"
                print(f"{error_msg}")
                save_to_log(LOG_FILE, repo_name, arquivo_nome, "erro", error_msg, start_dir, end_dir)
                continue

            if not user_story:
                print(f"  ⚠️  Arquivo vazio: {arquivo_nome}")
                save_to_log(LOG_FILE, repo_name, arquivo_nome, "erro", "Arquivo vazio", start_dir, end_dir)
                continue

            descricao = ""
            if desc_file.exists():
                try:
                    with open(desc_file, 'r', encoding='utf-8') as f_desc:
                        descricao = f_desc.read().strip()
                except Exception as e:
                    print(f"Erro ao ler descrição: {str(e)}")

            us = user_story.replace("Description: ", "")

            prompt = PROMPT_TEMPLATE.format(
                user_story=us,
                description=descricao
            )

            prompt_final = SYSTEM_PROMPT + prompt

            try:
                resposta = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt_final}
                    ],
                    model=MODEL,
                    temperature=TEMPERATURE,
                    top_p=TOP_P,
                    stream=False
                )

                output_repo_path = output_path / repo_name
                output_repo_path.mkdir(parents=True, exist_ok=True)
                
                arquivo_saida = output_repo_path / f"{arquivo.stem}_processado.txt"
                with open(arquivo_saida, 'w', encoding='utf-8') as f:
                    f.write(resposta.choices[0].message.content)

                print(f"Processado: {arquivo_nome}")
                save_to_log(LOG_FILE, repo_name, arquivo_nome, "sucesso", "", start_dir, end_dir)
                
                time.sleep(0.5)

            except Exception as e:
                error_msg = str(e)
                print(f"Erro na API: {arquivo_nome} - {error_msg[:100]}...")
                save_to_log(LOG_FILE, repo_name, arquivo_nome, "erro", error_msg, start_dir, end_dir)
                
                time.sleep(2)
        
        print(f"Concluído repositório: {repo_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processar histórias de usuários usando Groq API')
    parser.add_argument('--start', type=int, default=0, 
                       help='Índice do primeiro diretório a processar (padrão: 0)')
    parser.add_argument('--end', type=int, default=None,
                       help='Índice do último diretório a processar (exclusivo, padrão: todos)')
    parser.add_argument('--batch-size', type=int, default=None,
                       help='Número de diretórios para processar em cada batch')
    parser.add_argument('--reprocess-errors', action='store_true',
                       help='Reprocessar arquivos que falharam anteriormente')
    
    args = parser.parse_args()
    
    if args.batch_size is not None:
        args.end = args.start + args.batch_size
        print(f"Configuração batch: {args.start} a {args.end-1} ({args.batch_size} diretórios)")
    
    processar_historias(
        start_dir=args.start,
        end_dir=args.end,
        reprocess_errors=args.reprocess_errors
    )
    
    if LOG_FILE.exists():
        success_count = 0
        error_count = 0
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['status'] == 'sucesso':
                    success_count += 1
                else:
                    error_count += 1
        
        print(f"\n{'='*50}")
        print(f"RESUMO DO PROCESSAMENTO")
        print(f"Sucessos: {success_count}")
        print(f"Erros: {error_count}")
        print(f"Log salvo em: {LOG_FILE}")