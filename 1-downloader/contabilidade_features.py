import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def main():

    load_dotenv()

    input_path = os.getenv("DOWNLOADER_OUTPUT")
    output_path = os.getenv("DOWNLOADER_SUMMARY")

    DIRETORIO_INPUT = Path(input_path)  
    DIRETORIO_OUTPUT = Path(output_path)   
    NOME_ARQUIVO_RELATORIO = "repositories_summary.txt" 
    
    if len(sys.argv) >= 2:
        DIRETORIO_INPUT = Path(sys.argv[1])
    if len(sys.argv) >= 3:
        DIRETORIO_OUTPUT = Path(sys.argv[2])
    if len(sys.argv) >= 4:
        NOME_ARQUIVO_RELATORIO = sys.argv[3]

    if not DIRETORIO_INPUT.is_dir():
        print(f"Erro: Diretório de entrada '{DIRETORIO_INPUT}' não encontrado")
        sys.exit(1)
    
    DIRETORIO_OUTPUT.mkdir(parents=True, exist_ok=True)
    
    caminho_relatorio = DIRETORIO_OUTPUT / NOME_ARQUIVO_RELATORIO

    repositorios_com_features = 0
    total_arquivos_features = 0
    relatorio = []

    print(f"Processando diretório: {DIRETORIO_INPUT}")
    
    for item in DIRETORIO_INPUT.iterdir():
        if item.is_dir():
            arquivos_features = list(item.rglob("*.feature"))
            qtd_features = len(arquivos_features)
            
            if qtd_features > 0:
                repositorios_com_features += 1
                total_arquivos_features += qtd_features
                relatorio.append(f"{item.name}: {qtd_features} arquivo(s) .feature")

    with open(caminho_relatorio, "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE ARQUIVOS .FEATURE\n")
        f.write("=" * 40 + "\n")
        f.write(f"Diretório analisado: {DIRETORIO_INPUT}\n")
        f.write(f"Repositórios com arquivos .feature: {repositorios_com_features}\n\n")
        f.write("Detalhamento por repositório:\n")
        for linha in relatorio:
            f.write(linha + "\n")
        f.write(f"\nTotal geral de arquivos .feature: {total_arquivos_features}\n")

    print(f"Relatório gerado com sucesso em: {caminho_relatorio}")
    print(f"Resumo:")
    print(f"- Repositórios com features: {repositorios_com_features}")
    print(f"- Total de arquivos .feature: {total_arquivos_features}")

if __name__ == "__main__":
    main()