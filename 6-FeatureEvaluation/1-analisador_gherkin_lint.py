import os
import subprocess
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DIRETORIO_FEATURES = os.getenv('SCENARIOS_ORIGINAIS_DIR') 
DIRETORIO_RELATORIOS = os.getenv('GHERKIN_LINT_SCENARIO_ORIGINAIS') 
CAMINHO_GHERKIN_LINT = os.getenv('GHERKIN_LINT_PATH') 
CAMINHO_CONFIGURACAO = os.getenv('GHERKIN_LINT_CONFIG_LINTRC') 

def executar_gherkin_lint(arquivo_feature):
    print("CAMINHO_GHERKIN_LINT: ")
    print(CAMINHO_GHERKIN_LINT)

    print("CAMINHO_CONFIGURACAO: ")
    print(CAMINHO_CONFIGURACAO)

    print("arquivo_feature: ")
    print(arquivo_feature)

    comando = f"node {CAMINHO_GHERKIN_LINT} -c {CAMINHO_CONFIGURACAO} {arquivo_feature}"

    print("comando: ")
    print(comando)
    
    print("============================================")

    try:
       
        resultado = subprocess.run(
            comando, 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding='utf-8'
        )
        
        return {
            'arquivo': arquivo_feature,
            'comando': comando,
            'sucesso': resultado.returncode == 0,
            'codigo_saida': resultado.returncode,
            'saida_stdout': resultado.stdout,
            'saida_stderr': resultado.stderr,
            'erro_execucao': False
        }
    
    except Exception as e:
        return {
            'arquivo': arquivo_feature,
            'comando': comando,
            'sucesso': False,
            'codigo_saida': -1,
            'saida_stdout': '',
            'saida_stderr': str(e),
            'erro_execucao': True
        }

def analisar_saida_lint(resultado):
    
    if resultado['erro_execucao']:

        print("ENTROU no IF AQUI")

        return {
            'erros': [],
            'aviso_erro_execucao': resultado['saida_stderr']
        }
    
    try:
        saida_json = json.loads(resultado['saida_stderr'])
        
        print("ENTROU NO TRY")

        return {
            'erros': saida_json,
            'aviso_erro_execucao': None
        }
    except json.JSONDecodeError:
        erros = []
        linhas = resultado['saida_stderr'].split('\n')
        
        for linha in linhas:
            linha = linha.strip()
            if linha and not linha == '/n':
                erros.append(linha)

        print("ENTROU NO except")
        
        return {
            'erros': erros,
            'aviso_erro_execucao': None
        }

def contar_erros_por_tipo(erros):

    contagem = {}
    
    for erro in erros:
        if isinstance(erro, dict):
            regra = erro.get('rule', 'unknown')
            contagem[regra] = contagem.get(regra, 0) + 1
        else:
            if 'error' in erro.lower():
                contagem['error'] = contagem.get('error', 0) + 1
            elif 'warning' in erro.lower():
                contagem['warning'] = contagem.get('warning', 0) + 1
            else:
                contagem['other'] = contagem.get('other', 0) + 1
    
    return contagem

def encontrar_arquivos_feature(diretorio_base):
    
    arquivos_feature = []
    
    for raiz, _, arquivos in os.walk(diretorio_base):
        for arquivo in arquivos:
            if arquivo.endswith('.feature'):
                caminho_completo = os.path.join(raiz, arquivo)
                
                caminho_relativo = os.path.relpath(caminho_completo, diretorio_base)
                arquivos_feature.append((caminho_completo, caminho_relativo))
    
    return arquivos_feature

def processar_diretorio_features(diretorio_features):

    if not os.path.exists(diretorio_features):
        print(f"Erro: Diretório '{diretorio_features}' não encontrado.")
        return []
    
    arquivos_feature = encontrar_arquivos_feature(diretorio_features)
    
    if not arquivos_feature:
        print(f"Nenhum arquivo .feature encontrado em '{diretorio_features}'")
        return []
    
    resultados = []
    print(f"Analisando {len(arquivos_feature)} arquivos .feature com gherkin-lint...")
    
    for caminho_completo, caminho_relativo in arquivos_feature:
        print(f"Analisando: {caminho_relativo}")
        
        resultado = executar_gherkin_lint(caminho_completo)
        analise = analisar_saida_lint(resultado)
        
        resultado_completo = {
            **resultado,
            'analise': analise,
            'contagem_erros': contar_erros_por_tipo(analise['erros']),
            'quantidade_erros': len(analise['erros']),
            'caminho_relativo': caminho_relativo
        }
        
        resultados.append(resultado_completo)
        
        relatorio_individual = gerar_relatorio_individual(resultado_completo, DIRETORIO_RELATORIOS)
        
        if resultado['erro_execucao']:
            print(f"ERRO NA EXECUÇÃO: {resultado['saida_stderr']}")
            print(f"Relatório individual: {relatorio_individual}")
        elif resultado_completo['quantidade_erros'] == 0:
            print(f"VÁLIDO (sem problemas encontrados)")
            print(f"Relatório individual: {relatorio_individual}")
        else:
            print(f"ENCONTRADOS {resultado_completo['quantidade_erros']} PROBLEMAS")
            print(f"Relatório individual: {relatorio_individual}")
    
    return resultados

def gerar_relatorio_lint(resultados, diretorio_saida):
    
    os.makedirs(diretorio_saida, exist_ok=True)
    
    caminho_relatorio = os.path.join(diretorio_saida, f"relatorio_gherkin_lint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(caminho_relatorio, 'w', encoding='utf-8') as relatorio:
        relatorio.write("RELATÓRIO DE ANÁLISE GHERKIN-LINT\n")
        relatorio.write("=" * 80 + "\n")
        relatorio.write(f"Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        relatorio.write(f"Diretório analisado: {DIRETORIO_FEATURES}\n")
        relatorio.write(f"Comando gherkin-lint: {CAMINHO_GHERKIN_LINT}\n")
        relatorio.write(f"Arquivo de configuração: {CAMINHO_CONFIGURACAO}\n\n")
        
        total_arquivos = len(resultados)
        arquivos_validos = sum(1 for r in resultados if r['quantidade_erros'] == 0 and not r['erro_execucao'])
        arquivos_com_erros = sum(1 for r in resultados if r['quantidade_erros'] > 0)
        arquivos_erro_execucao = sum(1 for r in resultados if r['erro_execucao'])
        total_erros = sum(r['quantidade_erros'] for r in resultados)
        
        relatorio.write("ESTATÍSTICAS GERAIS:\n")
        relatorio.write(f"Total de arquivos analisados: {total_arquivos}\n")
        relatorio.write(f"Arquivos válidos (sem problemas): {arquivos_validos}\n")
        relatorio.write(f"Arquivos com problemas de lint: {arquivos_com_erros}\n")
        relatorio.write(f"Arquivos com erro na execução: {arquivos_erro_execucao}\n")
        relatorio.write(f"Total de problemas encontrados: {total_erros}\n\n")
        
        todos_erros = {}
        for resultado in resultados:
            for tipo_erro, quantidade in resultado['contagem_erros'].items():
                todos_erros[tipo_erro] = todos_erros.get(tipo_erro, 0) + quantidade
        
        if todos_erros:
            relatorio.write("DISTRIBUIÇÃO DOS PROBLEMAS POR TIPO:\n")
            for tipo_erro, quantidade in sorted(todos_erros.items(), key=lambda x: x[1], reverse=True):
                relatorio.write(f"  {tipo_erro}: {quantidade} ocorrências\n")
            relatorio.write("\n")
        
        relatorio.write("DETALHAMENTO POR ARQUIVO:\n")
        relatorio.write("=" * 80 + "\n")
        
        for resultado in resultados:
            relatorio.write(f"\nArquivo: {resultado['caminho_relativo']}\n")
            relatorio.write(f"Comando executado: {resultado['comando']}\n")
            
            if resultado['erro_execucao']:
                relatorio.write("Status: ERRO NA EXECUÇÃO DO GHERKIN-LINT\n")
                relatorio.write(f"Erro: {resultado['saida_stderr']}\n")
            elif resultado['quantidade_erros'] == 0:
                relatorio.write("Status: VÁLIDO (sem problemas encontrados)\n")
            else:
                relatorio.write(f"Status: ENCONTRADOS {resultado['quantidade_erros']} PROBLEMAS\n")
                
                relatorio.write("Problemas encontrados:\n")
                for i, erro in enumerate(resultado['analise']['erros'], 1):
                    if isinstance(erro, dict):
                        relatorio.write(f"  {i}. [Linha {erro.get('line', 'N/A')}] {erro.get('rule', 'Unknown rule')}\n")
                        relatorio.write(f"      Mensagem: {erro.get('message', 'No message')}\n")
                        if 'element' in erro:
                            relatorio.write(f"      Elemento: {erro['element']}\n")
                    else:
                        relatorio.write(f"  {i}. {erro}\n")
            
            if resultado['saida_stderr'] and not resultado['erro_execucao']:
                relatorio.write("Avisos/adicionais:\n")
                relatorio.write(f"  {resultado['saida_stderr']}\n")
            
            relatorio.write("-" * 80 + "\n")
        
        relatorio.write("\nRECOMENDAÇÕES:\n")
        relatorio.write("=" * 80 + "\n")
        
        if arquivos_com_erros > 0:
            relatorio.write(f"\n{arquivos_com_erros} arquivo(s) precisam de correções:\n")
            for resultado in resultados:
                if resultado['quantidade_erros'] > 0 and not resultado['erro_execucao']:
                    relatorio.write(f"- {resultado['caminho_relativo']}: {resultado['quantidade_erros']} problemas\n")
        
        if arquivos_erro_execucao > 0:
            relatorio.write(f"\n{arquivos_erro_execucao} arquivo(s) tiveram erro na execução:\n")
            relatorio.write("Verifique se o gherkin-lint está instalado corretamente.\n")
            relatorio.write("Comando de instalação: npm install -g gherkin-lint\n")
    
    return caminho_relatorio

def gerar_relatorio_individual(resultado, diretorio_saida):
   
    caminho_relativo = resultado['caminho_relativo']
    
    nome_base = os.path.splitext(caminho_relativo)[0]
    nome_relatorio = f"{nome_base}_relatorio.txt"
    
    caminho_relatorio_completo = os.path.join(diretorio_saida, nome_relatorio)
    
    os.makedirs(os.path.dirname(caminho_relatorio_completo), exist_ok=True)
    
    with open(caminho_relatorio_completo, 'w', encoding='utf-8') as relatorio:
        relatorio.write("RELATÓRIO INDIVIDUAL - ANÁLISE GHERKIN-LINT\n")
        relatorio.write("=" * 60 + "\n")
        relatorio.write(f"Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        relatorio.write(f"Arquivo analisado: {resultado['arquivo']}\n")
        relatorio.write(f"Comando executado: {resultado['comando']}\n\n")
        
        if resultado['erro_execucao']:
            relatorio.write("Status: ERRO NA EXECUÇÃO DO GHERKIN-LINT\n")
            relatorio.write(f"Erro: {resultado['saida_stderr']}\n")
        elif resultado['quantidade_erros'] == 0:
            relatorio.write("Status: VÁLIDO (sem problemas encontrados)\n")
        else:
            relatorio.write(f"Status: ENCONTRADOS {resultado['quantidade_erros']} PROBLEMAS\n\n")
            
            relatorio.write("PROBLEMAS ENCONTRADOS:\n")
            relatorio.write("-" * 40 + "\n")
            for i, erro in enumerate(resultado['analise']['erros'], 1):
                if isinstance(erro, dict):
                    relatorio.write(f"{i}. [Linha {erro.get('line', 'N/A')}] {erro.get('rule', 'Unknown rule')}\n")
                    relatorio.write(f"   Mensagem: {erro.get('message', 'No message')}\n")
                    if 'element' in erro:
                        relatorio.write(f"   Elemento: {erro['element']}\n")
                else:
                    relatorio.write(f"{i}. {erro}\n")
                relatorio.write("\n")
        
        if resultado['saida_stderr'] and not resultado['erro_execucao']:
            relatorio.write("AVISOS/INFORMAÇÕES ADICIONAIS:\n")
            relatorio.write("-" * 40 + "\n")
            relatorio.write(f"{resultado['saida_stderr']}\n")
        
        if resultado['contagem_erros']:
            relatorio.write("\nRESUMO DOS PROBLEMAS POR TIPO:\n")
            relatorio.write("-" * 40 + "\n")
            for tipo_erro, quantidade in resultado['contagem_erros'].items():
                relatorio.write(f"  {tipo_erro}: {quantidade} ocorrência(s)\n")
    
    return caminho_relatorio_completo

def verificar_dependencias():

    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
        
        comando_verificacao = f"{CAMINHO_GHERKIN_LINT} --version"
        resultado = subprocess.run(comando_verificacao, shell=True, capture_output=True, text=True)
        
        if not os.path.exists(CAMINHO_CONFIGURACAO):
            print(f"Aviso: Arquivo de configuração não encontrado: {CAMINHO_CONFIGURACAO}")
            print("Criando arquivo de configuração padrão...")
            criar_configuracao_padrao()
        
        return True
    
    except subprocess.CalledProcessError:
        print("Erro: Node.js não está instalado ou não está no PATH.")
        print("Instale o Node.js para usar o gherkin-lint.")
        return False
    except Exception as e:
        print(f"Erro ao verificar dependências: {e}")
        return False

def criar_configuracao_padrao():
    
    config_padrao = {
        "no-files-without-scenarios": "off",
        "no-unnamed-features": "off",
        "no-unnamed-scenarios": "off",
        "no-duplicate-scenario-names": "error",
        "no-duplicate-feature-names": "error",
        "no-partially-commented-tag-lines": "error",
        "no-trailing-spaces": "error",
        "no-multiple-empty-lines": "error"
    }
    
    try:
        with open(CAMINHO_CONFIGURACAO, 'w', encoding='utf-8') as f:
            json.dump(config_padrao, f, indent=2)
        print(f"Arquivo de configuração criado: {CAMINHO_CONFIGURACAO}")
    except Exception as e:
        print(f"Erro ao criar arquivo de configuração: {e}")

def main():

    print("=== ANALISADOR GHERKIN-LINT ===\n")
    print(f"Diretório de features: {DIRETORIO_FEATURES}")
    print(f"Diretório de relatórios: {DIRETORIO_RELATORIOS}")
    print(f"Caminho do gherkin-lint: {CAMINHO_GHERKIN_LINT}")
    print(f"Arquivo de configuração: {CAMINHO_CONFIGURACAO}")
    
    print("\nVerificando dependências...")
    if not verificar_dependencias():
        print("Erro: Dependências não atendidas. Verifique as mensagens acima.")
        return
    
    resultados = processar_diretorio_features(DIRETORIO_FEATURES)
    
    if resultados:
    
        relatorio_consolidado = gerar_relatorio_lint(resultados, DIRETORIO_RELATORIOS)
        
        arquivos_validos = sum(1 for r in resultados if r['quantidade_erros'] == 0 and not r['erro_execucao'])
        total_erros = sum(r['quantidade_erros'] for r in resultados)
        
        print(f"\n=== ANÁLISE CONCLUÍDA ===")
        print(f"Total de arquivos: {len(resultados)}")
        print(f"Arquivos válidos: {arquivos_validos}")
        print(f"Total de problemas encontrados: {total_erros}")
        print(f"Relatórios individuais salvos em: {DIRETORIO_RELATORIOS}")
        print(f"Relatório consolidado salvo em: {relatorio_consolidado}")
    else:
        print("\nNenhum arquivo foi processado.")

if __name__ == "__main__":
    main()