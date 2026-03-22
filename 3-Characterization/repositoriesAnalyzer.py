
import os
import json
import csv
import requests
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GitHubRepositoryAnalyzer:
    def __init__(self):
        load_dotenv()
        
        self.input_dir = Path(os.getenv('RANDON_SELECTOR_OUTPUT'))
        self.output_csv = Path(os.getenv('CHARACTERIZATION_CSV_OUTPUT'))
        self.github_token = os.getenv('GITHUB_TOKEN')
        
        if not self.input_dir or not self.output_csv:
            raise ValueError("INPUT_DIR e OUTPUT_CSV devem ser definidos no arquivo .env")
        
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
    
        self.request_delay = 1  
        self.last_request_time = 0
        
        self.successful_requests = 0
        self.failed_requests = 0
    
    def safe_github_request(self, url, allow_404=False):

        try:
            time_since_last = time.time() - self.last_request_time
            if time_since_last < self.request_delay:
                time.sleep(self.request_delay - time_since_last)
            
            response = requests.get(url, headers=self.headers, timeout=30)
            self.last_request_time = time.time()
            
            if response.status_code == 403:
                remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
                reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 60))
                
                if remaining == 0:
                    wait_time = max(reset_time - time.time(), 0)
                    logger.warning(f"Rate limit atingido. Aguardando {wait_time:.0f} segundos...")
                    time.sleep(wait_time + 1)
                    return self.safe_github_request(url, allow_404)
            
            if response.status_code == 404 and allow_404:
                self.failed_requests += 1
                return None
            
            response.raise_for_status()
            self.successful_requests += 1
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            self.failed_requests += 1
            if e.response.status_code == 404 and allow_404:
                return None
            elif e.response.status_code == 404:
                logger.warning(f"Repositório não encontrado: {url}")
                return None
            elif e.response.status_code == 403:
                logger.warning(f"Acesso negado (403) para: {url}")
                return None
            else:
                logger.error(f"Erro HTTP {e.response.status_code} para {url}: {e}")
                return None
                
        except requests.exceptions.Timeout:
            self.failed_requests += 1
            logger.error(f"Timeout para {url}")
            return None
            
        except requests.exceptions.ConnectionError:
            self.failed_requests += 1
            logger.error(f"Erro de conexão para {url}")
            return None
            
        except Exception as e:
            self.failed_requests += 1
            logger.error(f"Erro inesperado para {url}: {e}")
            return None
    
    def get_repository_info(self, owner, repo_name):

        base_url = f"https://api.github.com/repos/{owner}/{repo_name}"
        
        logger.info(f"Obtendo informações para {owner}/{repo_name}")
        
        repo_data = self.safe_github_request(base_url)
        if not repo_data:
            logger.warning(f"Não foi possível obter dados básicos para {owner}/{repo_name}")
            return None
        
        languages_data = self.safe_github_request(f"{base_url}/languages", allow_404=True)
        
        contributors_data = self.safe_github_request(f"{base_url}/contributors?per_page=5", allow_404=True)
        
        releases_data = self.safe_github_request(f"{base_url}/releases/latest", allow_404=True)
        
        issues_url = f"{base_url}/issues?state=open&per_page=1"
        issues_data = self.safe_github_request(issues_url, allow_404=True)
        
        prs_url = f"{base_url}/pulls?state=open&per_page=1"
        prs_data = self.safe_github_request(prs_url, allow_404=True)
        
        commits_url = f"{base_url}/commits?per_page=1"
        commits_data = self.safe_github_request(commits_url, allow_404=True)
        
        license_data = self.safe_github_request(f"{base_url}/license", allow_404=True)
        
        readme_data = self.safe_github_request(f"{base_url}/readme", allow_404=True)
        
        forks_data = self.safe_github_request(f"{base_url}/forks?per_page=1", allow_404=True)
        
        stargazers_data = self.safe_github_request(f"{base_url}/stargazers?per_page=1", allow_404=True)
        
        languages = {}
        if languages_data and isinstance(languages_data, dict):
            languages = languages_data
        elif languages_data:
            logger.warning(f"Formato inesperado de linguagens para {owner}/{repo_name}")
        
        contributors_count = 0
        top_contributors = []
        if contributors_data and isinstance(contributors_data, list):
            contributors_count = len(contributors_data)
            top_contributors = [c.get('login', '') for c in contributors_data[:3] if c.get('login')]
        
        last_release = None
        if releases_data and isinstance(releases_data, dict) and releases_data.get('tag_name'):
            last_release = releases_data.get('tag_name')
        
        open_issues_count = 0
        if issues_data and isinstance(issues_data, list):
            if issues_data:
                pass
        open_issues_count = repo_data.get('open_issues_count', 0)
           
        open_prs_count = 0
        if prs_data and isinstance(prs_data, list):
            open_prs_count = len(prs_data)
        
       
        last_commit_date = None
        if commits_data and isinstance(commits_data, list) and commits_data:
            last_commit = commits_data[0]
            if isinstance(last_commit, dict) and last_commit.get('commit'):
                last_commit_date = last_commit.get('commit', {}).get('author', {}).get('date')
        

        license_name = None
        if license_data and isinstance(license_data, dict) and license_data.get('license'):
            license_name = license_data.get('license', {}).get('name')
        
        readme_size = 0
        if readme_data and isinstance(readme_data, dict):
            readme_size = readme_data.get('size', 0)
        
        return {
            'github_name': repo_data.get('name'),
            'github_full_name': repo_data.get('full_name'),
            'github_description': repo_data.get('description'),
            'github_stars': repo_data.get('stargazers_count'),
            'github_watchers': repo_data.get('watchers_count'),
            'github_forks': repo_data.get('forks_count'),
            'github_open_issues': repo_data.get('open_issues_count'),
            'github_size_kb': repo_data.get('size'),
            'github_created_at': repo_data.get('created_at'),
            'github_updated_at': repo_data.get('updated_at'),
            'github_pushed_at': repo_data.get('pushed_at'),
            'github_default_branch': repo_data.get('default_branch'),
            'github_private': repo_data.get('private'),
            'github_archived': repo_data.get('archived'),
            'github_disabled': repo_data.get('disabled'),
            'github_topics': ', '.join(repo_data.get('topics', [])),
            'github_homepage': repo_data.get('homepage'),
            'github_languages': ', '.join(languages.keys()) if languages else None,
            'github_language_bytes': sum(languages.values()) if languages else 0,
            'github_language_primary': max(languages.items(), key=lambda x: x[1])[0] if languages else None,
            'github_contributors_count': contributors_count,
            'github_top_contributors': ', '.join(top_contributors) if top_contributors else None,
            'github_last_release': last_release,
            'github_open_prs_count': open_prs_count,
            'github_last_commit_date': last_commit_date,
            'github_license': license_name,
            'github_readme_size': readme_size,
            'github_subscribers_count': repo_data.get('subscribers_count'),
            'github_network_count': repo_data.get('network_count'),
            'github_has_wiki': repo_data.get('has_wiki'),
            'github_has_pages': repo_data.get('has_pages'),
            'github_has_downloads': repo_data.get('has_downloads'),
            'github_has_discussions': repo_data.get('has_discussions', False),
            'github_allow_forking': repo_data.get('allow_forking'),
            'github_web_commit_signoff_required': repo_data.get('web_commit_signoff_required', False)
        }
    
    def extract_feature_files_stats(self, feature_files):
        """Extrai estatísticas dos arquivos .feature"""
        if not feature_files:
            return {
                'feature_files_count': 0,
                'feature_files_total_size': 0,
                'feature_files_avg_size': 0,
                'feature_files_min_size': 0,
                'feature_files_max_size': 0
            }
        
        sizes = [f.get('size', 0) for f in feature_files]
        return {
            'feature_files_count': len(feature_files),
            'feature_files_total_size': sum(sizes),
            'feature_files_avg_size': sum(sizes) / len(sizes) if sizes else 0,
            'feature_files_min_size': min(sizes) if sizes else 0,
            'feature_files_max_size': max(sizes) if sizes else 0
        }
    
    def process_repository(self, repo_dir):
        """Processa um único repositório"""
        json_path = repo_dir / 'repository_info.json'
        
        if not json_path.exists():
            logger.warning(f"Arquivo não encontrado: {json_path}")
            return None
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                repo_info = json.load(f)
            
            result = {
                'local_name': repo_info.get('repository_name'),
                'local_owner': repo_info.get('repository_owner'),
                'local_url': repo_info.get('repository_url'),
                'local_visibility': repo_info.get('visibility'),
                'local_is_private': repo_info.get('is_private'),
                'local_total_feature_files': repo_info.get('total_feature_files'),
                'local_downloaded_files': repo_info.get('downloaded_files'),
                'local_download_date': repo_info.get('download_date'),
                'local_status': repo_info.get('status'),
                'local_directory': str(repo_dir)
            }
            
            feature_stats = self.extract_feature_files_stats(repo_info.get('feature_files', []))
            result.update({f'local_{k}': v for k, v in feature_stats.items()})
            
            owner = repo_info.get('repository_owner')
            repo_name = repo_info.get('repository_name')
            
            if owner and repo_name:
                logger.info(f"Coletando dados do GitHub para {owner}/{repo_name}")
                github_info = self.get_repository_info(owner, repo_name)
                
                if github_info:
                    result.update(github_info)
                else:
                    logger.warning(f"Não foi possível obter dados do GitHub para {owner}/{repo_name}")

                    github_fields = self.get_github_fields()
                    for field in github_fields:
                        result[field] = None
            else:
                logger.warning(f"Owner ou nome do repositório não encontrado em {json_path}")

                github_fields = self.get_github_fields()
                for field in github_fields:
                    result[field] = None
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON em {json_path}: {e}")
            return None
        except KeyError as e:
            logger.error(f"Chave não encontrada em {json_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao processar {json_path}: {e}")
            return None
    
    def get_github_fields(self):
       
        return [
            'github_name', 'github_full_name', 'github_description', 'github_stars',
            'github_watchers', 'github_forks', 'github_open_issues', 'github_size_kb',
            'github_created_at', 'github_updated_at', 'github_pushed_at',
            'github_default_branch', 'github_private', 'github_archived',
            'github_disabled', 'github_topics', 'github_homepage', 'github_languages',
            'github_language_bytes', 'github_language_primary', 'github_contributors_count',
            'github_top_contributors', 'github_last_release', 'github_open_prs_count',
            'github_last_commit_date', 'github_license', 'github_readme_size',
            'github_subscribers_count', 'github_network_count', 'github_has_wiki',
            'github_has_pages', 'github_has_downloads', 'github_has_discussions',
            'github_allow_forking', 'github_web_commit_signoff_required'
        ]
    
    def get_csv_fields(self):
       
        local_fields = [
            'local_name', 'local_owner', 'local_url', 'local_visibility',
            'local_is_private', 'local_total_feature_files', 'local_downloaded_files',
            'local_download_date', 'local_status', 'local_directory',
            'local_feature_files_count', 'local_feature_files_total_size',
            'local_feature_files_avg_size', 'local_feature_files_min_size',
            'local_feature_files_max_size'
        ]
        
        return local_fields + self.get_github_fields()
    
    def run(self):
       
        logger.info(f"Processando repositórios em: {self.input_dir}")
        
        if not self.input_dir.exists():
            logger.error(f"Diretório de entrada não encontrado: {self.input_dir}")
            return
        
        repositories = []
        for subdir in self.input_dir.iterdir():
            if subdir.is_dir():
                json_path = subdir / 'repository_info.json'
                if json_path.exists():
                    repositories.append(subdir)
        
        logger.info(f"Encontrados {len(repositories)} repositórios para processar")
        
        all_data = []
        for i, repo_dir in enumerate(repositories, 1):
            logger.info(f"Processando {i}/{len(repositories)}: {repo_dir.name}")
            
            repo_data = self.process_repository(repo_dir)
            if repo_data:
                all_data.append(repo_data)
            else:
                logger.warning(f"Falha ao processar repositório: {repo_dir.name}")

        self.output_csv.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.output_csv, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = self.get_csv_fields()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for row in all_data:
                    writer.writerow(row)
            
            logger.info(f"\nProcessamento concluído!")
            logger.info(f"Total de repositórios processados: {len(all_data)}")
            logger.info(f"Requisições bem-sucedidas: {self.successful_requests}")
            logger.info(f"Requisições falhadas: {self.failed_requests}")
            logger.info(f"Arquivo CSV salvo em: {self.output_csv}")
            
            log_file = self.output_csv.parent / 'processamento.log'
            with open(log_file, 'w') as f:
                f.write(f"Processamento concluído em: {datetime.now()}\n")
                f.write(f"Total de repositórios: {len(repositories)}\n")
                f.write(f"Repositórios processados com sucesso: {len(all_data)}\n")
                f.write(f"Requisições bem-sucedidas: {self.successful_requests}\n")
                f.write(f"Requisições falhadas: {self.failed_requests}\n")
                f.write(f"Arquivo CSV: {self.output_csv}\n")
                
        except Exception as e:
            logger.error(f"Erro ao salvar CSV: {e}")

def main():

    try:
        analyzer = GitHubRepositoryAnalyzer()
        analyzer.run()
    except ValueError as e:
        logger.error(f"Erro de configuração: {e}")
        logger.info("\nCertifique-se de que o arquivo .env contém:")
        logger.info("INPUT_DIR=/caminho/para/diretorio/com/repositorios")
        logger.info("OUTPUT_CSV=/caminho/para/saida/resultados.csv")
        logger.info("GITHUB_TOKEN=seu_token_aqui  # opcional, mas recomendado")
        return 1
    except Exception as e:
        logger.error(f"Erro durante a execução: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())