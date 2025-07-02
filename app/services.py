"""
Criar o "Parser" com LangChain: Em app/services.py, 
vamos usar LangChain para orquestrar a chamada à OpenAI e 
forçar a saída no formato do nosso modelo Pydantic.
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from .models import PerfilCandidato # Importa o modelo Pydantic

def extrair_info_curriculo(texto_curriculo: str) -> PerfilCandidato:
    # 1. Inicializa o modelo da OpenAI
    model = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    # 2. Cria o parser com o nosso modelo Pydantic
    parser = PydanticOutputParser(pydantic_object=PerfilCandidato)

    # 3. Cria o template do prompt, incluindo as instruções de formatação
    prompt_template = """
    Você é um especialista em recrutamento e análise de currículos.
    Sua tarefa é extrair as informações do texto do currículo abaixo e estruturá-las em formato JSON.

    {format_instructions}

    Texto do Currículo:
    ---
    {texto_curriculo}
    ---
    """
    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # 4. Cria a "chain" que conecta o prompt, o modelo e o parser
    chain = prompt | model | parser

    # 5. Invoca a chain com o texto do currículo
    perfil = chain.invoke({"texto_curriculo": texto_curriculo})
    return perfil


"""
Caso de Uso 2 - Análise de Compatibilidade
Com o perfil estruturado em mãos, vamos compará-lo com a vaga.
"""

from .models import AnaliseCompatibilidade, PerfilCandidato

def analisar_compatibilidade_vaga(perfil: PerfilCandidato, contexto_vaga: str) -> AnaliseCompatibilidade:
    model = ChatOpenAI(model="gpt-4-turbo", temperature=0)
    parser = PydanticOutputParser(pydantic_object=AnaliseCompatibilidade)

    prompt_template = """
    Você é um recrutador sênior e sua tarefa é analisar a compatibilidade de um candidato para uma vaga.
    Analise o perfil do candidato (em JSON) e a descrição da vaga (texto).
    Para o score_geral, considere:
    - 0-3: Incompatível
    - 4-6: Parcialmente compatível, com gaps significativos.
    - 7-8: Bom candidato, atende a maioria dos requisitos.
    - 9-10: Candidato ideal, forte aderência à vaga.

    {format_instructions}

    Descrição da Vaga:
    ---
    {contexto_vaga}
    ---
    Perfil do Candidato (JSON):
    ---
    {perfil_json}
    ---
    """
    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    chain = prompt | model | parser
    analise = chain.invoke({
        "contexto_vaga": contexto_vaga,
        "perfil_json": perfil.model_dump_json() # Converte o objeto Pydantic para uma string JSON
    })
    return analise


"""
Extra - Perguntas Inteligentes
Vamos adicionar a lógica para identificar informações faltantes e sugerir perguntas.
"""

#def gerar_perguntas_esclarecimento() -> PerguntasEntrevista:
    # A lógica será muito similar às funções anteriores, mas com um prompt focado em identificar GAPS.
    # Prompt: "Baseado no perfil e na vaga, identifique informações cruciais que estão faltando
    # no currículo. Formule perguntas diretas para o candidato para obter essas informações."
    # ...