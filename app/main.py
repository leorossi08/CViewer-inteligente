from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from dotenv import load_dotenv
from . import services, utils, models
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Validação para garantir que a chave da API foi configurada ao iniciar
if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("A variável de ambiente OPENAI_API_KEY não foi definida no arquivo .env")

app = FastAPI(
    title="RH Inteligente API",
    description="API para análise e triagem de currículos com IA, utilizando FastAPI e LangChain.",
    version="1.0.0"
)

@app.post(
    "/analisar_curriculo",
    response_model=models.AnaliseCompleta,
    summary="Analisar Currículo",
    tags=["Análise de Currículos"]
)
async def analisar_curriculo(
    contexto_vaga: str = Form(..., description="Texto com a descrição completa da vaga."),
    arquivo_pdf: UploadFile = File(..., description="Arquivo de currículo em formato PDF.")
):
    """
    Recebe um currículo em PDF e um contexto de vaga, e retorna uma análise completa, incluindo:
    - **Perfil Extraído**: Dados estruturados do candidato.
    - **Análise de Compatibilidade**: Pontos fortes, fracos e um score geral.
    - **Perguntas Sugeridas**: Questões para aprofundar na entrevista.
    """
    if arquivo_pdf.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="O arquivo enviado não é um PDF.")
        
    try:
        # Etapa 1: Extrair texto do PDF usando a função utilitária
        # A função é `async` e por isso usamos `await`
        texto_curriculo = await utils.extrair_texto_de_pdf(arquivo_pdf)
        if not texto_curriculo.strip():
            raise HTTPException(status_code=400, detail="O PDF parece estar vazio ou não contém texto legível.")

        # Etapa 2: Chamar o serviço para estruturar o perfil do candidato
        perfil_candidato = services.extrair_info_curriculo(texto_curriculo)

        # Etapa 3: Chamar o serviço para analisar a compatibilidade com a vaga
        analise_compatibilidade = services.analisar_compatibilidade_vaga(perfil_candidato, contexto_vaga)

        # Etapa 4: Chamar o serviço para gerar perguntas para a entrevista
        perguntas_sugeridas = services.gerar_perguntas_esclarecimento(perfil_candidato, contexto_vaga)

        # Monta a resposta final usando o modelo Pydantic `AnaliseCompleta`
        return models.AnaliseCompleta(
            perfil_extraido=perfil_candidato,
            analise_compatibilidade=analise_compatibilidade,
            perguntas_sugeridas=perguntas_sugeridas
        )

    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a análise: {e}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno ao processar o currículo.")