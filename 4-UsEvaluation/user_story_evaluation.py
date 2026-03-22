import os
import subprocess
import csv
import glob
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

INPUT_DIR = "TESTES/user_stories1"


OUTPUT_DIR = "TESTES/US_evaluation"

AQUSA_CORE_SCRIPT = os.getenv("AQUSA_CORE_SCRIPT") 


CSV_REPORT = "TESTES/US_evaluation/user_stories_errors_report.csv"

def run_aqusa_analysis():
    
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    csv_data = []
    
    txt_files = glob.glob(os.path.join(INPUT_DIR, "**", "*.txt"), recursive=True)
    
    print(f"Encontrados {len(txt_files)} arquivos para processar...")
    
    for i, input_file in enumerate(txt_files, 1):
        print(f"Processando arquivo {i}/{len(txt_files)}: {input_file}")
        
        try:
           
            relative_path = os.path.relpath(input_file, INPUT_DIR)
            output_file_base = os.path.join(OUTPUT_DIR, os.path.splitext(relative_path)[0])
            
            Path(os.path.dirname(output_file_base)).mkdir(parents=True, exist_ok=True)
            
            command = [
                "py", 
                AQUSA_CORE_SCRIPT,
                "-i", input_file,
                "-o", output_file_base,
                "-f", "txt"
            ]
            
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            
            print(f"Análise concluída: {output_file_base}")
            
            defect_types, messages = extract_errors_from_output(output_file_base + ".txt")

            tipos_erro_formatados = []
            mensagens_formatadas = []

            for i, (defect_type, message) in enumerate(zip(defect_types, messages), 1):
                tipos_erro_formatados.append(f"{i} - {defect_type}")
                mensagens_formatadas.append(f"{i} - {message}")

            csv_data.append({
                "arquivo": relative_path,
                "total_erros": len(defect_types),
                "tipos_erro": "; ".join(tipos_erro_formatados) if tipos_erro_formatados else "Nenhum erro encontrado",
                "mensagens": "; ".join(mensagens_formatadas) if mensagens_formatadas else "Nenhuma mensagem"
            })
            
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Erro ao processar {input_file}: {e}")
            csv_data.append({
                "arquivo": relative_path,
                "total_erros": -1,
                "tipos_erro": f"ERRO NA EXECUÇÃO: {e.stderr if e.stderr else str(e)}",
                "mensagens": ""
            })
        except Exception as e:
            print(f"  ✗ Erro inesperado ao processar {input_file}: {e}")
            csv_data.append({
                "arquivo": relative_path,
                "total_erros": -1,
                "tipos_erro": f"ERRO INESPERADO: {str(e)}",
                "mensagens": ""
            })
    
    generate_csv_report(csv_data)
    print(f"\nRelatório CSV gerado: {CSV_REPORT}")


def extract_errors_from_output(output_file):
   
    defect_types = []
    messages = []
    
    try:
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                if line.startswith('Defect type:'):
                    defect_type = line.replace('Defect type:', '').strip()
                    
                    if i + 1 < len(lines):
                        message_line = lines[i + 1].strip()
                        if message_line.startswith('Message:'):
                            message = message_line.replace('Message:', '').strip()
                            
                            defect_types.append(defect_type)
                            messages.append(message)
                            
                            i += 1 
                
                i += 1
                
    except Exception as e:
        defect_types = [f"Erro ao ler arquivo: {str(e)}"]
        messages = [""]
    
    return defect_types, messages


def generate_csv_report(data):
   
    try:
        with open(CSV_REPORT, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['arquivo', 'total_erros', 'tipos_erro', 'mensagens']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in data:
                writer.writerow(row)
                
        print(f"Relatório CSV gerado com {len(data)} entradas")
    except Exception as e:
        print(f"Erro ao gerar CSV: {e}")

        
if __name__ == "__main__":
    print("Iniciando análise de histórias de usuário com aqusa-core...")
    print(f"Diretório de entrada: {INPUT_DIR}")
    print(f"Diretório de saída: {OUTPUT_DIR}")
    print(f"Script aqusa-core: {AQUSA_CORE_SCRIPT}")
    print("-" * 50)
    
    run_aqusa_analysis()
    
    print("\nProcessamento concluído!")