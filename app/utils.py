"""
Extrair Texto do PDF
"""

import fitz  # PyMuPDF
from fastapi import UploadFile
import io

def extrair_texto_de_pdf(arquivo: UploadFile) -> str:
    conteudo_arquivo = arquivo.file.read()
    documento = fitz.open(stream=io.BytesIO(conteudo_arquivo), filetype="pdf")
    texto_completo = ""
    for pagina in documento:
        texto_completo += pagina.get_text()
    documento.close()
    return texto_completo