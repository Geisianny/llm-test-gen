import os
import csv
import argparse
from dotenv import load_dotenv

def processar_diretorios(diretorio_base, arquivo_saida='user_stories.csv'):
    
    if not os.path.exists(diretorio_base):
        print(f"Erro: Diretório '{diretorio_base}' não encontrado.")
        return
    
    dados_csv = []
    
    for repositorio in os.listdir(diretorio_base):
        caminho_repositorio = os.path.join(diretorio_base, repositorio)
        
        if os.path.isdir(caminho_repositorio):
            print(f"Processando repositório: {repositorio}")
            
            for arquivo in os.listdir(caminho_repositorio):
                if arquivo.endswith('.txt'):
                    caminho_arquivo = os.path.join(caminho_repositorio, arquivo)
                    
                    try:
                        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                            conteudo = f.read().strip()
                        
                        dados_csv.append({
                            'repositorio': repositorio,
                            'arquivo': arquivo,
                            'conteudo': conteudo
                        })
                        
                        print(f"  ✓ {arquivo}")
                        
                    except Exception as e:
                        print(f"  ✗ Erro ao ler {arquivo}: {e}")
    
    if dados_csv:
        try:
            with open(arquivo_saida, 'w', newline='', encoding='utf-8') as csvfile:
                
                campo_nomes = ['repositorio', 'arquivo', 'conteudo']
                writer = csv.DictWriter(csvfile, fieldnames=campo_nomes)
                
                writer.writeheader()
                writer.writerows(dados_csv)
            
            print(f"\nCSV criado com sucesso: {arquivo_saida}")
            print(f"Total de estórias processadas: {len(dados_csv)}")
            
        except Exception as e:
            print(f"Erro ao criar CSV: {e}")
    else:
        print("Nenhum arquivo txt encontrado para processar.")

def main():

    load_dotenv()
        
    INPUT = os.getenv("RANDON_SELECTOR_OUTPUT")
    CSV_OUTPUT = os.getenv("US_TO_CSV_OUTPUT") 
    
    processar_diretorios(INPUT, CSV_OUTPUT)

if __name__ == "__main__":
    main()