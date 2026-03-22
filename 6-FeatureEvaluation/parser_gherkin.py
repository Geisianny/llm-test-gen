import os
from datetime import datetime
from gherkin.parser import Parser
from gherkin.errors import ParserError
from dotenv import load_dotenv

load_dotenv()
DIRETORIO_CENARIOS = os.getenv('SCENARIOS_ORIGINAIS_DIR')
DIRETORIO_RELATORIOS = os.getenv('PARSER_GHERKIN_SCENARIO_ORIGINAIS')

def corrigir_falta_de_feature(conteudo):
   
    linhas = conteudo.split('\n')
    
    for linha in linhas:
        if linha.strip().startswith('Feature:'):
            return conteudo, False 
    
    feature_name = "Auto-generated Feature"
    if linhas and linhas[0].strip().startswith('Scenario:'):
        
        scenario_name = linhas[0].replace('Scenario:', '').strip()
        feature_name = f"Feature for: {scenario_name}"
    
    conteudo_corrigido = f"Feature: {feature_name}\n\n{conteudo}"
    return conteudo_corrigido, True

def analisar_arquivo_gherkin(caminho_arquivo):
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo_original = f.read()

        parser = Parser()
        correcao_aplicada = False
        conteudo = conteudo_original
        
        try:
            documento_analisado = parser.parse(conteudo)
        except ParserError as e:
           
            conteudo, correcao_aplicada = corrigir_falta_de_feature(conteudo_original)
            if correcao_aplicada:
                try:
                    documento_analisado = parser.parse(conteudo)
                except ParserError as e2:
                    return {
                        'arquivo': caminho_arquivo,
                        'valido': False,
                        'erros': [f"Erro de parsing mesmo após correção: {str(e2)}"],
                        'documento': None,
                        'correcao_aplicada': correcao_aplicada
                    }
            else:
                return {
                    'arquivo': caminho_arquivo,
                    'valido': False,
                    'erros': [f"Erro de parsing: {str(e)}"],
                    'documento': None,
                    'correcao_aplicada': False
                }
        
        erros = verificar_estrutura_gherkin(documento_analisado)
        
        return {
            'arquivo': caminho_arquivo,
            'valido': len(erros) == 0,
            'erros': erros,
            'documento': documento_analisado if len(erros) == 0 else None,
            'correcao_aplicada': correcao_aplicada
        }
    except UnicodeDecodeError:
        return {
            'arquivo': caminho_arquivo,
            'valido': False,
            'erros': ["Erro de codificação: arquivo não está em UTF-8"],
            'documento': None,
            'correcao_aplicada': False
        }
    except Exception as e:
        return {
            'arquivo': caminho_arquivo,
            'valido': False,
            'erros': [f"Erro inesperado: {str(e)}"],
            'documento': None,
            'correcao_aplicada': False
        }

def verificar_estrutura_gherkin(documento):

    erros = []
    
    if not documento:
        erros.append("Documento vazio ou nulo")
        return erros
    
    if 'feature' not in documento or not documento['feature']:
        erros.append("Documento não contém uma feature")
        return erros
    
    feature = documento['feature']
    
    if not feature.get('name') or not feature['name'].strip():
        erros.append("Feature não possui nome")
    
    if 'children' not in feature or not feature['children']:
        erros.append("Feature não contém cenários")
        return erros
    
    for child in feature['children']:
        if 'scenario' in child:
            cenario = child['scenario']
            
            if not cenario.get('name') or not cenario['name'].strip():
                erros.append(f"Cenário sem nome na linha {cenario.get('location', {}).get('line', '?')}")
            
            if 'steps' not in cenario or not cenario['steps']:
                erros.append(f"Cenário '{cenario.get('name', 'sem nome')}' não possui steps")
            else:
                for step in cenario['steps']:
                    if not step.get('text') or not step['text'].strip():
                        erros.append(f"Step vazio no cenário '{cenario.get('name', 'sem nome')}'")
    
    return erros

def encontrar_arquivos_feature(diretorio_base):

    arquivos_feature = []
    
    for raiz, _, arquivos in os.walk(diretorio_base):
        for arquivo in arquivos:
            if arquivo.endswith('.feature'):
                caminho_completo = os.path.join(raiz, arquivo)
                caminho_relativo = os.path.relpath(caminho_completo, diretorio_base)
                arquivos_feature.append((caminho_completo, caminho_relativo))
    
    return arquivos_feature

def gerar_relatorio(resultados, diretorio_saida):
    
    os.makedirs(diretorio_saida, exist_ok=True)
    
    caminho_relatorio = os.path.join(diretorio_saida, f"relatorio_gherkin_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(caminho_relatorio, 'w', encoding='utf-8') as relatorio:
        relatorio.write("RELATÓRIO DE ANÁLISE GHERKIN\n")
        relatorio.write("=" * 60 + "\n")
        relatorio.write(f"Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        relatorio.write(f"Diretório analisado: {DIRETORIO_CENARIOS}\n\n")
        
        total_arquivos = len(resultados)
        arquivos_validos = sum(1 for r in resultados if r['valido'])
        arquivos_invalidos = total_arquivos - arquivos_validos
        arquivos_corrigidos = sum(1 for r in resultados if r.get('correcao_aplicada', False))
        
        relatorio.write("ESTATÍSTICAS GERAIS:\n")
        relatorio.write(f"Total de arquivos analisados: {total_arquivos}\n")
        relatorio.write(f"Arquivos válidos: {arquivos_validos}\n")
        relatorio.write(f"Arquivos com problemas: {arquivos_invalidos}\n")
        relatorio.write(f"Arquivos corrigidos automaticamente: {arquivos_corrigidos}\n\n")
        
        relatorio.write("DETALHAMENTO POR ARQUIVO:\n")
        relatorio.write("=" * 60 + "\n")
        
        for resultado in resultados:
            relatorio.write(f"\nArquivo: {resultado['caminho_relativo']}\n")
            
            if resultado.get('correcao_aplicada'):
                relatorio.write("⚠  CORRIGIDO AUTOMATICAMENTE (faltava Feature)\n")
            
            relatorio.write(f"Status: {'VÁLIDO' if resultado['valido'] else 'INVÁLIDO'}\n")
            
            if not resultado['valido']:
                relatorio.write("Erros encontrados:\n")
                for i, erro in enumerate(resultado['erros'], 1):
                    relatorio.write(f"  {i}. {erro}\n")
            
            relatorio.write("-" * 60 + "\n")
        
        relatorio.write("\nRECOMENDAÇÕES:\n")
        relatorio.write("=" * 60 + "\n")
        
        if arquivos_corrigidos > 0:
            relatorio.write(f"\n{arquivos_corrigidos} arquivo(s) foram corrigidos automaticamente por falta de 'Feature:'.\n")
            relatorio.write("Para corrigir permanentemente, adicione no início de cada arquivo:\n")
            relatorio.write("Feature: Nome da Funcionalidade\n")
            relatorio.write("  [Descrição opcional]\n\n")
        
        problemas_comuns = []
        for resultado in resultados:
            if not resultado['valido']:
                for erro in resultado['erros']:
                    if "expected: #FeatureLine" in erro:
                        problemas_comuns.append("Falta declaração 'Feature:' no início do arquivo")
                        break
        
        if problemas_comuns:
            relatorio.write("Problemas mais frequentes:\n")
            for problema in set(problemas_comuns):
                relatorio.write(f"- {problema}\n")
    
    return caminho_relatorio

def gerar_relatorios_individuais(resultados, diretorio_saida):
    
    for resultado in resultados:
       
        caminho_relativo = resultado['caminho_relativo']
        
        nome_relatorio = os.path.splitext(caminho_relativo)[0] + ".txt"
        caminho_relatorio = os.path.join(diretorio_saida, nome_relatorio)
        
        os.makedirs(os.path.dirname(caminho_relatorio), exist_ok=True)
        
        with open(caminho_relatorio, 'w', encoding='utf-8') as relatorio:
            relatorio.write("RELATÓRIO INDIVIDUAL DE ANÁLISE GHERKIN\n")
            relatorio.write("=" * 50 + "\n")
            relatorio.write(f"Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            relatorio.write(f"Arquivo analisado: {os.path.basename(resultado['arquivo'])}\n")
            relatorio.write(f"Caminho relativo: {caminho_relativo}\n")
            relatorio.write(f"Caminho completo: {resultado['arquivo']}\n\n")
            
            if resultado.get('correcao_aplicada'):
                relatorio.write("CORRIGIDO AUTOMATICAMENTE (faltava declaração Feature)\n\n")
            
            relatorio.write(f"Status: {'VÁLIDO' if resultado['valido'] else 'INVÁLIDO'}\n")
            
            if not resultado['valido']:
                relatorio.write("\nERROS ENCONTRADOS:\n")
                relatorio.write("-" * 30 + "\n")
                for i, erro in enumerate(resultado['erros'], 1):
                    relatorio.write(f"{i}. {erro}\n")
            else:
                relatorio.write("\nO arquivo está sintaticamente correto!\n")
                
            if resultado['valido'] and resultado['documento']:
                feature = resultado['documento']['feature']
                relatorio.write("\nINFORMAÇÕES DA FEATURE:\n")
                relatorio.write("-" * 30 + "\n")
                relatorio.write(f"Nome: {feature.get('name', 'Não especificado')}\n")
                relatorio.write(f"Descrição: {feature.get('description', 'Não possui').strip() or 'Não possui'}\n")
                
                if 'children' in feature:
                    cenarios = [c for c in feature['children'] if 'scenario' in c]
                    relatorio.write(f"Total de cenários: {len(cenarios)}\n")
                    
                    relatorio.write("\nCENÁRIOS IDENTIFICADOS:\n")
                    for i, child in enumerate(feature['children'], 1):
                        if 'scenario' in child:
                            cenario = child['scenario']
                            relatorio.write(f"{i}. {cenario.get('name', 'Sem nome')}\n")
                            
                            if 'steps' in cenario:
                                relatorio.write(f"   Steps: {len(cenario['steps'])}\n")
                                for step in cenario['steps']:
                                    relatorio.write(f"   - {step.get('keyword', '').strip()} {step.get('text', '').strip()}\n")
    
    return diretorio_saida

def gerar_relatorio_consolidado(resultados, diretorio_saida):
   
    caminho_relatorio = os.path.join(diretorio_saida, f"RELATORIO_CONSOLIDADO_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(caminho_relatorio, 'w', encoding='utf-8') as relatorio:
        relatorio.write("RELATÓRIO CONSOLIDADO - ANÁLISE GHERKIN\n")
        relatorio.write("=" * 60 + "\n")
        relatorio.write(f"Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        relatorio.write(f"Total de arquivos processados: {len(resultados)}\n\n")
        
        arquivos_validos = sum(1 for r in resultados if r['valido'])
        arquivos_corrigidos = sum(1 for r in resultados if r.get('correcao_aplicada', False))
        
        relatorio.write("ESTATÍSTICAS:\n")
        relatorio.write(f"Arquivos válidos: {arquivos_validos}\n")
        relatorio.write(f"Arquivos inválidos: {len(resultados) - arquivos_validos}\n")
        relatorio.write(f"Arquivos corrigidos: {arquivos_corrigidos}\n\n")
        
        relatorio.write("ARQUIVOS PROCESSADOS:\n")
        relatorio.write("-" * 40 + "\n")
        for resultado in resultados:
            status = "VÁLIDO" if resultado['valido'] else "INVÁLIDO"
            correcao = " (CORRIGIDO)" if resultado.get('correcao_aplicada') else ""
            relatorio.write(f"{resultado['caminho_relativo']}: {status}{correcao}\n")

def main():
    print("=== ANALISADOR SINTÁTICO GHERKIN ===\n")
    print(f"Diretório de cenários: {DIRETORIO_CENARIOS}")
    print(f"Diretório de relatórios: {DIRETORIO_RELATORIOS}")
    
    if not os.path.exists(DIRETORIO_CENARIOS):
        print(f"\nErro: Diretório '{DIRETORIO_CENARIOS}' não encontrado.")
        print("Criando diretório...")
        os.makedirs(DIRETORIO_CENARIOS, exist_ok=True)
        print(f"Diretório '{DIRETORIO_CENARIOS}' criado. Adicione os arquivos .feature com cenários Gherkin.")
        return

    arquivos_feature = encontrar_arquivos_feature(DIRETORIO_CENARIOS)
    
    if not arquivos_feature:
        print(f"\nNenhum arquivo .feature encontrado no diretório '{DIRETORIO_CENARIOS}'.")
        return
    
    print(f"\nAnalisando {len(arquivos_feature)} arquivos...")
    resultados = []
    
    for caminho_completo, caminho_relativo in arquivos_feature:
        print(f"Processando: {caminho_relativo}")
        resultado = analisar_arquivo_gherkin(caminho_completo)
        resultado['caminho_relativo'] = caminho_relativo
        resultados.append(resultado)
        
        if resultado['valido']:
            if resultado.get('correcao_aplicada'):
                print(f"{caminho_relativo} - CORRIGIDO (agora válido)")
            else:
                print(f"{caminho_relativo} - VÁLIDO")
        else:
            print(f"{caminho_relativo} - INVÁLIDO")
            for erro in resultado['erros']:
                print(f"{erro}")
    
    caminho_relatorio = gerar_relatorio(resultados, DIRETORIO_RELATORIOS)
    
    diretorio_relatorios = gerar_relatorios_individuais(resultados, DIRETORIO_RELATORIOS)
    
    gerar_relatorio_consolidado(resultados, DIRETORIO_RELATORIOS)
    
    arquivos_validos = sum(1 for r in resultados if r['valido'])
    arquivos_corrigidos = sum(1 for r in resultados if r.get('correcao_aplicada', False))
    
    print(f"\n=== ANÁLISE CONCLUÍDA ===")
    print(f"Total de arquivos: {len(resultados)}")
    print(f"Arquivos válidos: {arquivos_validos}")
    print(f"Arquivos corrigidos: {arquivos_corrigidos}")
    print(f"Relatório consolidado salvo em: {caminho_relatorio}")
    print(f"Relatórios individuais salvos em: {diretorio_relatorios}")
    print(f"Cada arquivo possui seu relatório individual mantendo a estrutura de subdiretórios")

if __name__ == "__main__":
    main()