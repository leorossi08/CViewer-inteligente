from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from .models import PerfilCandidato, AnaliseCompatibilidade, PerguntasEntrevista

def extrair_info_curriculo(texto_curriculo: str) -> PerfilCandidato:
    """
    Usa o LangChain e a OpenAI para extrair informações estruturadas de um texto de currículo.
    """
    # 1. Inicializa o modelo da OpenAI que será usado.
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 2. Cria o parser que dirá ao LangChain como formatar a saída, usando nosso modelo Pydantic.
    parser = PydanticOutputParser(pydantic_object=PerfilCandidato)

    # 3. Cria o template do prompt com instruções claras para a IA.
    prompt_template = """
    Você é um especialista em recrutamento e análise de currículos.
    Sua tarefa é extrair as informações do texto do currículo abaixo e estruturá-las em formato JSON.
    Preste muita atenção ao formato solicitado nas instruções abaixo.

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

    # 4. Cria a "chain" que conecta o prompt, o modelo e o parser.
    chain = prompt | model | parser

    # 5. Invoca a chain com o texto do currículo e retorna o resultado já "parseado".
    perfil = chain.invoke({"texto_curriculo": texto_curriculo})
    return perfil


def analisar_compatibilidade_vaga(perfil: PerfilCandidato, contexto_vaga: str) -> AnaliseCompatibilidade:
    """
    Analisa a compatibilidade entre um perfil de candidato e uma descrição de vaga.
    """
    # CORREÇÃO: Trocado 'gpt-4-turbo' por 'gpt-3.5-turbo'.
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    parser = PydanticOutputParser(pydantic_object=AnaliseCompatibilidade)

    prompt_template = """
    Você é um recrutador sênior com vasta experiência e sua tarefa é analisar a compatibilidade de um candidato para uma vaga.
    Analise o perfil do candidato (em JSON) e a descrição da vaga (texto).
    Seja criterioso na sua análise. Para o score_geral, siga estritamente as seguintes regras:
    - 0-3: Incompatível. O candidato não possui as habilidades essenciais.
    - 4-6: Parcialmente compatível. Possui algumas habilidades, mas com gaps significativos para a vaga.
    - 7-8: Bom candidato. Atende a maioria dos requisitos importantes.
    - 9-10: Candidato ideal. Forte aderência à vaga, incluindo diferenciais.

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


def gerar_perguntas_esclarecimento(perfil: PerfilCandidato, contexto_vaga: str) -> PerguntasEntrevista:
    """
    Gera perguntas para uma entrevista com base nas informações ausentes ou que precisam de
    esclarecimento no currículo, comparando com os requisitos da vaga.
    """
    # CORREÇÃO: Trocado 'gpt-4-turbo' por 'gpt-3.5-turbo'.
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5) # Um pouco mais de criatividade aqui
    parser = PydanticOutputParser(pydantic_object=PerguntasEntrevista)

    prompt_template = """
    Você é um recrutador experiente preparando uma entrevista técnica.
    Baseado no perfil do candidato (JSON) e na descrição da vaga (texto), sua tarefa é identificar
    informações cruciais que estão faltando no currículo ou que são importantes de aprofundar.
    Formule de 2 a 4 perguntas diretas e inteligentes para o candidato para obter essas informações durante a entrevista.
    Exemplos de perguntas: "Você teve alguma experiência com a arquitetura X mencionada na vaga?" ou "Qual seu nível de proficiência em inglês para conversação?".

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
    perguntas = chain.invoke({
        "contexto_vaga": contexto_vaga,
        "perfil_json": perfil.model_dump_json()
    })
    return perguntas