import requests
import pandas as pd
import time
from datetime import datetime
import json
import base64
import re
from dotenv import load_dotenv
import os

class GitHubFeatureSearcher:
    def __init__(self, token):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {token}"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def check_auth(self):
        
        url = f"{self.base_url}/user"
        try:
            response = self.session.get(url)
            return response.status_code == 200
        except:
            return False

    def search_repositories_advanced(self, domain_query, max_results=30):
        
        repositories = []
        page = 1

        search_query = f'extension:feature {domain_query}'
        print(f"Buscando: {search_query}")

        while len(repositories) < max_results:
            url = f"{self.base_url}/search/code"
            params = {
                'q': search_query,
                'per_page': 30,
                'page': page
            }

            try:
                response = self.session.get(url, params=params)

                if response.status_code == 403:
                    self.handle_rate_limit(response)
                    continue
                elif response.status_code == 422:
                    print("Query muito complexa, simplificando...")
                    break

                response.raise_for_status()

                data = response.json()

                if not data.get('items'):
                    print("Nenhum item encontrado nesta página")
                    break

                print(f"Página {page}: {len(data['items'])} arquivos encontrados")

                for item in data['items']:
                    repo = item['repository']
                    repo_full_name = repo['full_name']

                    if any(r['name'] == repo_full_name for r in repositories):
                        continue

                    repo_details = self.get_repository_details(repo_full_name)
                    if not repo_details:
                        continue

                    if self.is_relevant_repository(repo_details):
                        repo_info = self.create_repo_info(repo, item, repo_details)
                        repositories.append(repo_info)
                        print(f"Adicionado: {repo_full_name} ({repo_details['stargazers_count']} )")

                if len(repositories) >= max_results or page >= 5:
                    break

                page += 1
                time.sleep(2)

            except Exception as e:
                print(f"Erro na busca: {e}")
                break

        return repositories[:max_results]

    def is_relevant_repository(self, repo_details, min_stars=5, exclude_archived=True):
        
        if exclude_archived and repo_details.get('archived', False):
            return False

        if repo_details.get('stargazers_count', 0) < min_stars:
            return False

        exclude_keywords = ['tutorial', 'example', 'demo', 'boilerplate', 'sample',
                          'test-project', 'learning', 'workshop', 'course', 'template']

        name = repo_details['full_name'].lower()
        description = (repo_details.get('description') or '').lower()

        if any(keyword in name for keyword in exclude_keywords) or \
           any(keyword in description for keyword in exclude_keywords):
            return False

        return True

    def get_repository_details(self, repo_full_name):
      
        url = f"{self.base_url}/repos/{repo_full_name}"
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"Repositório não encontrado: {repo_full_name}")
            elif response.status_code == 403:
                self.handle_rate_limit(response)
        except Exception as e:
            print(f"Erro ao obter detalhes de {repo_full_name}: {e}")
        return None

    def create_repo_info(self, repo, item, repo_details):
        
        return {
            'name': repo['full_name'],
            'url': repo['html_url'],
            'description': repo.get('description', ''),
            'stars': repo_details.get('stargazers_count', 0),
            'forks': repo_details.get('forks_count', 0),
            'watchers': repo_details.get('watchers_count', 0),
            'language': repo_details.get('language', ''),
            'created_at': repo_details.get('created_at', ''),
            'updated_at': repo_details.get('updated_at', ''),
            'pushed_at': repo_details.get('pushed_at', ''),
            'archived': repo_details.get('archived', False),
            'topics': repo_details.get('topics', []),
            'feature_file_url': item['html_url'],
            'feature_file_path': item['path'],
            'score': item.get('score', 0),
            'size': repo_details.get('size', 0),
            'open_issues': repo_details.get('open_issues_count', 0)
        }

    def search_by_repository_topics(self, topic, max_results=20):
        
        repos_by_topic = []
        page = 1

        while len(repos_by_topic) < max_results:
            url = f"{self.base_url}/search/repositories"
            params = {
                'q': f'topic:{topic} stars:>5',
                'per_page': 30,
                'page': page,
                'sort': 'stars',
                'order': 'desc'
            }

            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()

                data = response.json()
                if not data.get('items'):
                    break

                for repo in data['items']:
                    if self.has_feature_files(repo['full_name']):
                        repos_by_topic.append(repo)
                        print(f"{repo['full_name']} tem arquivos .feature")

                    if len(repos_by_topic) >= max_results:
                        break

                page += 1
                time.sleep(1)

            except Exception as e:
                print(f"Erro na busca por tópicos: {e}")
                break

        return repos_by_topic[:max_results]

    def has_feature_files(self, repo_full_name):

        url = f"{self.base_url}/search/code"
        params = {
            'q': f'extension:feature repo:{repo_full_name}'
        }

        try:
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('total_count', 0) > 0
        except:
            pass
        return False

    def handle_rate_limit(self, response):
        
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        wait_time = max(reset_time - time.time(), 0) + 10

        print(f"Rate limit excedido. Aguardando {wait_time:.0f} segundos...")

        time.sleep(wait_time)

def main():
    load_dotenv()

    # INSIRA SEU TOKEN
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    OUTPUT_PATH = os.getenv("GITHUBSEARCH_OUTPUT")

    DOMAINS = os.getenv("DOMAINS").split(',')

    TOPICS = os.getenv("TOPICS").split(',')

    if GITHUB_TOKEN == "":
        print("Por favor, GITHUB_TOKEN no arquivo .env")
        return

    searcher = GitHubFeatureSearcher(token=GITHUB_TOKEN)

    if not searcher.check_auth():
        print("Falha na autenticação")
        return

   
    print("=== ESTRATÉGIA 1: Busca direta por domínios ===")
    domains = DOMAINS

    all_repositories = []

    for domain in domains:
        print(f"\n--- Buscando: {domain} ---")
        repos = searcher.search_repositories_advanced(
            domain_query=domain,
            max_results=15
        )
        all_repositories.extend(repos)
        print(f"Encontrados {len(repos)} repositórios para '{domain}'")
        time.sleep(3)


    print("\n===ESTRATÉGIA 2: Busca por tópicos ===")
    topics = TOPICS

    for topic in topics:
        print(f"\n--- Buscando tópico: {topic} ---")
        repos = searcher.search_by_repository_topics(
            topic=topic,
            max_results=10
        )

        for repo in repos:
            repo_info = {
                'name': repo['full_name'],
                'url': repo['html_url'],
                'description': repo.get('description', ''),
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'language': repo.get('language', ''),
                'topics': repo.get('topics', [])
            }
            all_repositories.append(repo_info)
        print(f"Encontrados {len(repos)} repositórios com tópico '{topic}'")
        time.sleep(2)

    if all_repositories:
        df = pd.DataFrame(all_repositories)

        df = df.drop_duplicates(subset=['name'])

        df = df.sort_values('stars', ascending=False)

        print(f"\nTOTAL: {len(df)} repositórios únicos encontrados!")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{OUTPUT_PATH}/github_feature_repos_{timestamp}.csv"
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Resultados salvos em: {filename}")

        print(f"\nTOP 10 REPOSITÓRIOS:")
        for i, (_, repo) in enumerate(df.head(10).iterrows()):
            print(f"{i+1}. {repo['name']} - {repo['stars']} - {repo['language']}")
            print(f"   {repo['description']}")
            print(f"   {repo['url']}\n")

    else:
        print("Nenhum repositório encontrado. Verifique:")
        print("1. Se o token está correto")
        print("2. Se a conexão está funcionando")
        print("3. Tente termos de busca mais amplos")

if __name__ == "__main__":
    main()