# Em download_dataset.py
import kagglehub
import os
import shutil

# --- Configuração ---
# O nome da pasta final onde o dataset organizado ficará.
output_path = "dataset"

print("Iniciando o processo de download e organização do dataset...")

# --- Passo 1: Download e Cópia Inicial ---
# Baixa os dados para o cache do Kaggle.
source_dir = kagglehub.dataset_download(
    "snehaanbhawal/resume-dataset"
)

# Limpa a pasta de destino antiga, se existir, para começar do zero.
if os.path.exists(output_path):
    shutil.rmtree(output_path)

# Copia os arquivos do cache para a nossa pasta 'dataset'.
shutil.copytree(source_dir, output_path)
print(f"Dataset copiado para a pasta '{output_path}'.")


# --- Passo 2: Organização da Estrutura ---
print("Organizando a estrutura de pastas...")

# Define os caminhos de origem (onde os arquivos estão agora)
nested_data_path = os.path.join(output_path, "data", "data")
resume_folder_path = os.path.join(output_path, "Resume")

# Move as pastas de categorias (ACCOUNTANT, HR, etc.) para a raiz de 'dataset'
if os.path.exists(nested_data_path):
    for folder_name in os.listdir(nested_data_path):
        source = os.path.join(nested_data_path, folder_name)
        destination = os.path.join(output_path, folder_name)
        shutil.move(source, destination)
    
    # Remove a pasta 'data' que agora está vazia
    shutil.rmtree(os.path.join(output_path, "data"))
    print("Pastas de categoria organizadas.")

# Move o conteúdo da pasta 'Resume' (ex: Resume.csv) para a raiz de 'dataset'
if os.path.exists(resume_folder_path):
    for file_name in os.listdir(resume_folder_path):
        source = os.path.join(resume_folder_path, file_name)
        destination = os.path.join(output_path, file_name)
        shutil.move(source, destination)
        
    # Remove a pasta 'Resume' que agora está vazia
    os.rmdir(resume_folder_path)
    print("Arquivos CSV organizados.")

print(f"\nPronto! A estrutura em '{output_path}' está limpa e pronta para uso.")