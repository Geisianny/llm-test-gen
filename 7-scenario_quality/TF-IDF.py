"""
Script para comparação de similaridade textual entre cenários Gherkin.
Baseado na técnica descrita no artigo: TF-IDF + Similaridade de Cosseno.
"""

import os
import re
import csv
import math
import argparse
from pathlib import Path
from collections import defaultdict
from typing import List, Tuple, Dict
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from dotenv import load_dotenv

# Baixar recursos do NLTK se necessário
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class GherkinTextProcessor:
    """Processador de texto especializado para cenários Gherkin"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.gherkin_keywords = {
            'feature', 'scenario', 'given', 'when', 'then', 'and', 'but',
            'background', 'outline', 'examples', 'scenario outline'
        }
        self.stemmer = PorterStemmer()
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Pré-processa o texto conforme especificado no artigo:
        1. Tokenização (espaços e pontuação)
        2. Conversão para minúsculas
        3. Remoção de stopwords em inglês
        4. Remoção de keywords do Gherkin
        5. Stemming (radicalização)
        """
        # Converter para minúsculas
        text = text.lower()
        
        # Tokenização usando regex (espaços e pontuação e numeros)
        tokens = re.findall(r'\b[a-zA-Z0-9]+(?:[_-][a-zA-Z0-9]+)*\b', text)
        
        # Remover stopwords e keywords do Gherkin
        filtered_tokens = []
        for token in tokens:
            if (token not in self.stop_words and 
                token not in self.gherkin_keywords and
                len(token) > 1):  # Remover caracteres únicos
                filtered_tokens.append(token)
        
        # Aplicar stemming
        stemmed_tokens = [self.stemmer.stem(token) for token in filtered_tokens]
        
        return stemmed_tokens


class TFIDFCalculator:
    """Calcula TF-IDF e similaridade de cosseno"""
    
    def __init__(self, processor: GherkinTextProcessor):
        self.processor = processor
        self.documents = []
        self.vocabulary = set()
        self.idf = {}
        
    def build_vocabulary(self, texts: List[str]):
        """Constrói o vocabulário a partir de todos os textos"""
        all_tokens = []
        for text in texts:
            tokens = self.processor.preprocess_text(text)
            all_tokens.extend(tokens)
            self.documents.append(tokens)
        
        self.vocabulary = set(all_tokens)
        self._calculate_idf()
    
    def _calculate_idf(self):
        """Calcula o IDF para cada termo no vocabulário"""
        N = len(self.documents)
        
        for term in self.vocabulary:
            # Contar em quantos documentos o termo aparece
            doc_count = sum(1 for doc in self.documents if term in doc)
            # IDF suavizado (evitar divisão por zero)
            self.idf[term] = math.log((N + 1) / (doc_count + 1)) + 1
    
    def tfidf_vector(self, text: str) -> Dict[str, float]:
        """Converte um texto em vetor TF-IDF"""
        tokens = self.processor.preprocess_text(text)
        
        # Calcular TF (frequência do termo no documento)
        tf = defaultdict(int)
        for token in tokens:
            tf[token] += 1
        
        # Normalizar TF
        total_terms = len(tokens)
        if total_terms > 0:
            tf = {term: count / total_terms for term, count in tf.items()}
        
        # Calcular TF-IDF
        vector = {}
        for term, tf_value in tf.items():
            if term in self.idf:
                vector[term] = tf_value * self.idf[term]
        
        return vector
    
    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calcula a similaridade de cosseno entre dois vetores"""
        # Obter todos os termos únicos de ambos os vetores
        all_terms = set(vec1.keys()) | set(vec2.keys())
        
        if not all_terms:
            return 0.0
        
        # Calcular produto escalar
        dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0) for term in all_terms)
        
        # Calcular normas
        norm1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        norm2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
        
        # Evitar divisão por zero
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


class GherkinComparator:
    """Comparador de cenários Gherkin entre dois diretórios"""
    
    def __init__(self, dir1: str, dir2: str, output_csv: str):
        self.dir1 = Path(dir1)
        self.dir2 = Path(dir2)
        self.output_csv = output_csv
        
        self.processor = GherkinTextProcessor()
        self.tfidf_calculator = TFIDFCalculator(self.processor)
        
        # Resultados
        self.results = []
    
    def find_matching_files(self) -> List[Tuple[Path, Path, str, str]]:
        """Encontra pares de arquivos correspondentes nos dois diretórios"""
        matches = []
        
        # Percorrer diretório1
        for file1 in self.dir1.rglob("*.txt"):
            # Obter caminho relativo
            rel_path = file1.relative_to(self.dir1)
            file2 = self.dir2 / rel_path
            
            if file2.exists():
                # Extrair nome do repositório (primeira parte do caminho relativo)
                repo_name = rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
                matches.append((file1, file2, repo_name, rel_path.name))
            else:
                print(f"Aviso: Arquivo correspondente não encontrado: {rel_path}")
        
        return matches
    
    def read_all_texts(self, matches: List[Tuple[Path, Path, str, str]]) -> List[str]:
        """Lê todos os textos para construir o vocabulário"""
        all_texts = []
        
        for file1, file2, _, _ in matches:
            # Ler conteúdo dos dois arquivos
            for file_path in [file1, file2]:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        all_texts.append(content)
                except UnicodeDecodeError:
                    # Tentar outra codificação se UTF-8 falhar
                    with open(file_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                        all_texts.append(content)
        
        return all_texts
    
    # def compare_scenarios(self) -> None:
    #     """Compara todos os cenários e salva resultados"""
    #     print("Buscando arquivos correspondentes...")
    #     matches = self.find_matching_files()
        
    #     if not matches:
    #         print("Nenhum arquivo correspondente encontrado.")
    #         return
        
    #     print(f"Encontrados {len(matches)} pares de arquivos para comparação.")
        
    #     # Ler todos os textos para construir vocabulário
    #     print("Construindo vocabulário e calculando IDF...")
    #     all_texts = self.read_all_texts(matches)
    #     self.tfidf_calculator.build_vocabulary(all_texts)
        
    #     print("Calculando similaridades...")
    #     for file1, file2, repo_name, filename in matches:
    #         try:
    #             # Ler conteúdos
    #             with open(file1, 'r', encoding='utf-8') as f1:
    #                 content1 = f1.read()
    #             with open(file2, 'r', encoding='utf-8') as f2:
    #                 content2 = f2.read()
                
    #             # Calcular vetores TF-IDF
    #             vec1 = self.tfidf_calculator.tfidf_vector(content1)
    #             vec2 = self.tfidf_calculator.tfidf_vector(content2)
                
    #             # Calcular similaridade
    #             similarity = self.tfidf_calculator.cosine_similarity(vec1, vec2)
                
    #             # Adicionar resultado
    #             self.results.append({
    #                 'repositorio': repo_name,
    #                 'arquivo': filename,
    #                 'similaridade': round(similarity, 4)
    #             })
                
    #             print(f"  {repo_name}/{filename}: {similarity:.4f}")
                
    #         except Exception as e:
    #             print(f"Erro ao processar {repo_name}/{filename}: {e}")
        
    #     # Salvar resultados em CSV
    #     self._save_results()
    

    def compare_scenarios(self) -> None:
        """Compara todos os cenários e salva resultados"""
        print("Buscando arquivos correspondentes...")
        matches = self.find_matching_files()
        
        if not matches:
            print("Nenhum arquivo correspondente encontrado.")
            return
        
        print(f"Encontrados {len(matches)} pares de arquivos para comparação.")
        
        # Ler todos os textos para construir vocabulário
        print("Construindo vocabulário e calculando IDF...")
        all_texts = self.read_all_texts(matches)
        self.tfidf_calculator.build_vocabulary(all_texts)
        
        print("Calculando similaridades...")
        for file1, file2, repo_name, filename in matches:
            try:
                # Ler conteúdos
                with open(file1, 'r', encoding='utf-8') as f1:
                    content1 = f1.read()
                with open(file2, 'r', encoding='utf-8') as f2:
                    content2 = f2.read()
                
                # Contar cenários no arquivo ORIGINAL_DIR (file2)
                scenario_count = count_scenarios_in_file(file2)
                
                # Calcular vetores TF-IDF
                vec1 = self.tfidf_calculator.tfidf_vector(content1)
                vec2 = self.tfidf_calculator.tfidf_vector(content2)
                
                # Calcular similaridade
                similarity = self.tfidf_calculator.cosine_similarity(vec1, vec2)
                
                # Adicionar resultado
                self.results.append({
                    'repositorio': repo_name,
                    'arquivo': filename,
                    'similaridade': round(similarity, 4),
                    'qtd_cenarios': scenario_count  # Nova coluna
                })
                
                print(f"  {repo_name}/{filename}: {similarity:.4f}, Cenários: {scenario_count}")
                
            except Exception as e:
                print(f"Erro ao processar {repo_name}/{filename}: {e}")
        
        # Salvar resultados em CSV
        self._save_results()

    # def _save_results(self) -> None:
        # """Salva os resultados em arquivo CSV"""
        # os.makedirs(os.path.dirname(self.output_csv), exist_ok=True)
        
        # with open(self.output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        #     fieldnames = ['repositorio', 'arquivo', 'similaridade']
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
        #     writer.writeheader()
        #     for result in self.results:
        #         writer.writerow(result)
        
        # print(f"\nResultados salvos em: {self.output_csv}")
        # print(f"Total de comparações: {len(self.results)}")

    def _save_results(self) -> None:
        """Salva os resultados em arquivo CSV"""
        os.makedirs(os.path.dirname(self.output_csv), exist_ok=True)
        
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            # ATUALIZE AQUI: Adicione 'qtd_cenarios' aos fieldnames
            fieldnames = ['repositorio', 'arquivo', 'similaridade', 'qtd_cenarios']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results:
                writer.writerow(result)
        
        print(f"\nResultados salvos em: {self.output_csv}")
        print(f"Total de comparações: {len(self.results)}")


def count_scenarios_in_file(file_path: Path) -> int:
    """Conta o número de cenários em um arquivo Gherkin"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Usa regex para encontrar cenários (case insensitive)
    # Considera "Scenario", "Scenario Outline", "Example", etc.
    scenario_pattern = re.compile(r'^\s*Scenario', re.IGNORECASE | re.MULTILINE)
    matches = scenario_pattern.findall(content)
    
    return len(matches)

def main():
    """Função principal"""
    # Carregar variáveis de ambiente do arquivo .env
    load_dotenv()
    
    # Configuração via variáveis de ambiente (com valores padrão)
    LLM_GENERATED_DIR = os.getenv('LLM_US_TO_TEST_OUTPUT_DIR')
    ORIGINAL_DIR = os.getenv('DIRETORIO_DESTINO_CONSOLIDADOS')
    SCENARIO_QUALITY_CSV = os.getenv('SCENARIO_QUALITY_CSV')
    
    # Verificar se diretórios existem
    if not os.path.exists(LLM_GENERATED_DIR):
        print(f"Erro: Diretório não encontrado: {LLM_GENERATED_DIR}")
        return
    
    if not os.path.exists(ORIGINAL_DIR):
        print(f"Erro: Diretório não encontrado: {ORIGINAL_DIR}")
        return
    
    print("=== Comparador de Cenários Gherkin ===")
    print(f"Diretório 1: {LLM_GENERATED_DIR}")
    print(f"Diretório 2: {ORIGINAL_DIR}")
    print(f"Saída CSV: {SCENARIO_QUALITY_CSV}")
    print("-" * 40)
    
    # Criar comparador e executar
    comparator = GherkinComparator(LLM_GENERATED_DIR, ORIGINAL_DIR, SCENARIO_QUALITY_CSV)
    comparator.compare_scenarios()


if __name__ == "__main__":
    main()