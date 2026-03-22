import os
import re
from pathlib import Path
from dotenv import load_dotenv

def separar_cenarios_gherkin(diretorio_entrada, diretorio_saida):
    
    padrao_arquivo = re.compile(r'(.*)_story_processado\.txt$', re.IGNORECASE)
    
    for raiz, dirs, arquivos in os.walk(diretorio_entrada):
        for arquivo in arquivos:
            if arquivo.endswith('.txt'):
                match = padrao_arquivo.match(arquivo)
                if match:
                    nome_base = match.group(1) 
                    
                    caminho_original = os.path.join(raiz, arquivo)
                    
                    caminho_relativo = os.path.relpath(raiz, diretorio_entrada)
                    
                    caminho_saida = os.path.join(diretorio_saida, caminho_relativo)
                    os.makedirs(caminho_saida, exist_ok=True)
                    
                    processar_arquivo(caminho_original, caminho_saida, nome_base)

def processar_arquivo(caminho_arquivo, caminho_saida, nome_base):
   
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        padrao_cenario = re.compile(r'^(Scenario(?:\s+Outline)?:[^\n]*\n(?:[ \t].*\n)*)', 
                                    re.MULTILINE)
        
        cenarios = padrao_cenario.findall(conteudo)
        
        print(f"Processando: {caminho_arquivo}")
        print(f"Encontrados {len(cenarios)} cenários")
        
        for i, cenario in enumerate(cenarios, 1):
            cenario_limpo = cenario.strip()
            
            nome_arquivo = f"{nome_base}_scenario_{i}.txt"
            caminho_completo = os.path.join(caminho_saida, nome_arquivo)
            
            with open(caminho_completo, 'w', encoding='utf-8') as f:
                f.write(cenario_limpo + '\n')
            
            print(f"  Salvo: {nome_arquivo}")
            
    except UnicodeDecodeError:

        try:
            with open(caminho_arquivo, 'r', encoding='latin-1') as f:
                conteudo = f.read()
            
            padrao_cenario = re.compile(r'^(Scenario(?:\s+Outline)?:[^\n]*\n(?:[ \t].*\n)*)', 
                                        re.MULTILINE)
            cenarios = padrao_cenario.findall(conteudo)
            
            print(f"Processando (latin-1): {caminho_arquivo}")
            print(f"Encontrados {len(cenarios)} cenários")
            
            for i, cenario in enumerate(cenarios, 1):
                cenario_limpo = cenario.strip()
                nome_arquivo = f"{nome_base}_scenario_{i}.txt"
                caminho_completo = os.path.join(caminho_saida, nome_arquivo)
                
                with open(caminho_completo, 'w', encoding='utf-8') as f:
                    f.write(cenario_limpo + '\n')
                
                print(f"  Salvo: {nome_arquivo}")
                
        except Exception as e:
            print(f"Erro ao processar {caminho_arquivo}: {e}")
    
    except Exception as e:
        print(f"Erro ao processar {caminho_arquivo}: {e}")

def main():

    load_dotenv()
    
    
    diretorio_entrada = os.getenv('LLM_US_TO_TEST_OUTPUT_DIR')
    diretorio_saida = os.getenv('SCENARIOS_SPLITED_DIR')
    
    if not diretorio_entrada or not diretorio_saida:
        print("Erro: DIRETORIO_ENTRADA e DIRETORIO_SAIDA devem ser definidos no arquivo .env")
        print("\nExemplo de conteúdo do arquivo .env:")
        print("DIRETORIO_ENTRADA=./dados/entrada")
        print("DIRETORIO_SAIDA=./dados/saida")
        return
    
    diretorio_entrada = os.path.abspath(diretorio_entrada)
    diretorio_saida = os.path.abspath(diretorio_saida)
    
    if not os.path.exists(diretorio_entrada):
        print(f"Erro: Diretório de entrada não encontrado: {diretorio_entrada}")
        return
    
    print("=" * 60)
    print("SEPARADOR DE CENÁRIOS GHERKIN")
    print("=" * 60)
    print(f"Diretório de entrada: {diretorio_entrada}")
    print(f"Diretório de saída: {diretorio_saida}")
    print("-" * 60)
    
    os.makedirs(diretorio_saida, exist_ok=True)

    separar_cenarios_gherkin(diretorio_entrada, diretorio_saida)
    
    print("-" * 60)
    print("Processamento concluído!")
    print("=" * 60)

if __name__ == "__main__":
    main()