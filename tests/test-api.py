# test_api.py
import requests
import os
import random

# URL da sua API rodando localmente
API_URL = "http://localhost:8000/analisar_curriculo"

# Caminho para a pasta de dados do dataset (ajuste se necessário)
DATASET_PDF_PATH = os.path.join("datasets", "data", "PDF")

# Exemplo de contexto de vaga (você pode criar vários)
CONTEXTO_VAGA_TI = """
Buscamos um Analista Pleno para atuar na área de engenharia de dados.
Esperamos alguém com conhecimento em Python e SQL e boa capacidade de comunicação. Inglês é um diferencial.
É essencial ter tido experiência prévia com PySpark.
"""

def testar_analise_curriculo():
    print("--- Iniciando teste de análise de currículo ---")

    # 1. Escolher uma categoria e um currículo aleatório
    categorias = [d for d in os.listdir(DATASET_PDF_PATH) if os.path.isdir(os.path.join(DATASET_PDF_PATH, d))]
    categoria_aleatoria = random.choice(categorias)
    print(f"Categoria escolhida: {categoria_aleatoria}")

    caminho_categoria = os.path.join(DATASET_PDF_PATH, categoria_aleatoria)
    curriculo_aleatorio = random.choice(os.listdir(caminho_categoria))
    caminho_curriculo_pdf = os.path.join(caminho_categoria, curriculo_aleatorio)
    print(f"Arquivo de currículo escolhido: {caminho_curriculo_pdf}")

    # 2. Preparar os dados para a requisição
    files = {'arquivo_pdf': (os.path.basename(caminho_curriculo_pdf), open(caminho_curriculo_pdf, 'rb'), 'application/pdf')}
    data = {'contexto_vaga': CONTEXTO_VAGA_TI}

    # 3. Chamar a API
    try:
        print("Enviando requisição para a API...")
        response = requests.post(API_URL, files=files, data=data)
        response.raise_for_status()  # Lança um erro se a resposta for 4xx ou 5xx

        # 4. Imprimir o resultado
        print("\n--- Resposta da API ---")
        print(f"Status Code: {response.status_code}")
        print("JSON Recebido:")
        print(response.json())
        print("-----------------------\n")

    except requests.exceptions.RequestException as e:
        print(f"\nERRO: Não foi possível conectar à API. Você rodou 'uvicorn app.main:app --reload'?")
        print(f"Detalhes do erro: {e}")

if __name__ == "__main__":
    testar_analise_curriculo()