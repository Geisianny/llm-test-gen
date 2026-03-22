import os
import shutil
from datetime import datetime
import re
from dotenv import load_dotenv

load_dotenv()

DIRETORIO_ORIGEM = os.getenv('LLM_US_TO_TEST_OUTPUT_DIR')
DIRETORIO_DESTINO = os.getenv('CONVERSOR_FEATURES_OUTPUT')

def sanitizar_nome_arquivo(nome):
    nome_sanitizado = re.sub(r'[^\w\s-]', '', nome)
    nome_sanitizado = re.sub(r'[-\s]+', '_', nome_sanitizado)
    return nome_sanitizado.strip('-_')

def extrair_cenarios(conteudo):
    cenarios = []
    cenario_atual = []
    dentro_cenario = False
    
    linhas = conteudo.split('\n')
    
    for linha in linhas:
        linha = linha.rstrip()  
        
        if linha.strip().startswith('Scenario:') or linha.strip().startswith('Scenario Outline:'):
            if dentro_cenario and cenario_atual:
                
                cenarios.append('\n'.join(cenario_atual))
                cenario_atual = []
            
            dentro_cenario = True
            cenario_atual.append(linha)
        elif dentro_cenario:
            if linha.strip() == '' and not cenario_atual[-1].strip() == '':
                cenario_atual.append(linha)
            elif linha.strip() != '':
                cenario_atual.append(linha)
    
    if dentro_cenario and cenario_atual:
        cenarios.append('\n'.join(cenario_atual))
    
    return cenarios

def gerar_nome_feature(conteudo_cenario):
    primeira_linha = conteudo_cenario.strip().split('\n')[0] if conteudo_cenario.strip() else ''
    if primeira_linha.startswith('Scenario:') or primeira_linha.startswith('Scenario Outline:'):
        nome_cenario = primeira_linha.replace('Scenario:', '').replace('Scenario Outline:', '').strip()
        return f"Feature: {nome_cenario}"
    else:

        palavras = conteudo_cenario.strip().split()[:5]
        nome_fallback = ' '.join(palavras)
        return f"Feature: {nome_fallback}"

def adicionar_descricao_feature(conteudo):

    descricao = "\n  As a user\n  I want to use the system\n  So that I can accomplish my tasks\n"
    return descricao

def converter_cenario_para_feature(conteudo_cenario, nome_arquivo_origem, indice_cenario):
    
    try:
    
        linha_feature = gerar_nome_feature(conteudo_cenario)
        
        conteudo_final = f"{linha_feature}\n\n{conteudo_cenario}\n\n"
        
        nome_base = os.path.splitext(nome_arquivo_origem)[0]
        primeira_linha = conteudo_cenario.strip().split('\n')[0]
        nome_cenario = primeira_linha.replace('Scenario:', '').replace('Scenario Outline:', '').strip()
        nome_cenario_sanitizado = sanitizar_nome_arquivo(nome_cenario)
        
        if nome_cenario_sanitizado:
            nome_feature_arquivo = f"{nome_base}_{indice_cenario:02d}_{nome_cenario_sanitizado}.feature"
        else:
            nome_feature_arquivo = f"{nome_base}_{indice_cenario:02d}.feature"
        
        return {
            'arquivo_destino': nome_feature_arquivo,
            'conteudo_original': conteudo_cenario,
            'conteudo_feature': conteudo_final,
            'sucesso': True
        }
    
    except Exception as e:
        return {
            'arquivo_destino': '',
            'conteudo_original': '',
            'conteudo_feature': '',
            'sucesso': False,
            'erro': str(e)
        }

def processar_arquivo_txt(caminho_arquivo):
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo_original = f.read().strip()

        nome_arquivo = os.path.basename(caminho_arquivo)
 
        cenarios = extrair_cenarios(conteudo_original)
        
        if not cenarios:
           
            cenarios = [conteudo_original]
        
        resultados = []
        for indice, cenario in enumerate(cenarios, 1):
            resultado = converter_cenario_para_feature(cenario, nome_arquivo, indice)
            resultado['arquivo_origem'] = caminho_arquivo
            resultado['indice_cenario'] = indice
            resultados.append(resultado)
        
        return resultados
    
    except Exception as e:
        return [{
            'arquivo_origem': caminho_arquivo,
            'arquivo_destino': '',
            'conteudo_original': '',
            'conteudo_feature': '',
            'sucesso': False,
            'erro': str(e)
        }]

def processar_diretorio(diretorio_origem, diretorio_destino):
   
    os.makedirs(diretorio_destino, exist_ok=True)
    
    arquivos_txt = []
    for raiz, diretorios, arquivos in os.walk(diretorio_origem):
        for arquivo in arquivos:
            if arquivo.endswith('.txt'):
                caminho_completo = os.path.join(raiz, arquivo)
                arquivos_txt.append(caminho_completo)
    
    if not arquivos_txt:
        print(f"Nenhum arquivo .txt encontrado em '{diretorio_origem}' e subdiretórios")
        return []
    
    resultados = []
    print(f"Processando {len(arquivos_txt)} arquivos...")
    
    for arquivo in arquivos_txt:
        print(f"Processando arquivo: {os.path.basename(arquivo)}")
        resultados_arquivo = processar_arquivo_txt(arquivo)
        resultados.extend(resultados_arquivo)
        
        for resultado in resultados_arquivo:
            if resultado['sucesso']:
                caminho_destino = os.path.join(diretorio_destino, resultado['arquivo_destino'])
                with open(caminho_destino, 'w', encoding='utf-8') as f:
                    f.write(resultado['conteudo_feature'])
                
                print(f"CENÁRIO {resultado['indice_cenario']} -> {resultado['arquivo_destino']}")
            else:
                print(f"ERRO no cenário {resultado.get('indice_cenario', '?')}: {resultado.get('erro', 'Erro desconhecido')}")
    
    return resultados

def gerar_relatorio_conversao(resultados, diretorio_destino):
    caminho_relatorio = os.path.join(diretorio_destino, f"relatorio_conversao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(caminho_relatorio, 'w', encoding='utf-8') as relatorio:
        relatorio.write("RELATÓRIO DE CONVERSÃO TXT PARA FEATURE\n")
        relatorio.write("=" * 60 + "\n")
        relatorio.write(f"Data da conversão: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        relatorio.write(f"Diretório de origem: {DIRETORIO_ORIGEM}\n")
        relatorio.write(f"Diretório de destino: {DIRETORIO_DESTINO}\n\n")
        
        total_cenarios = len(resultados)
        cenarios_sucesso = sum(1 for r in resultados if r['sucesso'])
        cenarios_erro = total_cenarios - cenarios_sucesso
        
        arquivos_processados = set(r['arquivo_origem'] for r in resultados)
        
        relatorio.write("ESTATÍSTICAS:\n")
        relatorio.write(f"Total de arquivos processados: {len(arquivos_processados)}\n")
        relatorio.write(f"Total de cenários extraídos: {total_cenarios}\n")
        relatorio.write(f"Cenários convertidos com sucesso: {cenarios_sucesso}\n")
        relatorio.write(f"Cenários com erro: {cenarios_erro}\n\n")
        
        relatorio.write("DETALHAMENTO POR ARQUIVO:\n")
        relatorio.write("=" * 60 + "\n")
        
        for arquivo in sorted(arquivos_processados):
            cenarios_arquivo = [r for r in resultados if r['arquivo_origem'] == arquivo]
            sucesso_arquivo = sum(1 for r in cenarios_arquivo if r['sucesso'])
            
            relatorio.write(f"\nArquivo: {os.path.basename(arquivo)}\n")
            relatorio.write(f"Caminho: {arquivo}\n")
            relatorio.write(f"Cenários: {len(cenarios_arquivo)} ({sucesso_arquivo} | ✗ {len(cenarios_arquivo) - sucesso_arquivo})\n")
            
            for resultado in cenarios_arquivo:
                if resultado['sucesso']:
                    relatorio.write(f"{resultado['arquivo_destino']}\n")
                else:
                    relatorio.write(f"ERRO: {resultado.get('erro', 'Desconhecido')}\n")
            
            relatorio.write("-" * 40 + "\n")
    
    return caminho_relatorio

def main():
    print("=== CONVERSOR TXT PARA FEATURE ===\n")
    print(f"Diretório de origem: {DIRETORIO_ORIGEM}")
    print(f"Diretório de destino: {DIRETORIO_DESTINO}")
    
    if not os.path.exists(DIRETORIO_ORIGEM):
        print(f"\nErro: Diretório '{DIRETORIO_ORIGEM}' não encontrado.")
        return
    
    resultados = processar_diretorio(DIRETORIO_ORIGEM, DIRETORIO_DESTINO)
    
    if resultados:

        relatorio = gerar_relatorio_conversao(resultados, DIRETORIO_DESTINO)
        
        arquivos_processados = set(r['arquivo_origem'] for r in resultados)
        cenarios_sucesso = sum(1 for r in resultados if r['sucesso'])
        
        print(f"\n=== CONVERSÃO CONCLUÍDA ===")
        print(f"Arquivos processados: {len(arquivos_processados)}")
        print(f"Cenários convertidos: {cenarios_sucesso}")
        print(f"Arquivos de saída salvos em: {DIRETORIO_DESTINO}")
        print(f"Relatório gerado em: {relatorio}")
    else:
        print("\nNenhum arquivo foi processado.")

if __name__ == "__main__":
    main()