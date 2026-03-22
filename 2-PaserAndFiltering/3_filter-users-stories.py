import os 
import shutil
from pathlib import Path
from dotenv import load_dotenv

def extrair_conteudo_arquivo(caminho_arquivo):
   
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        historia = []
        cenarios = []
        cenario_atual = []
        dentro_description = False
        dentro_cenario = False
        description_encontrado = False
        
        for linha in linhas:
            linha_limpa = linha.strip()
            
            if linha_limpa.startswith('Description:'):
                dentro_description = True
                description_encontrado = True
                resto_linha = linha_limpa[len('Description:'):].strip()
                if resto_linha:
                    historia.append(resto_linha + ' ')
                continue
            
            elif dentro_description and (
                linha_limpa.startswith('Background:') or 
                linha_limpa.startswith('Scenario') or
                linha_limpa.startswith('Tags:')
            ):
                dentro_description = False
            
            elif dentro_description:
                if linha_limpa:  
                    historia.append(linha_limpa + ' ')
            
            if linha_limpa.startswith('Scenario'):
                if cenario_atual:  
                    cenarios.append(''.join(cenario_atual))
                
                cenario_atual = [linha]
                dentro_cenario = True
                
            elif dentro_cenario:
                cenario_atual.append(linha)
        
        if cenario_atual:
            cenarios.append(''.join(cenario_atual))
        
        conteudo_historia = ''.join(historia).strip() if historia and description_encontrado else ""
        
        return conteudo_historia, cenarios
        
    except Exception as e:
        print(f"Erro ao ler {caminho_arquivo}: {e}")
        return "", []


def salvar_conteudo_separado(conteudo_historia, cenarios, caminho_base, diretorio_destino_historias, diretorio_destino_cenarios, diretorio_destino_consolidado):
  
    arquivos_salvos = []
    
    Path(diretorio_destino_historias).mkdir(parents=True, exist_ok=True)
    Path(diretorio_destino_cenarios).mkdir(parents=True, exist_ok=True)
    Path(diretorio_destino_consolidado).mkdir(parents=True, exist_ok=True)  
    
    if conteudo_historia:
        nome_arquivo_historia = f"{Path(caminho_base).stem}_story.txt"
        caminho_historia = os.path.join(diretorio_destino_historias, nome_arquivo_historia)
        
        with open(caminho_historia, 'w', encoding='utf-8') as f:
            f.write(conteudo_historia)
        arquivos_salvos.append(('historia', caminho_historia))
    
    if cenarios and any(c.strip() for c in cenarios):
    
        for i, cenario in enumerate(cenarios, 1):
            if cenario.strip(): 
                nome_arquivo_cenario = f"{Path(caminho_base).stem}_scenario_{i}.txt"
                caminho_cenario = os.path.join(diretorio_destino_cenarios, nome_arquivo_cenario)
                
                with open(caminho_cenario, 'w', encoding='utf-8') as f:
                    f.write(cenario)
                arquivos_salvos.append(('cenario', caminho_cenario))
        
        nome_arquivo_consolidado = f"{Path(caminho_base).stem}_story_processado.txt"
        caminho_consolidado = os.path.join(diretorio_destino_consolidado, nome_arquivo_consolidado)
        
        with open(caminho_consolidado, 'w', encoding='utf-8') as f:
           
            f.write("\n\n".join(cenarios))
        arquivos_salvos.append(('consolidado', caminho_consolidado))
    
    return arquivos_salvos

def processar_diretorios(diretorio_origem, diretorio_destino_historias, diretorio_destino_cenarios, diretorio_destino_consolidado):
   
    relatorio = {
        'total_arquivos_processados': 0,
        'total_historias_extraidas': 0,
        'total_cenarios_extraidos': 0,
        'total_arquivos_consolidados': 0,  
        'arquivos_sem_conteudo': 0,
        'arquivos_sem_description': 0,
        'historias_por_diretorio': {},
        'cenarios_por_diretorio': {},
        'arquivos_salvos': [],
        'todos_diretorios': set(),
        'erros': [],
        'diretorios_filtrados': 0
    }
    
    estatisticas_diretorios = {}
    
    for root, dirs, files in os.walk(diretorio_origem):
        rel_path = os.path.relpath(root, diretorio_origem)
        dir_nome = os.path.basename(root) if rel_path != '.' else 'root'
        
        if dir_nome not in estatisticas_diretorios:
            estatisticas_diretorios[dir_nome] = {
                'historias': 0,
                'cenarios': 0,
                'caminho': root,
                'rel_path': rel_path
            }
            
        for file in files:
            if file.lower().endswith('.txt'):
                caminho_arquivo = os.path.join(root, file)
                
                try:
                    conteudo_historia, cenarios = extrair_conteudo_arquivo(caminho_arquivo)
                    
                    if conteudo_historia.strip():
                        estatisticas_diretorios[dir_nome]['historias'] += 1
                    if cenarios and any(c.strip() for c in cenarios):
                        estatisticas_diretorios[dir_nome]['cenarios'] += len(cenarios)
                        
                except Exception as e:
                    print(f"  ✗ Erro ao coletar estatísticas de {caminho_arquivo}: {e}")
    
    for root, dirs, files in os.walk(diretorio_origem):
        rel_path = os.path.relpath(root, diretorio_origem)
        dir_nome = os.path.basename(root) if rel_path != '.' else 'root'
        
        stats = estatisticas_diretorios.get(dir_nome, {'historias': 0, 'cenarios': 0})
        if stats['historias'] < 10 or stats['cenarios'] < 10:
            relatorio['diretorios_filtrados'] += 1
            print(f"  ⚠️  Diretório ignorado (menos de 10 histórias ou cenários): {dir_nome} [Histórias: {stats['historias']}, Cenários: {stats['cenarios']}]")
            continue
        
        relatorio['todos_diretorios'].add(dir_nome)
        
        if dir_nome not in relatorio['historias_por_diretorio']:
            relatorio['historias_por_diretorio'][dir_nome] = 0
        if dir_nome not in relatorio['cenarios_por_diretorio']:
            relatorio['cenarios_por_diretorio'][dir_nome] = 0

        repo_info_source = os.path.join(root, 'repository_info.json')
        if os.path.exists(repo_info_source):
           
            dest_hist_dir = os.path.join(diretorio_destino_historias, rel_path)
            Path(dest_hist_dir).mkdir(parents=True, exist_ok=True)
            shutil.copy2(repo_info_source, dest_hist_dir)
            print(f"  📄 Copiado repository_info.json para {dest_hist_dir}")
            
            dest_cen_dir = os.path.join(diretorio_destino_cenarios, rel_path)
            Path(dest_cen_dir).mkdir(parents=True, exist_ok=True)
            shutil.copy2(repo_info_source, dest_cen_dir)
            print(f"  📄 Copiado repository_info.json para {dest_cen_dir}")
            
            dest_cons_dir = os.path.join(diretorio_destino_consolidado, rel_path)
            Path(dest_cons_dir).mkdir(parents=True, exist_ok=True)
            shutil.copy2(repo_info_source, dest_cons_dir)
            print(f"  📄 Copiado repository_info.json para {dest_cons_dir}")
            
        for file in files:
            if file.lower().endswith('.txt'):
                caminho_arquivo = os.path.join(root, file)
                relatorio['total_arquivos_processados'] += 1
                
                try:
                    
                    conteudo_historia, cenarios = extrair_conteudo_arquivo(caminho_arquivo)
                    
                    tem_historia = bool(conteudo_historia.strip())
                    tem_cenarios = len(cenarios) > 0 and any(c.strip() for c in cenarios)
                    
                    if not tem_historia:
                        relatorio['arquivos_sem_description'] += 1
                    
                    if not tem_historia and not tem_cenarios:
                        relatorio['arquivos_sem_conteudo'] += 1
                        print(f"  ⚠️  Arquivo sem conteúdo válido: {file}")
                        continue
                    
                    dest_hist_dir = os.path.join(diretorio_destino_historias, rel_path)
                    dest_cen_dir = os.path.join(diretorio_destino_cenarios, rel_path)
                    dest_cons_dir = os.path.join(diretorio_destino_consolidado, rel_path) 
                    
                    arquivos_salvos = salvar_conteudo_separado(
                        conteudo_historia, cenarios, file, dest_hist_dir, dest_cen_dir, dest_cons_dir  
                    )
                    
                    if tem_historia:
                        relatorio['historias_por_diretorio'][dir_nome] += 1
                        relatorio['total_historias_extraidas'] += 1
                    
                    if tem_cenarios:
                        relatorio['cenarios_por_diretorio'][dir_nome] += len(cenarios)
                        relatorio['total_cenarios_extraidos'] += len(cenarios)
                        
                        relatorio['total_arquivos_consolidados'] += 1
                    
                    relatorio['arquivos_salvos'].extend(arquivos_salvos)
                    
                    status_historia = "com história" if tem_historia else "sem história"
                    tem_consolidado = " + consolidado" if tem_cenarios else ""
                    print(f"  ✓ Processado: {file} [{status_historia}] -> {len(cenarios)} cenário(s){tem_consolidado}")
                    
                except Exception as e:
                    erro_msg = f"Erro ao processar {caminho_arquivo}: {e}"
                    relatorio['erros'].append(erro_msg)
                    print(f"  ✗ {erro_msg}")
    
    return relatorio

def gerar_relatorio(relatorio, arquivo_relatorio=None):
   
    print("=" * 60)
    print("RELATÓRIO DE EXTRAÇÃO DE HISTÓRIAS E CENÁRIOS")
    print("=" * 60)
    
    print(f"\nTOTAIS GERAIS:")
    print(f"  - Arquivos TXT processados: {relatorio['total_arquivos_processados']}")
    print(f"  - Histórias de usuário extraídas: {relatorio['total_historias_extraidas']}")
    print(f"  - Cenários extraídos: {relatorio['total_cenarios_extraidos']}")
    print(f"  - Arquivos sem Description: {relatorio['arquivos_sem_description']}")
    print(f"  - Arquivos sem conteúdo válido: {relatorio['arquivos_sem_conteudo']}")
    print(f"  - Diretórios filtrados (menos de 10 histórias/cenários): {relatorio['diretorios_filtrados']}")
    print(f"  - Erros encontrados: {len(relatorio['erros'])}")
    
    print("\nESTATÍSTICAS POR DIRETÓRIO:")
    diretorios_ordenados = sorted(relatorio['todos_diretorios'])
    
    for i, dir_nome in enumerate(diretorios_ordenados, 1):
        historias = relatorio['historias_por_diretorio'].get(dir_nome, 0)
        cenarios = relatorio['cenarios_por_diretorio'].get(dir_nome, 0)
        print(f"  {i}. {dir_nome}:")
        print(f"     - Histórias de usuário: {historias}")
        print(f"     - Cenários: {cenarios}")

    diretorios_com_historias = len([d for d, count in relatorio['historias_por_diretorio'].items() if count > 0])
    diretorios_com_cenarios = len([d for d, count in relatorio['cenarios_por_diretorio'].items() if count > 0])
    
    print(f"\nRESUMO:")
    print(f"  - Total de diretórios processados: {len(relatorio['todos_diretorios'])}")
    print(f"  - Diretórios com histórias de usuário: {diretorios_com_historias}")
    print(f"  - Diretórios com cenários: {diretorios_com_cenarios}")
    print(f"  - Arquivos salvos no total: {len(relatorio['arquivos_salvos'])}")
    
    if relatorio['erros']:
        print(f"\nERROS ENCONTRADOS:")
        for erro in relatorio['erros']:
            print(f"  ✗ {erro}")
    
    if arquivo_relatorio:
        with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE EXTRAÇÃO DE HISTÓRIAS E CENÁRIOS\n")
            f.write("=" * 60 + "\n")
            f.write(f"\nTOTAIS GERAIS:\n")
            f.write(f"  - Arquivos TXT processados: {relatorio['total_arquivos_processados']}\n")
            f.write(f"  - Histórias de usuário extraídas: {relatorio['total_historias_extraidas']}\n")
            f.write(f"  - Cenários extraídos: {relatorio['total_cenarios_extraidos']}\n")
            f.write(f"  - Arquivos sem Description: {relatorio['arquivos_sem_description']}\n")
            f.write(f"  - Arquivos sem conteúdo válido: {relatorio['arquivos_sem_conteudo']}\n")
            f.write(f"  - Diretórios filtrados (menos de 10 histórias/cenários): {relatorio['diretorios_filtrados']}\n")
            f.write(f"  - Erros encontrados: {len(relatorio['erros'])}\n\n")
            
            f.write("ESTATÍSTICAS POR DIRETÓRIO:\n")
            for i, dir_nome in enumerate(diretorios_ordenados, 1):
                historias = relatorio['historias_por_diretorio'].get(dir_nome, 0)
                cenarios = relatorio['cenarios_por_diretorio'].get(dir_nome, 0)
                f.write(f"  {i}. {dir_nome}:\n")
                f.write(f"     - Histórias de usuário: {historias}\n")
                f.write(f"     - Cenários: {cenarios}\n")
            
            f.write(f"\nRESUMO:\n")
            f.write(f"  - Total de diretórios processados: {len(relatorio['todos_diretorios'])}\n")
            f.write(f"  - Diretórios com histórias de usuário: {diretorios_com_historias}\n")
            f.write(f"  - Diretórios com cenários: {diretorios_com_cenarios}\n")
            
            if relatorio['erros']:
                f.write(f"\nERROS ENCONTRADOS:\n")
                for erro in relatorio['erros']:
                    f.write(f"  - {erro}\n")

def main():

    load_dotenv()

    GHERKIN_OFFICIAL_OUTPUT = os.getenv("GHERKIN_OFFICIAL_OUTPUT")

    DIRETORIO_ORIGEM = os.getenv("GHERKIN_OFFICIAL_OUTPUT") 
    DIRETORIO_DESTINO_HISTORIAS = os.getenv("DIRETORIO_DESTINO_HISTORIAS")        
    DIRETORIO_DESTINO_CENARIOS = os.getenv("DIRETORIO_DESTINO_CENARIOS")
    ARQUIVO_RELATORIO = os.getenv("PASER_AND_FILTERING_SUMMARY")  
    DIRETORIO_DESTINO_CONSOLIDADOS = os.getenv("DIRETORIO_DESTINO_CONSOLIDADOS")              

    if not os.path.exists(DIRETORIO_ORIGEM):
        print(f"Erro: Diretório '{DIRETORIO_ORIGEM}' não encontrado!")
        return
    
    print(f"Processando diretório: {DIRETORIO_ORIGEM}")
    print(f"Destino histórias: {DIRETORIO_DESTINO_HISTORIAS}")
    print(f"Destino cenários: {DIRETORIO_DESTINO_CENARIOS}")
    print(f"Destino consolidados: {DIRETORIO_DESTINO_CONSOLIDADOS}")
    print(f"Critério: Diretórios com pelo menos 10 histórias E 10 cenários")
    if ARQUIVO_RELATORIO:
        print(f"Relatório: {ARQUIVO_RELATORIO}")
    print("-" * 60)

    relatorio = processar_diretorios(
        DIRETORIO_ORIGEM, 
        DIRETORIO_DESTINO_HISTORIAS, 
        DIRETORIO_DESTINO_CENARIOS,
        DIRETORIO_DESTINO_CONSOLIDADOS
    )
    
    gerar_relatorio(relatorio, ARQUIVO_RELATORIO)
    
    print(f"\nProcessamento concluído!")
    print(f"Histórias salvas em: {DIRETORIO_DESTINO_HISTORIAS}")
    print(f"Cenários salvos em: {DIRETORIO_DESTINO_CENARIOS}")
    print(f"Cenários consolidados salvos em: {DIRETORIO_DESTINO_CONSOLIDADOS}")

if __name__ == "__main__":
    main()