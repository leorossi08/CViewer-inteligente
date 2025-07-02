import fitz  # A biblioteca PyMuPDF
from fastapi import UploadFile
import io

async def extrair_texto_de_pdf(arquivo: UploadFile) -> str:
    """
    Lê o conteúdo de um UploadFile (PDF), extrai o texto de todas as páginas
    e retorna uma única string com o texto completo.

    Args:
        arquivo: O objeto UploadFile vindo do endpoint FastAPI.

    Returns:
        Uma string contendo todo o texto extraído do PDF.
    """
    # UploadFile.read() é uma operação assíncrona, por isso usamos 'await'.
    # Isto lê o ficheiro em memória como bytes.
    conteudo_arquivo_bytes = await arquivo.read()

    # Abrimos o conteúdo em bytes como um ficheiro PDF usando fitz.open()
    # O stream=True e filetype="pdf" ajudam o fitz a entender os dados.
    documento = fitz.open(stream=conteudo_arquivo_bytes, filetype="pdf")
    
    texto_completo = ""
    # Iteramos por cada página do documento.
    for pagina in documento:
        # Extraímos o texto da página e adicionamos à nossa string.
        texto_completo += pagina.get_text()
    
    # É uma boa prática fechar o documento para libertar recursos.
    documento.close()
    
    return texto_completo