import os
import csv
import requests
import time
from pathlib import Path
from collections import defaultdict
import json
from dotenv import load_dotenv

class GitHubRepositoryAnalyzer:
    def __init__(self, token=None):
       
        self.base_url = "https://api.github.com/repos"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Repository-Analyzer"
        }
        
        if token:
            self.headers["Authorization"] = f"token {token}"
        
        self.cache = {}
    
    def parse_repository_info(self, file_path):
        
        repo_info = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        repo_info[key] = value
        except Exception as e:
            print(f"Erro ao ler arquivo {file_path}: {e}")
            return None
        
        return repo_info
    
    def extract_owner_repo_from_url(self, url):
     
        try:
            parts = url.replace('https://github.com/', '').split('/')
            if len(parts) >= 2:
                return parts[0], parts[1]
        except:
            pass
        return None, None
    
    def make_github_request(self, url, max_retries=3):
        
        if url in self.cache:
            return self.cache[url]
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    data = response.json()
                    self.cache[url] = data
                    return data
                elif response.status_code == 202:
                    
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  
                        continue
                elif response.status_code == 204:
                    return None
                elif response.status_code == 404:
                   
                    return None
                elif response.status_code == 422:
                    return None
                elif response.status_code == 403:
                    reset_time = response.headers.get('X-RateLimit-Reset')
                    if reset_time:
                        sleep_time = int(reset_time) - time.time() + 10
                        if sleep_time > 0:
                            print(f"Rate limit excedido. Aguardando {sleep_time} segundos...")
                            time.sleep(sleep_time)
                            continue
                    return None
                else:
                    print(f"Erro na requisição {url}: {response.status_code}")
                    return None
                    
            except Exception as e:
                print(f"Exceção na requisição {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
        
        return None
    
    def get_commit_activity_stats(self, owner, repo_name):
       
        stats = {
            'total_commits_last_year': 0,
            'weekly_commit_activity': [],
            'commit_activity_52_weeks': {'all': [], 'owner': []},
            'contributors_commit_stats': []
        }
        
        try:
            activity_url = f"{self.base_url}/{owner}/{repo_name}/stats/commit_activity"
            activity_data = self.make_github_request(activity_url)
            
            if activity_data:
                stats['total_commits_last_year'] = sum(week.get('total', 0) for week in activity_data)
                stats['weekly_commit_activity'] = activity_data
            
            time.sleep(0.5)
            
            participation_url = f"{self.base_url}/{owner}/{repo_name}/stats/participation"
            participation_data = self.make_github_request(participation_url)
            
            if participation_data:
                stats['commit_activity_52_weeks'] = participation_data
            
            time.sleep(0.5)
            
            contributors_url = f"{self.base_url}/{owner}/{repo_name}/stats/contributors"
            contributors_data = self.make_github_request(contributors_url)
            
            if contributors_data:
                stats['contributors_commit_stats'] = contributors_data
                
                if contributors_data:
                    stats['active_contributors_count'] = len(contributors_data)
                    
            
            time.sleep(0.5)
            
            code_freq_url = f"{self.base_url}/{owner}/{repo_name}/stats/code_frequency"
            code_freq_data = self.make_github_request(code_freq_url)
            
            punch_card_url = f"{self.base_url}/{owner}/{repo_name}/stats/punch_card"
            
        except Exception as e:
            print(f"Erro ao coletar estatísticas de commits para {owner}/{repo_name}: {e}")
        
        return stats
    
    def get_repository_data(self, owner, repo_name):

        cache_key = f"{owner}/{repo_name}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        repo_data = defaultdict(lambda: None)
        
        try:
            repo_url = f"{self.base_url}/{owner}/{repo_name}"
            repo_info = self.make_github_request(repo_url)
            
            if not repo_info:
                return None
            
            repo_data['full_name'] = repo_info.get('full_name')
            repo_data['description'] = repo_info.get('description', '')
            repo_data['html_url'] = repo_info.get('html_url')

            repo_data['stargazers_count'] = repo_info.get('stargazers_count', 0)
            repo_data['forks_count'] = repo_info.get('forks_count', 0)

            repo_data['watchers_count'] = repo_info.get('watchers_count', 0)
            repo_data['size'] = repo_info.get('size', 0)  
            repo_data['created_at'] = repo_info.get('created_at')
            repo_data['updated_at'] = repo_info.get('updated_at')
 
            repo_data['license'] = repo_info.get('license', {}).get('name', '')

            repo_data['has_issues'] = repo_info.get('has_issues', False)
            repo_data['has_projects'] = repo_info.get('has_projects', False)
            repo_data['has_wiki'] = repo_info.get('has_wiki', False)
            repo_data['has_downloads'] = repo_info.get('has_downloads', False)
            repo_data['has_pages'] = repo_info.get('has_pages', False)
            
            repo_data['kloc_estimate'] = round(repo_data['size'] / 10, 2)
            
            time.sleep(0.5)
            
            languages_url = f"{self.base_url}/{owner}/{repo_name}/languages"
            languages_data = self.make_github_request(languages_url)
            
            if languages_data:
                repo_data['languages_json'] = json.dumps(languages_data)

                repo_data['main_language'] = max(languages_data, key=languages_data.get) if languages_data else ''
                
                if languages_data:
                    total_bytes = sum(languages_data.values())
                    main_language_bytes = languages_data[repo_data['main_language']]
            else:
                repo_data['languages_json'] = '{}'
                repo_data['main_language'] = ''
            
            time.sleep(0.5)
            
            contributors_url = f"{self.base_url}/{owner}/{repo_name}/contributors?per_page=1"
            contributors_response = requests.get(contributors_url, headers=self.headers)
            
            if contributors_response.status_code == 200:
                link_header = contributors_response.headers.get('Link', '')
                if 'rel="last"' in link_header:
                    last_page = int(link_header.split('page=')[-1].split('>')[0])
                    
                else:
                    contributors = contributors_response.json()
                
            time.sleep(0.5)
            
            commits_url = f"{self.base_url}/{owner}/{repo_name}/commits?per_page=1"
            commits_response = requests.get(commits_url, headers=self.headers)
            
            if commits_response.status_code == 200:
                link_header = commits_response.headers.get('Link', '')
                if 'rel="last"' in link_header:
                    last_page = int(link_header.split('page=')[-1].split('>')[0])
                    repo_data['commits_count'] = last_page
                else:
                    commits = commits_response.json()
                    repo_data['commits_count'] = len(commits) if isinstance(commits, list) else 0
            else:
                repo_data['commits_count'] = 0
            
            time.sleep(0.5)
            
            releases_url = f"{self.base_url}/{owner}/{repo_name}/releases"
            releases_data = self.make_github_request(releases_url)
            
            if releases_data:
                repo_data['releases_count'] = len(releases_data)
                if releases_data:
                    latest_release = releases_data[0]
                    repo_data['latest_release_date'] = latest_release.get('published_at', '')
            else:
                repo_data['releases_count'] = 0
                repo_data['latest_release'] = ''
                repo_data['latest_release_date'] = ''
            
            time.sleep(0.5)

            commit_stats = self.get_commit_activity_stats(owner, repo_name)
            repo_data.update(commit_stats)
            
            self._calculate_derived_metrics(repo_data)
            
            self.cache[cache_key] = repo_data
            
        except Exception as e:
            print(f"Erro ao coletar dados para {owner}/{repo_name}: {e}")
            return None
        
        return repo_data
    
    def _calculate_derived_metrics(self, repo_data):
       
        try:
            if repo_data['created_at']:
                from datetime import datetime
                created = datetime.fromisoformat(repo_data['created_at'].replace('Z', '+00:00'))
                now = datetime.now().astimezone(created.tzinfo)
            if repo_data.get('commit_activity_52_weeks', {}).get('all'):
                recent_commits = sum(repo_data['commit_activity_52_weeks']['all'][-4:])
                repo_data['recent_activity_4_weeks'] = recent_commits
            else:
                repo_data['recent_activity_4_weeks'] = 0
                
        except Exception as e:
            print(f"Erro ao calcular métricas derivadas: {e}")
    

    def parse_repository_info(self, file_path):
        repo_info = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            
            repo_info = {
                'Nome': json_data.get('repository_name', ''),
                'Proprietário': json_data.get('repository_owner', ''),
                'URL': json_data.get('repository_url', ''),
                'Visibilidade': json_data.get('visibility', ''),
                'Privado': 'Sim' if json_data.get('is_private', False) else 'Não',
                'Data': json_data.get('download_date', ''),
                'Arquivos .feature encontrados': str(json_data.get('total_feature_files', 0)),
                'Arquivos baixados': str(json_data.get('downloaded_files', 0)),
                'Status': json_data.get('status', '')
            }
            
        except Exception as e:
            print(f"Erro ao ler arquivo {file_path}: {e}")
            return None
        
        return repo_info  

    def process_directory(self, base_directory, output_csv='repositories_analysis.csv'):
    
        base_path = Path(base_directory)
        
        if not base_path.exists():
            print(f"Diretório {base_directory} não encontrado!")
            return
        
        all_repos_data = []
        subdirs = [d for d in base_path.iterdir() if d.is_dir()]
        
        print(f"Encontrados {len(subdirs)} subdiretórios para processar...")
        
        for i, subdir in enumerate(subdirs, 1):
            repo_info_file = subdir / "repository_info.json"  
            
            if repo_info_file.exists():
                print(f"\n[{i}/{len(subdirs)}] Processando: {subdir.name}")
                
                repo_info = self.parse_repository_info(repo_info_file)
                
                if repo_info and 'URL' in repo_info:
                    url = repo_info['URL']
                    owner, repo_name = self.extract_owner_repo_from_url(url)
                    
                    if owner and repo_name:
                        repo_data = self.get_repository_data(owner, repo_name)
                        
                        if repo_data:
                            combined_data = {
                                'feature_files_count': repo_info.get('Arquivos .feature encontrados', ''),
                                'downloaded_files_count': repo_info.get('Arquivos baixados', ''),
                                **repo_data
                            }
                            all_repos_data.append(combined_data)
                            print(f"  ✓ Dados coletados para {owner}/{repo_name}")
                        else:
                            print(f"  ✗ Erro ao coletar dados da API para {owner}/{repo_name}")
                    else:
                        print(f"  ✗ URL inválida: {url}")
                else:
                    print(f"  ✗ Arquivo de informações incompleto em {subdir.name}")
            else:
                print(f"  ✗ Arquivo repository_info.json não encontrado em {subdir.name}")  
        
        if all_repos_data:
            self.save_to_csv(all_repos_data, output_csv)
            print(f"\n✅ Análise concluída! {len(all_repos_data)} repositórios processados.")
            print(f"📊 Arquivo salvo: {output_csv}")
            
            self.print_summary_statistics(all_repos_data)
        else:
            print("\n❌ Nenhum dado foi coletado!")

            
    def print_summary_statistics(self, repos_data):

        if not repos_data:
            return
        
        print(f"\n{'='*50}")
        print("📈 ESTATÍSTICAS RESUMIDAS")
        print(f"{'='*50}")
        
        total_repos = len(repos_data)
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos_data)
        total_commits = sum(repo.get('commits_count', 0) for repo in repos_data)
        
        languages = {}
        for repo in repos_data:
            lang = repo.get('main_language', 'Unknown')
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        
        print(f"Total de repositórios analisados: {total_repos}")
        print(f"Total de estrelas: {total_stars}")
        print(f"Total de forks: {total_forks}")
        print(f"Total de commits: {total_commits}")
        print(f"\nLinguagens mais populares:")
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]:
            percentage = (count / total_repos) * 100
            print(f"  {lang}: {count} ({percentage:.1f}%)")
    
    def save_to_csv(self, repos_data, output_file):

        if not repos_data:
            return
        
        fieldnames = [
            'feature_files_count', 
            'downloaded_files_count',
            
            'full_name', 'description', 'html_url',
            'main_language',
            'stargazers_count', 'forks_count', 
            'watchers_count', 'kloc_estimate', 
            'commits_count', 'created_at', 'updated_at', 
            
            'total_commits_last_year', 
            'active_contributors_count', 
            'recent_activity_4_weeks',
    
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for repo in repos_data:
                row = {field: repo.get(field, '') for field in fieldnames}
                writer.writerow(row)

def main():

    load_dotenv()

    BASE_DIRECTORY = os.getenv("RANDON_SELECTOR_OUTPUT") 
    
    OUTPUT_CSV = os.getenv("CHARACTERIZATION_CSV_OUTPUT")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") 
    
    analyzer = GitHubRepositoryAnalyzer(token=GITHUB_TOKEN)
    analyzer.process_directory(BASE_DIRECTORY, OUTPUT_CSV)

if __name__ == "__main__":
    main()