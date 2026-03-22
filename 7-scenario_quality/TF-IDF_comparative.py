
import os
import re
import csv
import math
import argparse
from pathlib import Path
from collections import defaultdict
from typing import List, Tuple, Dict, Set
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from dotenv import load_dotenv


try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class GherkinTextProcessor:
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.gherkin_keywords = {
            'feature', 'scenario', 'given', 'when', 'then', 'and', 'but',
            'background', 'outline', 'examples', 'scenario outline'
        }
        self.stemmer = PorterStemmer()
    
    def preprocess_text(self, text: str) -> List[str]:
        
        text = text.lower()
        
        tokens = re.findall(r'\b[a-zA-Z0-9]+(?:[_-][a-zA-Z0-9]+)*\b', text)
        
        filtered_tokens = []
        for token in tokens:
            if (token not in self.stop_words and 
                token not in self.gherkin_keywords and
                len(token) > 1): 
                filtered_tokens.append(token)
        
        stemmed_tokens = [self.stemmer.stem(token) for token in filtered_tokens]
        
        return stemmed_tokens


class TFIDFCalculator:
    
    def __init__(self, processor: GherkinTextProcessor):
        self.processor = processor
        self.documents = []
        self.vocabulary = set()
        self.idf = {}
        
    def build_vocabulary(self, texts: List[str]):
        
        all_tokens = []
        for text in texts:
            tokens = self.processor.preprocess_text(text)
            all_tokens.extend(tokens)
            self.documents.append(tokens)
        
        self.vocabulary = set(all_tokens)
        self._calculate_idf()
    
    def _calculate_idf(self):
        
        N = len(self.documents)
        
        for term in self.vocabulary:
            
            doc_count = sum(1 for doc in self.documents if term in doc)
          
            self.idf[term] = math.log((N + 1) / (doc_count + 1)) + 1
    
    def tfidf_vector(self, text: str) -> Dict[str, float]:
       
        tokens = self.processor.preprocess_text(text)
        
        tf = defaultdict(int)
        for token in tokens:
            tf[token] += 1
        
        total_terms = len(tokens)
        if total_terms > 0:
            tf = {term: count / total_terms for term, count in tf.items()}
        
        vector = {}
        for term, tf_value in tf.items():
            if term in self.idf:
                vector[term] = tf_value * self.idf[term]
        
        return vector
    
    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
       
        all_terms = set(vec1.keys()) | set(vec2.keys())
        
        if not all_terms:
            return 0.0
        
        dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0) for term in all_terms)
        
        norm1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        norm2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


class GherkinComparator:
    
    def __init__(self, dir1: str, dir2: str, output_csv: str):
        self.dir1 = Path(dir1) 
        self.dir2 = Path(dir2) 
        self.output_csv = output_csv
        
        self.processor = GherkinTextProcessor()
        self.tfidf_calculator = TFIDFCalculator(self.processor)
        
        self.results = []
    
    def extract_scenario_type(self, filename: str) -> str:
       
        name_without_ext = filename.replace('.txt', '')
        
        parts = name_without_ext.split('_scenario_')
        if len(parts) > 1:
            return parts[0]
        else:
           
            return re.sub(r'_\d+$', '', name_without_ext)
    
    def find_scenario_files(self) -> Tuple[Dict[str, Dict[str, List[Path]]], Dict[str, Dict[str, List[Path]]]]:
      
        files_dir1 = defaultdict(lambda: defaultdict(list))
        files_dir2 = defaultdict(lambda: defaultdict(list))
        
        for file_path in self.dir1.rglob("*.txt"):
            rel_path = file_path.relative_to(self.dir1)
            repo_name = rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
            filename = rel_path.name
            
            scenario_type = self.extract_scenario_type(filename)
            files_dir1[repo_name][scenario_type].append((filename, file_path))
        
        for file_path in self.dir2.rglob("*.txt"):
            rel_path = file_path.relative_to(self.dir2)
            repo_name = rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
            filename = rel_path.name
            
            scenario_type = self.extract_scenario_type(filename)
            files_dir2[repo_name][scenario_type].append((filename, file_path))
        
        return files_dir1, files_dir2
    
    def read_all_texts(self, files_dir1: Dict[str, Dict[str, List[Tuple[str, Path]]]], 
                       files_dir2: Dict[str, Dict[str, List[Tuple[str, Path]]]]) -> List[str]:
        
        all_texts = []
        
        for repo in set(list(files_dir1.keys()) + list(files_dir2.keys())):

            if repo in files_dir1:
                for scenario_type in files_dir1[repo]:
                    for filename, file_path in files_dir1[repo][scenario_type]:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                all_texts.append(content)
                        except UnicodeDecodeError:
                            with open(file_path, 'r', encoding='latin-1') as f:
                                content = f.read()
                                all_texts.append(content)
            
            if repo in files_dir2:
                for scenario_type in files_dir2[repo]:
                    for filename, file_path in files_dir2[repo][scenario_type]:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                all_texts.append(content)
                        except UnicodeDecodeError:
                            with open(file_path, 'r', encoding='latin-1') as f:
                                content = f.read()
                                all_texts.append(content)
        
        return all_texts
    
    def compare_scenarios(self) -> None:
        
        print("Organizando arquivos por repositório e tipo de cenário...")
        files_dir1, files_dir2 = self.find_scenario_files()
        
        all_repos = set(list(files_dir1.keys()) + list(files_dir2.keys()))
        
        if not all_repos:
            print("Nenhum arquivo encontrado.")
            return
        
        print(f"Encontrados {len(all_repos)} repositórios.")
        
        
        print("Construindo vocabulário e calculando IDF...")
        all_texts = self.read_all_texts(files_dir1, files_dir2)
        self.tfidf_calculator.build_vocabulary(all_texts)
        
        print("Calculando similaridades...")
        total_comparisons = 0
        
        for repo in all_repos:
            print(f"\nRepositório: {repo}")
            
            scenario_types_dir1 = set(files_dir1[repo].keys()) if repo in files_dir1 else set()
            scenario_types_dir2 = set(files_dir2[repo].keys()) if repo in files_dir2 else set()
            all_scenario_types = scenario_types_dir1 | scenario_types_dir2
            
            for scenario_type in all_scenario_types:
                print(f"  Tipo de cenário: {scenario_type}")
                
                files_type_dir1 = files_dir1[repo].get(scenario_type, [])
                files_type_dir2 = files_dir2[repo].get(scenario_type, [])
                
                if not files_type_dir1 or not files_type_dir2:
                    print(f"    Aviso: Tipo '{scenario_type}' não encontrado em ambos os diretórios")
                    continue
                
                for filename1, file_path1 in files_type_dir1:
  
                    try:
                        with open(file_path1, 'r', encoding='utf-8') as f1:
                            content1 = f1.read()
                    except UnicodeDecodeError:
                        with open(file_path1, 'r', encoding='latin-1') as f1:
                            content1 = f1.read()
                    
                    for filename2, file_path2 in files_type_dir2:
                       
                        try:
                            with open(file_path2, 'r', encoding='utf-8') as f2:
                                content2 = f2.read()
                        except UnicodeDecodeError:
                            with open(file_path2, 'r', encoding='latin-1') as f2:
                                content2 = f2.read()
                        
                        vec1 = self.tfidf_calculator.tfidf_vector(content1)
                        vec2 = self.tfidf_calculator.tfidf_vector(content2)
                        
                        similarity = self.tfidf_calculator.cosine_similarity(vec1, vec2)
                        
                        self.results.append({
                            'repositorio': repo,
                            'tipo_cenario': scenario_type,
                            'arquivo_llm': filename1,
                            'arquivo_original': filename2,
                            'similaridade': round(similarity, 4)
                        })
                        
                        total_comparisons += 1
                        print(f"    {filename1} vs {filename2}: {similarity:.4f}")
        
        self._save_results(total_comparisons)
    
    def _save_results(self, total_comparisons: int) -> None:
       
        os.makedirs(os.path.dirname(self.output_csv), exist_ok=True)
        
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['repositorio', 'tipo_cenario', 'arquivo_llm', 'arquivo_original', 'similaridade']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results:
                writer.writerow(result)
        
        print(f"\nResultados salvos em: {self.output_csv}")
        print(f"Total de comparações: {total_comparisons}")


def main():
   
    load_dotenv()
    
    LLM_GENERATED_DIR = os.getenv('SCENARIOS_SPLITED_DIR')
    ORIGINAL_DIR = os.getenv('DIRETORIO_DESTINO_CENARIOS')
    SCENARIO_QUALITY_CSV = os.getenv('SCENARIO_QUALITY_CSV')
    
    if not os.path.exists(LLM_GENERATED_DIR):
        print(f"Erro: Diretório não encontrado: {LLM_GENERATED_DIR}")
        return
    
    if not os.path.exists(ORIGINAL_DIR):
        print(f"Erro: Diretório não encontrado: {ORIGINAL_DIR}")
        return
    
    print("=== Comparador de Cenários Gherkin (MODIFICADO) ===")
    print("Compara todos os cenários do mesmo tipo entre diretórios")
    print(f"Diretório LLM: {LLM_GENERATED_DIR}")
    print(f"Diretório Original: {ORIGINAL_DIR}")
    print(f"Saída CSV: {SCENARIO_QUALITY_CSV}")
    print("-" * 50)

    comparator = GherkinComparator(LLM_GENERATED_DIR, ORIGINAL_DIR, SCENARIO_QUALITY_CSV)
    comparator.compare_scenarios()


if __name__ == "__main__":
    main()