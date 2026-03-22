import os
import random
import shutil
import math
from datetime import datetime
from dotenv import load_dotenv

def selecionar_e_copiar_arquivos_igual(dir_entrada, dir_saida, arquivos_por_repositorio, seed=42):
   
    random.seed(seed)
    
    arquivos_por_repositorio_dict = {}
    mapa_repo_info = {}
    
    print(f"Varrendo diretório: {dir_entrada}")
    for raiz, diretorios, arquivos in os.walk(dir_entrada):
       
        arquivos_txt = [arquivo for arquivo in arquivos if arquivo.endswith('.txt')]
        
        repo_info = next((arquivo for arquivo in arquivos if arquivo == 'repository_info.json'), None)
        
        if arquivos_txt:
            caminho_relativo = os.path.relpath(raiz, dir_entrada)
            
            if repo_info:
                caminho_completo_repo_info = os.path.join(raiz, repo_info)
                mapa_repo_info[caminho_relativo] = caminho_completo_repo_info
            
            arquivos_por_repositorio_dict[caminho_relativo] = []
            for arquivo_txt in arquivos_txt:
                caminho_completo_txt = os.path.join(raiz, arquivo_txt)
                arquivos_por_repositorio_dict[caminho_relativo].append((arquivo_txt, caminho_completo_txt))
    
    total_repositorios = len(arquivos_por_repositorio_dict)
    print(f"Encontrados {total_repositorios} repositórios com arquivos .txt")
    
    if total_repositorios == 0:
        print("Nenhum repositório com arquivos .txt encontrado!")
        return
    
    diretorios_com_selecao = {}
    total_copiados = 0
    
    for repositorio, arquivos_disponiveis in arquivos_por_repositorio_dict.items():
        n_para_selecionar = min(arquivos_por_repositorio, len(arquivos_disponiveis))
        
        if n_para_selecionar > 0:

            arquivos_selecionados = random.sample(arquivos_disponiveis, n_para_selecionar)
            diretorios_com_selecao[repositorio] = arquivos_selecionados
            total_copiados += n_para_selecionar
    
    print(f"Selecionando {arquivos_por_repositorio} arquivos por repositório (ou o máximo disponível)")
    print(f"Total de arquivos selecionados: {total_copiados} com seed {seed}")
    
    os.makedirs(dir_saida, exist_ok=True)
    
    for caminho_rel, arquivos in diretorios_com_selecao.items():
        dir_destino = os.path.join(dir_saida, caminho_rel)
        
        os.makedirs(dir_destino, exist_ok=True)
        
        for nome_arquivo, caminho_origem in arquivos:
            caminho_destino = os.path.join(dir_destino, nome_arquivo)
            shutil.copy2(caminho_origem, caminho_destino)
            print(f"Copiado: {caminho_rel}/{nome_arquivo}")
        
        if caminho_rel in mapa_repo_info:
            repo_info_origem = mapa_repo_info[caminho_rel]
            repo_info_destino = os.path.join(dir_destino, 'repository_info.json')
            shutil.copy2(repo_info_origem, repo_info_destino)
            print(f"Copiado repository_info.json para: {caminho_rel}")
    
    salvar_resumo_igual(dir_saida, dir_entrada, total_copiados, len(diretorios_com_selecao), 
                       arquivos_por_repositorio, seed)
    
    estatisticas = []
    for caminho_rel, arquivos in diretorios_com_selecao.items():
        estatisticas.append(len(arquivos))
    
    print(f"Processo concluído!")
    print(f"Diretório de entrada: {dir_entrada}")
    print(f"Diretório de saída: {dir_saida}")
    print(f"Arquivos por repositório solicitados: {arquivos_por_repositorio}")
    print(f"Total de arquivos .txt copiados: {total_copiados}")
    print(f"Total de repositórios com arquivos selecionados: {len(diretorios_com_selecao)}")
    print(f"Média real de arquivos por repositório: {total_copiados/len(diretorios_com_selecao):.2f}")
    print(f"Mínimo de arquivos em um repositório: {min(estatisticas) if estatisticas else 0}")
    print(f"Máximo de arquivos em um repositório: {max(estatisticas) if estatisticas else 0}")
    print(f"Seed utilizada: {seed}")

def salvar_resumo_igual(dir_saida, dir_entrada, total_arquivos, total_repositorios, 
                       arquivos_por_repositorio, seed):
 
    resumo_path = os.path.join(dir_saida, "resumo_selecao_igual.txt")
    
    with open(resumo_path, 'w', encoding='utf-8') as f:
        f.write("RESUMO DA SELEÇÃO IGUAL POR REPOSITÓRIO\n")
        f.write("=" * 50 + "\n")
        f.write(f"Diretório de entrada: {dir_entrada}\n")
        f.write(f"Diretório de saída: {dir_saida}\n")
        f.write(f"Arquivos por repositório solicitados: {arquivos_por_repositorio}\n")
        f.write(f"Total de arquivos .txt copiados: {total_arquivos}\n")
        f.write(f"Total de repositórios com arquivos selecionados: {total_repositorios}\n")
        f.write(f"Seed utilizada: {seed}\n")
        f.write(f"Data e hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"📄 Resumo salvo em: {resumo_path}")

if __name__ == "__main__":

    load_dotenv()

    DIRETORIO_ENTRADA = os.getenv("DIRETORIO_DESTINO_HISTORIAS")
    DIRETORIO_SAIDA = os.getenv("RANDON_SELECTOR_OUTPUT")
    NUMERO_ARQUIVOS = int(os.getenv("RADON_SELECTOR_NUMBER"))  
    SEED_ALEATORIA = int(os.getenv("RADON_SELECTOR_SEED"))    

    if not os.path.exists(DIRETORIO_ENTRADA):
        print(f"❌ Erro: Diretório de entrada não encontrado: {DIRETORIO_ENTRADA}")
        print("Por favor, modifique a variável DIRETORIO_ENTRADA no código.")
    else:
        selecionar_e_copiar_arquivos_igual(
            dir_entrada=DIRETORIO_ENTRADA,
            dir_saida=DIRETORIO_SAIDA,
            arquivos_por_repositorio=NUMERO_ARQUIVOS,
            seed=SEED_ALEATORIA
        )