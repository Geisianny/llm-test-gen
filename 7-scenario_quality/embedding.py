
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
            'dado', 'quando', 'então', 'e', 'mas'  # Versões em português
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
    
    def batch_get_embeddings(self, texts: List[str], batch_size: int = 8) -> List[np.ndarray]:
        
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_processed = [self.preprocess_gherkin(text) for text in batch_texts]
            
            inputs = self.tokenizer(
                batch_processed,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            ).to(device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                attention_mask = inputs['attention_mask']
                token_embeddings = outputs.last_hidden_state
                
                input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
                sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
                sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
                batch_embeddings = sum_embeddings / sum_mask
            
            for emb in batch_embeddings.cpu().numpy():
                emb_norm = emb / np.linalg.norm(emb)
                embeddings.append(emb_norm)
            
            print(f"  Processados {min(i+batch_size, len(texts))}/{len(texts)} textos")
        
        return embeddings
    
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
                # Tentar encontrar por nome de arquivo se não encontrar pelo caminho
                filename = file1.name
                matching_files = list(self.dir2.rglob(f"**/{filename}"))
                if matching_files:
                    file2 = matching_files[0]
                    repo_name = file1.parent.name
                    matches.append((file1, file2, repo_name, filename))
                else:
                    print(f"Aviso: Arquivo correspondente não encontrado para: {rel_path}")
        
        return matches
    
    def extract_scenarios_from_file(self, file_path: Path) -> List[str]:
        """
        Extrai cenários individuais de um arquivo Gherkin.
        
        Returns:
            Lista de strings, cada uma representando um cenário
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Padrão para encontrar cenários (suporta inglês e português)
        scenario_pattern = re.compile(
            r'^\s*(?:Scenario|Cenário)(?:\s+Outline| Outline)?:(.*?)(?=^\s*(?:Scenario|Cenário|Feature|Funcionalidade|$))',
            re.IGNORECASE | re.MULTILINE | re.DOTALL
        )
        
        scenarios = []
        for match in scenario_pattern.finditer(content):
            scenario_text = match.group(1).strip()
            if scenario_text:  # Ignorar cenários vazios
                scenarios.append(scenario_text)
        
        return scenarios
    
    def compare_files_semantic(self, file1: Path, file2: Path) -> Dict[str, Any]:
        """
        Compara dois arquivos usando similaridade semântica.
        
        Returns:
            Dicionário com métricas de comparação
        """
        # Extrair cenários
        scenarios1 = self.extract_scenarios_from_file(file1)
        scenarios2 = self.extract_scenarios_from_file(file2)

        # print("scenarios1: ")
        # print(scenarios1)

        # print("scenarios2: ")
        # print(scenarios2)

        # garantir que sempre caia nessa condição para comparar os arquivos por inteiros

        if not scenarios1 or not scenarios2:
            # Se algum arquivo não tem cenários, usar conteúdo completo
            with open(file1, 'r', encoding='utf-8') as f:
                content1 = f.read()
            with open(file2, 'r', encoding='utf-8') as f:
                content2 = f.read()
                
            # Gerar embeddings para conteúdo completo
            embedding1 = self.processor.get_embedding(content1)
            embedding2 = self.processor.get_embedding(content2)
            similarity = self.processor.cosine_similarity(embedding1, embedding2)
            
            return {
                'similarity_overall': similarity,
                'similarity_scenario_based': similarity,
                'num_scenarios_file1': len(scenarios1),
                'num_scenarios_file2': len(scenarios2),
                'best_matches': [],
                'coverage_score': 0.0 if not scenarios1 or not scenarios2 else similarity
            }
        
        # Gerar embeddings para todos os cenários
        print(f"  Gerando embeddings para {len(scenarios1)} + {len(scenarios2)} cenários...")
        all_scenarios = scenarios1 + scenarios2
        all_embeddings = self.processor.batch_get_embeddings(all_scenarios)
        
        embeddings1 = all_embeddings[:len(scenarios1)]
        embeddings2 = all_embeddings[len(scenarios1):]
        
        # Calcular matriz de similaridade
        similarity_matrix = np.zeros((len(scenarios1), len(scenarios2)))
        for i, emb1 in enumerate(embeddings1):
            for j, emb2 in enumerate(embeddings2):
                similarity_matrix[i][j] = np.dot(emb1, emb2)
        
        # Estratégia 1: Melhor correspondência para cada cenário do arquivo 1
        best_matches = []
        if len(scenarios2) > 0:
            for i in range(len(scenarios1)):
                best_similarity = np.max(similarity_matrix[i]) if len(scenarios2) > 0 else 0
                best_match_idx = np.argmax(similarity_matrix[i]) if len(scenarios2) > 0 else -1
                best_matches.append({
                    'scenario_idx': i,
                    'best_match_idx': best_match_idx,
                    'similarity': float(best_similarity)
                })
        
        # Métricas de similaridade
        if best_matches:
            similarity_scenario_based = np.mean([match['similarity'] for match in best_matches])
        else:
            similarity_scenario_based = 0.0
        
        # Estratégia 2: Similaridade entre embeddings médios dos arquivos
        if embeddings1 and embeddings2:
            avg_embedding1 = np.mean(embeddings1, axis=0)
            avg_embedding2 = np.mean(embeddings2, axis=0)
            similarity_overall = np.dot(avg_embedding1, avg_embedding2)
        else:
            similarity_overall = similarity_scenario_based
        
        # Cálculo de cobertura
        coverage_score = 0.0
        if scenarios1 and scenarios2:
            # Percentual de cenários do arquivo 1 com correspondência razoável
            threshold = 0.6  # Threshold para considerar correspondência válida
            good_matches = sum(1 for match in best_matches if match['similarity'] >= threshold)
            coverage_score = good_matches / len(scenarios1) if scenarios1 else 0.0
        
        return {
            'similarity_overall': float(similarity_overall),
            'similarity_scenario_based': float(similarity_scenario_based),
            'num_scenarios_file1': len(scenarios1),
            'num_scenarios_file2': len(scenarios2),
            'best_matches': best_matches,
            'coverage_score': float(coverage_score)
        }
    
    def compare_scenarios(self) -> None:
        """Compara todos os cenários e salva resultados"""
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
                # Comparação semântica
                metrics = self.compare_files_semantic(file1, file2)
                
                # Adicionar resultado
                self.results.append({
                    'repositorio': repo_name,
                    'arquivo': filename,
                    'similaridade_semantica': round(metrics['similarity_overall'], 4),
                    'similaridade_cenarios': round(metrics['similarity_scenario_based'], 4),
                    'cobertura': round(metrics['coverage_score'], 4),
                    'qtd_cenarios_arquivo1': metrics['num_scenarios_file1'],
                    'qtd_cenarios_arquivo2': metrics['num_scenarios_file2'],
                    'match_ratio': round(min(metrics['num_scenarios_file1'], metrics['num_scenarios_file2']) / 
                                        max(metrics['num_scenarios_file1'], metrics['num_scenarios_file2'], 1), 4)
                })
                
                print(f"  Similaridade semântica: {metrics['similarity_overall']:.4f}")
                print(f"  Similaridade por cenários: {metrics['similarity_scenario_based']:.4f}")
                print(f"  Cobertura: {metrics['coverage_score']:.2%}")
                print(f"  Cenários: {metrics['num_scenarios_file1']} vs {metrics['num_scenarios_file2']}")
                
            except Exception as e:
                print(f"Erro ao processar {repo_name}/{filename}: {e}")
                # Adicionar resultado com erro
                self.results.append({
                    'repositorio': repo_name,
                    'arquivo': filename,
                    'similaridade_semantica': 0.0,
                    'similaridade_cenarios': 0.0,
                    'cobertura': 0.0,
                    'qtd_cenarios_arquivo1': 0,
                    'qtd_cenarios_arquivo2': 0,
                    'match_ratio': 0.0,
                    'erro': str(e)
                })
        
        # Salvar resultados
        self._save_results()

        # Salvar estatísticas em TXT
        self._save_summary_statistics()
        
        # Estatísticas resumidas
        self._print_summary_statistics()
    
    def _save_results(self) -> None:
        """Salva os resultados em arquivo CSV"""
        os.makedirs(os.path.dirname(self.output_csv), exist_ok=True)
        
        # Determinar colunas baseadas nos resultados
        if self.results:
            fieldnames = list(self.results[0].keys())
        else:
            fieldnames = ['repositorio', 'arquivo', 'similaridade_semantica', 
                         'similaridade_cenarios', 'cobertura', 'qtd_cenarios_arquivo1',
                         'qtd_cenarios_arquivo2', 'match_ratio']
        
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in self.results:
                writer.writerow(result)
        
        print(f"\nResultados salvos em: {self.output_csv}")
        print(f"Total de comparações: {len(self.results)}")
    
    # def _print_summary_statistics(self) -> None:
    #     """Imprime estatísticas resumidas da comparação"""
    #     if not self.results:
    #         print("Nenhum resultado para analisar.")
    #         return
        
    #     # Filtrar resultados sem erro
    #     valid_results = [r for r in self.results if 'erro' not in r]
        
    #     if not valid_results:
    #         print("Nenhum resultado válido para estatísticas.")
    #         return
        
    #     print("\n" + "="*60)
    #     print("ESTATÍSTICAS RESUMIDAS DA COMPARAÇÃO")
    #     print("="*60)
        
    #     # Similaridade semântica
    #     similarities = [r['similaridade_semantica'] for r in valid_results]
    #     print(f"Similaridade Semântica:")
    #     print(f"  Média: {np.mean(similarities):.4f}")
    #     print(f"  Mediana: {np.median(similarities):.4f}")
    #     print(f"  Mínima: {np.min(similarities):.4f}")
    #     print(f"  Máxima: {np.max(similarities):.4f}")
    #     print(f"  Desvio Padrão: {np.std(similarities):.4f}")
        
    #     # Cobertura
    #     coverages = [r['cobertura'] for r in valid_results]
    #     print(f"\nCobertura (cenários com match > 0.6):")
    #     print(f"  Média: {np.mean(coverages):.2%}")
    #     print(f"  Mediana: {np.median(coverages):.2%}")
        
    #     # Análise de correspondência
    #     high_similarity = sum(1 for r in valid_results if r['similaridade_semantica'] > 0.7)
    #     medium_similarity = sum(1 for r in valid_results if 0.4 <= r['similaridade_semantica'] <= 0.7)
    #     low_similarity = sum(1 for r in valid_results if r['similaridade_semantica'] < 0.4)
        
    #     print(f"\nDistribuição de Similaridade:")
    #     print(f"  Alta (>0.7): {high_similarity} arquivos ({high_similarity/len(valid_results):.1%})")
    #     print(f"  Média (0.4-0.7): {medium_similarity} arquivos ({medium_similarity/len(valid_results):.1%})")
    #     print(f"  Baixa (<0.4): {low_similarity} arquivos ({low_similarity/len(valid_results):.1%})")
        
    #     # Contagem total de cenários
    #     total_scenarios_1 = sum(r['qtd_cenarios_arquivo1'] for r in valid_results)
    #     total_scenarios_2 = sum(r['qtd_cenarios_arquivo2'] for r in valid_results)
    #     print(f"\nTotal de Cenários:")
    #     print(f"  Arquivos 1 (LLM): {total_scenarios_1}")
    #     print(f"  Arquivos 2 (Humanos): {total_scenarios_2}")
    #     print(f"  Diferença: {abs(total_scenarios_1 - total_scenarios_2)}")
        
    #     print("="*60)


    def _print_summary_statistics(self) -> str:
        """Gera e retorna estatísticas resumidas da comparação como string"""
        if not self.results:
            return "Nenhum resultado para analisar."
        
        # Filtrar resultados sem erro
        valid_results = [r for r in self.results if 'erro' not in r]
        
        if not valid_results:
            return "Nenhum resultado válido para estatísticas."
        
        # Construir string de saída
        output = []
        output.append("=" * 60)
        output.append("ESTATÍSTICAS RESUMIDAS DA COMPARAÇÃO")
        output.append("=" * 60)
        
        # Similaridade semântica
        similarities = [r['similaridade_semantica'] for r in valid_results]
        output.append(f"Similaridade Semântica:")
        output.append(f"  Média: {np.mean(similarities):.4f}")
        output.append(f"  Mediana: {np.median(similarities):.4f}")
        output.append(f"  Mínima: {np.min(similarities):.4f}")
        output.append(f"  Máxima: {np.max(similarities):.4f}")
        output.append(f"  Desvio Padrão: {np.std(similarities):.4f}")
        
        # Cobertura
        coverages = [r['cobertura'] for r in valid_results]
        output.append(f"\nCobertura (cenários com match > 0.6):")
        output.append(f"  Média: {np.mean(coverages):.2%}")
        output.append(f"  Mediana: {np.median(coverages):.2%}")
        
        # Análise de correspondência
        high_similarity = sum(1 for r in valid_results if r['similaridade_semantica'] > 0.7)
        medium_similarity = sum(1 for r in valid_results if 0.4 <= r['similaridade_semantica'] <= 0.7)
        low_similarity = sum(1 for r in valid_results if r['similaridade_semantica'] < 0.4)
        
        output.append(f"\nDistribuição de Similaridade:")
        output.append(f"  Alta (>0.7): {high_similarity} arquivos ({high_similarity/len(valid_results):.1%})")
        output.append(f"  Média (0.4-0.7): {medium_similarity} arquivos ({medium_similarity/len(valid_results):.1%})")
        output.append(f"  Baixa (<0.4): {low_similarity} arquivos ({low_similarity/len(valid_results):.1%})")
        
        # Contagem total de cenários
        total_scenarios_1 = sum(r['qtd_cenarios_arquivo1'] for r in valid_results)
        total_scenarios_2 = sum(r['qtd_cenarios_arquivo2'] for r in valid_results)
        output.append(f"\nTotal de Cenários:")
        output.append(f"  Arquivos 1 (LLM): {total_scenarios_1}")
        output.append(f"  Arquivos 2 (Humanos): {total_scenarios_2}")
        output.append(f"  Diferença: {abs(total_scenarios_1 - total_scenarios_2)}")
        
        # Adicionar informações do modelo e configuração
        output.append(f"\nInformações da Execução:")
        output.append(f"  Modelo usado: {self.model_name}")
        output.append(f"  Dispositivo: {device}")
        output.append(f"  Total de arquivos comparados: {len(valid_results)}")
        output.append(f"  Data da análise: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        output.append("=" * 60)
        
        return "\n".join(output)

    def _generate_summary_statistics(self) -> str:
        """Alias para compatibilidade - chama _print_summary_statistics"""
        return self._print_summary_statistics()

    def _save_summary_statistics(self) -> None:
        """Salva as estatísticas resumidas em um arquivo TXT"""
        if not self.results:
            return
        
        # Determinar caminho do arquivo de estatísticas
        csv_path = Path(self.output_csv)
        stats_path = csv_path.with_suffix('.txt')
        
        # Gerar conteúdo das estatísticas
        stats_content = self._generate_summary_statistics()
        
        # Salvar em arquivo
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write(stats_content)
        
        print(f"Estatísticas salvas em: {stats_path}")

def main():
    """Função principal"""
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Configuração via variáveis de ambiente
    LLM_GENERATED_DIR = os.getenv('LLM_US_TO_TEST_OUTPUT_DIR')
    ORIGINAL_DIR = os.getenv('DIRETORIO_DESTINO_CONSOLIDADOS')
    SCENARIO_QUALITY_CSV = os.getenv('SCENARIO_QUALITY_CSV_EMBEDDING')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', "sentence-transformers/all-MiniLM-L6-v2")
    
    # Verificar se diretórios existem
    if not os.path.exists(LLM_GENERATED_DIR):
        print(f"Erro: Diretório não encontrado: {LLM_GENERATED_DIR}")
        return
    
    if not os.path.exists(ORIGINAL_DIR):
        print(f"Erro: Diretório não encontrado: {ORIGINAL_DIR}")
        return
    
    print("=== Comparador Semântico de Cenários Gherkin ===")
    print(f"Modelo: {EMBEDDING_MODEL}")
    print(f"Dispositivo: {device}")
    print(f"Diretório 1 (LLM): {LLM_GENERATED_DIR}")
    print(f"Diretório 2 (Humanos): {ORIGINAL_DIR}")
    print(f"Saída CSV: {SCENARIO_QUALITY_CSV}")
    print("-" * 40)
    
    # Criar comparador e executar
    comparator = AdvancedGherkinComparator(
        LLM_GENERATED_DIR, 
        ORIGINAL_DIR, 
        SCENARIO_QUALITY_CSV,
        model_name=EMBEDDING_MODEL
    )
    
    comparator.compare_scenarios()


if __name__ == "__main__":
    # Parse de argumentos de linha de comando opcional
    parser = argparse.ArgumentParser(description="Comparador semântico de cenários Gherkin")
    parser.add_argument("--model", type=str, default=None, 
                       help="Nome do modelo de embeddings da Hugging Face")
    args = parser.parse_args()
    
    # Sobrescrever modelo se fornecido via linha de comando
    if args.model:
        os.environ['EMBEDDING_MODEL'] = args.model
    
    main()