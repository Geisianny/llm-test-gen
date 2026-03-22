import os
import csv
import requests
import time
from urllib.parse import urlparse
import json
from pathlib import Path
from dotenv import load_dotenv
import glob

class GitHubFeatureDownloader:

    def __init__(self, csv_file, output_dir="repositories", start_index=0, end_index=None, progress_file="download_progress.json", token):
        self.csv_file = csv_file
        self.output_dir = output_dir
        self.start_index = start_index
        self.end_index = end_index
        self.progress_file = progress_file
        
        self.downloaded_repos = self.load_progress()
        
        self.session = requests.Session()
     
        self.session.headers.update({
            'User-Agent': 'Python-Script-Feature-Downloader',
            'Accept': 'application/vnd.github.v3+json'
        })
        
        self.github_token = token
        if self.github_token:
            self.session.headers.update({
                'Authorization': f'token {self.github_token}'
            })
        
        self.rate_limit_remaining = 60 
        self.rate_limit_reset = 0
        
    def load_progress(self):
       
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return set(json.load(f))
            except:
                return set()
        return set()
    
    def save_progress(self):
       
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.downloaded_repos), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar progresso: {e}")
    
    def add_downloaded_repo(self, repo_url):
        
        self.downloaded_repos.add(repo_url.strip().lower())
        self.save_progress()
    
    def is_repo_downloaded(self, repo_url):
        
        return repo_url.strip().lower() in self.downloaded_repos
    
    def check_rate_limit(self):
        
        if self.rate_limit_remaining <= 10:
            wait_time = max(self.rate_limit_reset - time.time(), 0) + 10
            if wait_time > 0:
                print(f"Rate limit atingido. Aguardando {wait_time:.0f} segundos...")
                time.sleep(wait_time)
          
                self.rate_limit_remaining = 60
    
    def update_rate_limit(self, response):
       
        if 'X-RateLimit-Remaining' in response.headers:
            self.rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
        if 'X-RateLimit-Reset' in response.headers:
            self.rate_limit_reset = int(response.headers['X-RateLimit-Reset'])
    
    def make_github_request(self, url):
        
        self.check_rate_limit()
        
        try:
            response = self.session.get(url, timeout=30)
            self.update_rate_limit(response)
            
            if response.status_code == 403:
                print(f"Acesso negado (403) para: {url}")
                print("Motivo possível: Rate limit excedido ou repositório privado")
                return None
            elif response.status_code == 404:
                print(f"Recurso não encontrado (404): {url}")
                return None
            elif response.status_code == 200:
                return response
            else:
                print(f"Erro HTTP {response.status_code} para: {url}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão para {url}: {e}")
            return None
    
    def get_repo_info(self, repo_url):
       
        parsed_url = urlparse(repo_url)
        path_parts = parsed_url.path.strip('/').split('/')
        
        if len(path_parts) >= 2:
            owner = path_parts[0]
            repo_name = path_parts[1]
            return owner, repo_name
        return None, None
    
    def get_github_api_url(self, owner, repo_name, path=""):
        
        return f"https://api.github.com/repos/{owner}/{repo_name}/contents/{path}"
    
    def download_file(self, url, file_path):
        
        try:
            response = self.session.get(url, stream=True, timeout=30)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            else:
                print(f"Erro {response.status_code} ao baixar {url}")
                return False
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")
            return False
    
    def get_repo_visibility(self, owner, repo_name):
       
        url = f"https://api.github.com/repos/{owner}/{repo_name}"
        response = self.make_github_request(url)
        
        if response:
            try:
                repo_data = response.json()
                return repo_data.get('private', False), repo_data.get('visibility', 'unknown')
            except:
                return False, 'unknown'
        return False, 'unknown'
    
    def find_feature_files(self, owner, repo_name, path=""):
       
        feature_files = []
        
        api_url = self.get_github_api_url(owner, repo_name, path)
        response = self.make_github_request(api_url)
        
        if not response:
            return feature_files
        
        try:
            contents = response.json()
            
            if isinstance(contents, list):
                for item in contents:
                    if item.get('type') == 'file' and item.get('name', '').endswith('.feature'):
                        feature_files.append({
                            'name': item['name'],
                            'path': item['path'],
                            'download_url': item.get('download_url', ''),
                            'size': item.get('size', 0),
                            'sha': item.get('sha', '')
                        })
                    elif item.get('type') == 'dir':
                        
                        sub_files = self.find_feature_files(owner, repo_name, item['path'])
                        feature_files.extend(sub_files)
            
            time.sleep(0.2)
                    
        except ValueError as e:
            print(f"Erro ao decodificar JSON de {api_url}: {e}")
        except Exception as e:
            print(f"Erro ao processar conteúdo de {api_url}: {e}")
        
        return feature_files
    
    def download_repository_features(self, repo_url):

        owner, repo_name = self.get_repo_info(repo_url)
        
        if not owner or not repo_name:
            print(f"URL inválida: {repo_url}")
            return None
        
        print(f"\nProcessando repositório: {owner}/{repo_name}")
        
        is_private, visibility = self.get_repo_visibility(owner, repo_name)
        if is_private:
            print(f"Repositório {owner}/{repo_name} é privado. Pulando...")
            return None
        
        repo_dir = os.path.join(self.output_dir, f"{owner}_{repo_name}")
        os.makedirs(repo_dir, exist_ok=True)
        
        print("Buscando arquivos .feature...")
        feature_files = self.find_feature_files(owner, repo_name)
        
        if not feature_files:
            print("Nenhum arquivo .feature encontrado.")
        
        downloaded_files = []
        for file_info in feature_files:
            if not file_info.get('download_url'):
                print(f"URL de download não disponível para: {file_info['path']}")
                continue
            
            file_name = file_info['name']
            file_path = os.path.join(repo_dir, file_name)
            
            counter = 1
            original_file_path = file_path
            while os.path.exists(file_path):
                base_name = Path(file_name).stem
                extension = Path(file_name).suffix
                file_path = os.path.join(repo_dir, f"{base_name}_{counter}{extension}")
                counter += 1
            
            print(f"Baixando: {file_info['path']}")
            if self.download_file(file_info['download_url'], file_path):
                downloaded_files.append({
                    'name': os.path.basename(file_path),
                    'original_path': file_info['path'],
                    'size': file_info['size'],
                    'sha': file_info['sha']
                })
            
            time.sleep(0.1)
        
        info_data = {
            'repository_name': repo_name,
            'repository_owner': owner,
            'repository_url': repo_url,
            'visibility': visibility,
            'is_private': is_private,
            'total_feature_files': len(feature_files),
            'downloaded_files': len(downloaded_files),
            'download_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'feature_files': downloaded_files,
            'status': 'success' if downloaded_files else 'no_files_found'
        }
        
        info_file = os.path.join(repo_dir, 'repository_info.json')
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info_data, f, indent=2, ensure_ascii=False)
        
        txt_file = os.path.join(repo_dir, 'repository_info.txt')
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"INFORMAÇÕES DO REPOSITÓRIO\n")
            f.write(f"=" * 50 + "\n\n")
            f.write(f"Nome: {repo_name}\n")
            f.write(f"Proprietário: {owner}\n")
            f.write(f"URL: {repo_url}\n")
            f.write(f"Visibilidade: {visibility}\n")
            f.write(f"Privado: {'Sim' if is_private else 'Não'}\n")
            f.write(f"Data: {info_data['download_date']}\n")
            f.write(f"Arquivos .feature encontrados: {len(feature_files)}\n")
            f.write(f"Arquivos baixados: {len(downloaded_files)}\n")
            f.write(f"Status: {info_data['status']}\n\n")
            
            if downloaded_files:
                f.write(f"ARQUIVOS BAIXADOS\n")
                f.write(f"-" * 30 + "\n")
                for file in downloaded_files:
                    f.write(f"• {file['name']} ({file['size']} bytes)\n")
                    f.write(f"  Path original: {file['original_path']}\n")
                    f.write(f"  SHA: {file['sha']}\n\n")
        
        self.add_downloaded_repo(repo_url)
        
        return info_data
    
    def process_csv(self):
        
        repositories_info = []
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                
                if self.end_index is None or self.end_index > len(rows):
                    self.end_index = len(rows)
                
                start = max(0, self.start_index - 1)
                end = min(len(rows), self.end_index)
                
                print(f"Encontrados {len(rows)} repositórios no CSV")
                print(f"Processando repositórios de {start + 1} a {end}")
                
                for i in range(start, end):
                    repo_url = rows[i].get('url')
                    if repo_url and repo_url.strip():
                        
                        if self.is_repo_downloaded(repo_url):
                            print(f"\n[{i + 1}/{len(rows)}] Repositório já baixado: {repo_url.strip()}")
                            continue
                            
                        print(f"\n[{i + 1}/{len(rows)}] Processando: {repo_url.strip()}")
                        info = self.download_repository_features(repo_url.strip())
                        if info:
                            repositories_info.append(info)
                        
                        time.sleep(1)
                    else:
                        print(f"[{i + 1}/{len(rows)}] Linha sem URL válida, pulando...")
        
        except FileNotFoundError:
            print(f"Arquivo CSV não encontrado: {self.csv_file}")
        except Exception as e:
            print(f"Erro ao processar CSV: {e}")
        
        self.create_summary_report(repositories_info)
        
        return repositories_info
    
    def create_summary_report(self, repositories_info):
        
        summary_file = os.path.join(self.output_dir, 'summary_report.txt')
        
        successful = [r for r in repositories_info if r.get('downloaded_files', 0) > 0]
        no_files = [r for r in repositories_info if r.get('downloaded_files', 0) == 0]
        private_repos = [r for r in repositories_info if r.get('is_private', False)]
        
        total_repos = len(repositories_info)
        total_features_found = sum(repo.get('total_feature_files', 0) for repo in repositories_info)
        total_features_downloaded = sum(repo.get('downloaded_files', 0) for repo in repositories_info)
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DETALHADO - DOWNLOAD DE ARQUIVOS .FEATURE\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("ESTATÍSTICAS GERAIS\n")
            f.write("-" * 50 + "\n")
            f.write(f"Range processado: {self.start_index} a {self.end_index}\n")
            f.write(f"Total de repositórios processados: {total_repos}\n")
            f.write(f"Repositórios com arquivos baixados: {len(successful)}\n")
            f.write(f"Repositórios sem arquivos .feature: {len(no_files)}\n")
            f.write(f"Repositórios privados: {len(private_repos)}\n")
            f.write(f"Total de arquivos .feature encontrados: {total_features_found}\n")
            f.write(f"Total de arquivos .feature baixados: {total_features_downloaded}\n")
            f.write(f"Taxa de sucesso: {(len(successful)/total_repos*100 if total_repos > 0 else 0):.1f}%\n")
            f.write(f"Data do processamento: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("DETALHES POR REPOSITÓRIO\n")
            f.write("-" * 50 + "\n\n")
            
            for i, repo in enumerate(repositories_info, 1):
                status = "✓ SUCESSO" if repo.get('downloaded_files', 0) > 0 else "✗ SEM ARQUIVOS"
                if repo.get('is_private', False):
                    status = "🔒 PRIVADO"
                
                f.write(f"{i:3d}. {status} - {repo.get('repository_owner', '')}/{repo.get('repository_name', '')}\n")
                f.write(f"     URL: {repo.get('repository_url', '')}\n")
                f.write(f"     Visibilidade: {repo.get('visibility', 'unknown')}\n")
                f.write(f"     Arquivos .feature: {repo.get('downloaded_files', 0)}/{repo.get('total_feature_files', 0)} baixados\n")
                f.write(f"     Data do download: {repo.get('download_date', 'N/A')}\n")
                f.write(f"     Pasta local: {repo.get('repository_owner', '')}_{repo.get('repository_name', '')}\n")
                
                if repo.get('downloaded_files', 0) > 0:
                    f.write(f"     Arquivos:\n")
                    for file in repo.get('feature_files', []):
                        f.write(f"       • {file.get('name', '')} ({file.get('size', 0)} bytes)\n")
                
                f.write("-" * 70 + "\n")
            
            f.write("\nRESUMO FINAL\n")
            f.write("-" * 50 + "\n")
            f.write(f"RANGE PROCESSADO: {self.start_index} a {self.end_index}\n")
            f.write(f"TOTAL DE REPOSITÓRIOS: {total_repos}\n")
            f.write(f"TOTAL DE ARQUIVOS .FEATURE ENCONTRADOS: {total_features_found}\n")
            f.write(f"TOTAL DE ARQUIVOS .FEATURE BAIXADOS: {total_features_downloaded}\n")
            f.write(f"DATA DO PROCESSAMENTO: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"DIRETÓRIO DE SAÍDA: {os.path.abspath(self.output_dir)}\n\n")
            
            if successful:
                f.write("TOP 5 REPOSITÓRIOS COM MAIS ARQUIVOS .FEATURE\n")
                f.write("-" * 50 + "\n")
                top_repos = sorted(successful, key=lambda x: x.get('downloaded_files', 0), reverse=True)[:5]
                for j, repo in enumerate(top_repos, 1):
                    f.write(f"{j:2d}. {repo.get('repository_owner', '')}/{repo.get('repository_name', '')}: ")
                    f.write(f"{repo.get('downloaded_files', 0)} arquivos\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("PROCESSAMENTO CONCLUÍDO COM SUCESSO!\n")
            f.write("=" * 80 + "\n")

        summary_json = {
            'summary': {
                'range_processed': f"{self.start_index} to {self.end_index}",
                'total_repositories': total_repos,
                'repositories_with_files': len(successful),
                'repositories_without_files': len(no_files),
                'private_repositories': len(private_repos),
                'total_features_found': total_features_found,
                'total_features_downloaded': total_features_downloaded,
                'success_rate': (len(successful)/total_repos*100 if total_repos > 0 else 0),
                'processing_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'output_directory': os.path.abspath(self.output_dir)
            },
            'repositories': repositories_info
        }
        
        summary_json_file = os.path.join(self.output_dir, 'summary_report.json')
        with open(summary_json_file, 'w', encoding='utf-8') as f:
            json.dump(summary_json, f, indent=2, ensure_ascii=False)
        
        print(f"Relatórios gerados: {summary_file} e {summary_json_file}")

def get_latest_csv(directory_path):
    
    pattern = os.path.join(directory_path, "github_feature_repos_*.csv")
    
    csv_files = glob.glob(pattern)
    
    if not csv_files:
        raise FileNotFoundError(f"Nenhum arquivo CSV encontrado em {directory_path}")
    
    latest_file = max(csv_files, key=os.path.getmtime)
    
    return latest_file

def main():
    load_dotenv()

    GITHUBSEARCH_OUTPUT = os.getenv("GITHUBSEARCH_OUTPUT")

    DOWNLOADER_OUTPUT = os.getenv("DOWNLOADER_OUTPUT")

    TOKEN = os.getenv("GITHUB_TOKEN")
    
    csv_file = get_latest_csv(GITHUBSEARCH_OUTPUT) 

    output_dir = DOWNLOADER_OUTPUT
    
    print("GitHub Feature Downloader")
    print("=" * 30)

    try:
        start = int(input("Digite o índice inicial (1 para o primeiro): ") or "1")
        end_input = input("Digite o índice final (Enter para todos): ")
        end = int(end_input) if end_input else None
    except ValueError:
        print("Entrada inválida. Usando range padrão (todos os repositórios).")
        start = 1
        end = None
    
    start = start -1
    end = end - 1
    downloader = GitHubFeatureDownloader(csv_file, output_dir, start_index=start, end_index=end, TOKEN)
    results = downloader.process_csv()
    
    print(f"Processamento concluído!")
    print(f"   Range processado: {start} a {end if end else 'final'}")
    print(f"   Repositórios processados: {len(results)}")
    print(f"   Arquivos salvos em: {output_dir}")
    print(f"   Verifique o arquivo {output_dir}/summary_report.txt para detalhes")

if __name__ == "__main__":
    main()