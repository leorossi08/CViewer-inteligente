# download_dataset.py
import kagglehub
import os

# Define o caminho para onde o dataset será salvo
# (ex: uma pasta 'datasets' na raiz do projeto)
output_path = "datasets"
os.makedirs(output_path, exist_ok=True)

print("Baixando o dataset de currículos do Kaggle...")
# O path retornado será o caminho para o arquivo .zip
zip_path = kagglehub.dataset_download(
    "snehaanbhawal/resume-dataset",
    path=output_path
)

print(f"Dataset baixado e salvo em: {zip_path}")
print("Por favor, descompacte o arquivo .zip manualmente nesta pasta.")