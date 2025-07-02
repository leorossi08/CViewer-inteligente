import requests
import os
import random

# --- Início da Seção de Caminhos Robustos ---
# Garante que o script encontre a pasta do dataset, não importa de onde ele seja executado.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATASET_PATH = os.path.join(PROJECT_ROOT, "dataset")
# --- Fim da Seção de Caminhos Robustos ---

# URL da sua API rodando localmente
API_URL = "http://localhost:8000/analisar_curriculo"

# Exemplo de contexto de vaga de TI
CONTEXTO_VAGA_TI = """
Buscamos um Engenheiro de Dados Pleno para se juntar à nossa equipe.
O candidato ideal deve ter forte conhecimento em Python, SQL e experiência com
ferramentas de ETL. É essencial ter trabalhado com PySpark em projetos anteriores.
Conhecimento em arquitetura de dados na nuvem (AWS, GCP ou Azure) e
familiaridade com arquitetura Medalhão são grandes diferenciais.
Buscamos alguém com boa capacidade de comunicação para colaborar com equipes de negócio.
"""

def testar_analise_curriculo_ti():
    """
    Testa a análise de um currículo da categoria específica "INFORMATION-TECHNOLOGY".
    """
    print("--- Iniciando teste de análise de currículo de TI ---")

    categoria_especifica = "INFORMATION-TECHNOLOGY"
    print(f"Categoria alvo: {categoria_especifica}")

    try:
        # 1. Define o caminho para a categoria específica
        caminho_categoria = os.path.join(DATASET_PATH, categoria_especifica)
        if not os.path.isdir(caminho_categoria):
            print(f"ERRO: A pasta da categoria '{categoria_especifica}' não foi encontrada em '{DATASET_PATH}'.")
            return

        # 2. Escolhe um currículo aleatório dentro da categoria de TI
        curriculos_pdf = [f for f in os.listdir(caminho_categoria) if f.lower().endswith('.pdf')]
        if not curriculos_pdf:
            print(f"ERRO: Nenhum arquivo PDF encontrado na categoria '{categoria_especifica}'.")
            return

        curriculo_aleatorio = random.choice(curriculos_pdf)
        caminho_curriculo_pdf = os.path.join(caminho_categoria, curriculo_aleatorio)
        print(f"Arquivo de currículo escolhido: {caminho_curriculo_pdf}")

        # 3. Prepara os dados para a requisição
        files = {'arquivo_pdf': (os.path.basename(caminho_curriculo_pdf), open(caminho_curriculo_pdf, 'rb'), 'application/pdf')}
        data = {'contexto_vaga': CONTEXTO_VAGA_TI}

        # 4. Chama a API
        print("Enviando requisição para a API...")
        response = requests.post(API_URL, files=files, data=data)
        response.raise_for_status()  # Lança um erro se a resposta for 4xx ou 5xx

        # 5. Imprime o resultado
        print("\n--- Resposta da API ---")
        print(f"Status Code: {response.status_code}")
        print("JSON Recebido:")
        # Usar .json() para formatar a saída de forma legível
        import json
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        print("-----------------------\n")

    except requests.exceptions.RequestException as e:
        print(f"\nERRO: Não foi possível conectar à API. Você rodou 'uvicorn app.main:app --reload'?")
        print(f"Detalhes do erro: {e}")
    except FileNotFoundError:
        print(f"\nERRO: Arquivo ou diretório não encontrado. O caminho '{caminho_categoria}' está correto?")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")


if __name__ == "__main__":
    testar_analise_curriculo_ti()