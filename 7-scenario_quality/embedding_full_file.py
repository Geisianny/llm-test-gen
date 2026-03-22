
import os
import re
import csv
import argparse
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict, Any
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from scipy.spatial.distance import cosine
from datetime import datetime

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Usando dispositivo: {device}")

class GherkinEmbeddingProcessor:
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    
        print(f"Carregando modelo: {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(device)
        self.model.eval()
        
        self.gherkin_keywords = {
            'feature', 'scenario', 'given', 'when', 'then', 'and', 'but',
            'background', 'outline', 'examples', 'scenario outline',
            'dado', 'quando', 'então', 'e', 'mas' 
        }
    
    def preprocess_gherkin(self, text: str, remove_keywords: bool = True) -> str:
       
        if remove_keywords:
           
            pattern = r'\b(' + '|'.join(self.gherkin_keywords) + r')\b'
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def get_embedding(self, text: str, pooling_strategy: str = "mean") -> np.ndarray:
       
        processed_text = self.preprocess_gherkin(text)
        
        inputs = self.tokenizer(
            processed_text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            
            if pooling_strategy == "mean":
                
                attention_mask = inputs['attention_mask']
                token_embeddings = outputs.last_hidden_state
                input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
                sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
                sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
                embedding = sum_embeddings / sum_mask
                
            elif pooling_strategy == "cls":
           
                embedding = outputs.last_hidden_state[:, 0, :]
                
            elif pooling_strategy == "max":
                attention_mask = inputs['attention_mask']
                token_embeddings = outputs.last_hidden_state
                input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
                token_embeddings[input_mask_expanded == 0] = -1e9  
                embedding = torch.max(token_embeddings, 1)[0]
        
       
        embedding = embedding.cpu().numpy()[0]
        embedding = embedding / np.linalg.norm(embedding)   
        
        return embedding
    
    def cosine_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        similarity = np.dot(embedding1, embedding2)
        return float(similarity)


class AdvancedGherkinComparator:
    
    def __init__(self, dir1: str, dir2: str, output_csv: str, 
                 model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.dir1 = Path(dir1)
        self.dir2 = Path(dir2)
        self.output_csv = output_csv
        self.model_name = model_name
        
        self.processor = GherkinEmbeddingProcessor(model_name)
        
        self.results = []
    
    def find_matching_files(self) -> List[Tuple[Path, Path, str, str]]:
        
        matches = []
        
        for file1 in self.dir1.rglob("*.txt"):
            rel_path = file1.relative_to(self.dir1)
            file2 = self.dir2 / rel_path
            
            if file2.exists():
                repo_name = rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
                matches.append((file1, file2, repo_name, rel_path.name))
            else:
            
                filename = file1.name
                matching_files = list(self.dir2.rglob(f"**/{filename}"))
                if matching_files:
                    file2 = matching_files[0]
                    repo_name = file1.parent.name
                    matches.append((file1, file2, repo_name, filename))
                else:
                    print(f"Aviso: Arquivo correspondente não encontrado para: {rel_path}")
        
        return matches
    
    def read_file_content(self, file_path: Path) -> str:
        """Lê o conteúdo completo de um arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def compare_files_semantic(self, file1: Path, file2: Path) -> Dict[str, Any]:
   
        content1 = self.read_file_content(file1)
        content2 = self.read_file_content(file2)
        
        embedding1 = self.processor.get_embedding(content1)
        embedding2 = self.processor.get_embedding(content2)
        
        similarity = self.processor.cosine_similarity(embedding1, embedding2)
        
        lines1 = content1.count('\n') + 1
        lines2 = content2.count('\n') + 1
        words1 = len(content1.split())
        words2 = len(content2.split())
        chars1 = len(content1)
        chars2 = len(content2)
        
        return {
            'similarity_semantic': similarity,
            'lines_file1': lines1,
            'lines_file2': lines2,
            'words_file1': words1,
            'words_file2': words2,
            'chars_file1': chars1,
            'chars_file2': chars2
        }
    
    def compare_scenarios(self) -> None:
        
        print("Buscando arquivos correspondentes...")
        matches = self.find_matching_files()
        
        if not matches:
            print("Nenhum arquivo correspondente encontrado.")
            return
        
        print(f"Encontrados {len(matches)} pares de arquivos para comparação.")
        print("Usando embeddings para análise semântica...")
        
        for idx, (file1, file2, repo_name, filename) in enumerate(matches, 1):
            print(f"\n[{idx}/{len(matches)}] Processando: {repo_name}/{filename}")
            
            try:
                metrics = self.compare_files_semantic(file1, file2)
                
                self.results.append({
                    'repositorio': repo_name,
                    'arquivo': filename,
                    'similaridade_semantica': round(metrics['similarity_semantic'], 4),
                    'qtd_linhas_arquivo1': metrics['lines_file1'],
                    'qtd_linhas_arquivo2': metrics['lines_file2'],
                    'qtd_palavras_arquivo1': metrics['words_file1'],
                    'qtd_palavras_arquivo2': metrics['words_file2'],
                    'qtd_caracteres_arquivo1': metrics['chars_file1'],
                    'qtd_caracteres_arquivo2': metrics['chars_file2']
                })
                
                print(f"  Similaridade semântica: {metrics['similarity_semantic']:.4f}")
                print(f"  Linhas: {metrics['lines_file1']} vs {metrics['lines_file2']}")
                print(f"  Palavras: {metrics['words_file1']} vs {metrics['words_file2']}")
                
            except Exception as e:
                print(f"Erro ao processar {repo_name}/{filename}: {e}")

                self.results.append({
                    'repositorio': repo_name,
                    'arquivo': filename,
                    'similaridade_semantica': 0.0,
                    'qtd_linhas_arquivo1': 0,
                    'qtd_linhas_arquivo2': 0,
                    'qtd_palavras_arquivo1': 0,
                    'qtd_palavras_arquivo2': 0,
                    'qtd_caracteres_arquivo1': 0,
                    'qtd_caracteres_arquivo2': 0,
                    'erro': str(e)
                })
        
        self._save_results()

        self._save_summary_statistics()
        
        self._print_summary_statistics()
    
    def _save_results(self) -> None:

        os.makedirs(os.path.dirname(self.output_csv), exist_ok=True)
        
        if self.results:
            fieldnames = list(self.results[0].keys())
        else:
            fieldnames = ['repositorio', 'arquivo', 'similaridade_semantica',
                         'qtd_linhas_arquivo1', 'qtd_linhas_arquivo2',
                         'qtd_palavras_arquivo1', 'qtd_palavras_arquivo2',
                         'qtd_caracteres_arquivo1', 'qtd_caracteres_arquivo2']
        
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in self.results:
                writer.writerow(result)
        
        print(f"\nResultados salvos em: {self.output_csv}")
        print(f"Total de comparações: {len(self.results)}")
    
    def _print_summary_statistics(self) -> str:
       
        if not self.results:
            return "Nenhum resultado para analisar."
        
        valid_results = [r for r in self.results if 'erro' not in r]
        
        if not valid_results:
            return "Nenhum resultado válido para estatísticas."
        
        output = []
        output.append("=" * 60)
        output.append("ESTATÍSTICAS RESUMIDAS DA COMPARAÇÃO")
        output.append("=" * 60)
        
        similarities = [r['similaridade_semantica'] for r in valid_results]
        output.append(f"Similaridade Semântica (conteúdo completo):")
        output.append(f"  Média: {np.mean(similarities):.4f}")
        output.append(f"  Mediana: {np.median(similarities):.4f}")
        output.append(f"  Mínima: {np.min(similarities):.4f}")
        output.append(f"  Máxima: {np.max(similarities):.4f}")
        output.append(f"  Desvio Padrão: {np.std(similarities):.4f}")
        
        high_similarity = sum(1 for r in valid_results if r['similaridade_semantica'] > 0.7)
        medium_similarity = sum(1 for r in valid_results if 0.4 <= r['similaridade_semantica'] <= 0.7)
        low_similarity = sum(1 for r in valid_results if r['similaridade_semantica'] < 0.4)
        
        output.append(f"\nDistribuição de Similaridade:")
        output.append(f"  Alta (>0.7): {high_similarity} arquivos ({high_similarity/len(valid_results):.1%})")
        output.append(f"  Média (0.4-0.7): {medium_similarity} arquivos ({medium_similarity/len(valid_results):.1%})")
        output.append(f"  Baixa (<0.4): {low_similarity} arquivos ({low_similarity/len(valid_results):.1%})")
        
        total_lines1 = sum(r['qtd_linhas_arquivo1'] for r in valid_results)
        total_lines2 = sum(r['qtd_linhas_arquivo2'] for r in valid_results)
        total_words1 = sum(r['qtd_palavras_arquivo1'] for r in valid_results)
        total_words2 = sum(r['qtd_palavras_arquivo2'] for r in valid_results)
        total_chars1 = sum(r['qtd_caracteres_arquivo1'] for r in valid_results)
        total_chars2 = sum(r['qtd_caracteres_arquivo2'] for r in valid_results)
        
        output.append(f"\nTotal de Linhas:")
        output.append(f"  Arquivos 1 (LLM): {total_lines1}")
        output.append(f"  Arquivos 2 (Humanos): {total_lines2}")
        output.append(f"  Diferença: {abs(total_lines1 - total_lines2)}")
        
        output.append(f"\nTotal de Palavras:")
        output.append(f"  Arquivos 1 (LLM): {total_words1}")
        output.append(f"  Arquivos 2 (Humanos): {total_words2}")
        output.append(f"  Diferença: {abs(total_words1 - total_words2)}")
        
        output.append(f"\nTotal de Caracteres:")
        output.append(f"  Arquivos 1 (LLM): {total_chars1}")
        output.append(f"  Arquivos 2 (Humanos): {total_chars2}")
        output.append(f"  Diferença: {abs(total_chars1 - total_chars2)}")
        
        output.append(f"\nInformações da Execução:")
        output.append(f"  Modelo usado: {self.model_name}")
        output.append(f"  Dispositivo: {device}")
        output.append(f"  Total de arquivos comparados: {len(valid_results)}")
        output.append(f"  Data da análise: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        output.append("=" * 60)
        
        return "\n".join(output)

    def _generate_summary_statistics(self) -> str:

        return self._print_summary_statistics()

    def _save_summary_statistics(self) -> None:
       
        if not self.results:
            return
        
        csv_path = Path(self.output_csv)
        stats_path = csv_path.with_suffix('.txt')
        
        stats_content = self._generate_summary_statistics()
        
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write(stats_content)
        
        print(f"Estatísticas salvas em: {stats_path}")

def main():
    
    load_dotenv()
    
    LLM_GENERATED_DIR = os.getenv('LLM_US_TO_TEST_OUTPUT_DIR')
    ORIGINAL_DIR = os.getenv('DIRETORIO_DESTINO_CONSOLIDADOS')
    SCENARIO_QUALITY_CSV = os.getenv('SCENARIO_QUALITY_CSV_EMBEDDING')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', "sentence-transformers/all-MiniLM-L6-v2")
    
    if not os.path.exists(LLM_GENERATED_DIR):
        print(f"Erro: Diretório não encontrado: {LLM_GENERATED_DIR}")
        return
    
    if not os.path.exists(ORIGINAL_DIR):
        print(f"Erro: Diretório não encontrado: {ORIGINAL_DIR}")
        return
    
    print("=== Comparador Semântico de Conteúdo Gherkin ===")
    print(f"Modelo: {EMBEDDING_MODEL}")
    print(f"Dispositivo: {device}")
    print(f"Diretório 1 (LLM): {LLM_GENERATED_DIR}")
    print(f"Diretório 2 (Humanos): {ORIGINAL_DIR}")
    print(f"Saída CSV: {SCENARIO_QUALITY_CSV}")
    print("-" * 40)
    
    comparator = AdvancedGherkinComparator(
        LLM_GENERATED_DIR, 
        ORIGINAL_DIR, 
        SCENARIO_QUALITY_CSV,
        model_name=EMBEDDING_MODEL
    )
    
    comparator.compare_scenarios()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Comparador semântico de conteúdo Gherkin")
    parser.add_argument("--model", type=str, default=None, 
                       help="Nome do modelo de embeddings da Hugging Face")
    args = parser.parse_args()
    
    if args.model:
        os.environ['EMBEDDING_MODEL'] = args.model
    
    main()