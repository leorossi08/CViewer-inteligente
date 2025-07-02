from pydantic import BaseModel, Field
from typing import List, Optional

# --- Modelos para o Caso de Uso 1: Extração do Currículo ---

class Educacao(BaseModel):
    """Define a estrutura para cada item de educação no currículo."""
    instituicao: str = Field(description="Nome da instituição de ensino.")
    curso: str = Field(description="Nome do curso ou formação.")
    ano_conclusao: Optional[int] = Field(None, description="Ano de conclusão do curso.")

class Experiencia(BaseModel):
    """Define a estrutura para cada item de experiência profissional."""
    empresa: str = Field(description="Nome da empresa.")
    cargo: str = Field(description="Cargo ocupado na empresa.")
    inicio: str = Field(description="Data de início, ex: '2021-03'.")
    fim: Optional[str] = Field(None, description="Data de término, ex: '2023-01' ou 'Atual'.")
    responsabilidades: str = Field(description="Descrição das atividades e responsabilidades no cargo.")

class PerfilCandidato(BaseModel):
    """O modelo principal que estrutura todas as informações extraídas do currículo."""
    nome: str = Field(description="Nome completo do candidato.")
    email: Optional[str] = Field(None, description="Endereço de e-mail do candidato.")
    telefone: Optional[str] = Field(None, description="Número de telefone para contato.")
    resumo: str = Field(description="Um resumo de 2-3 frases sobre o perfil profissional do candidato, extraído do currículo.")
    habilidades: List[str] = Field(description="Lista de habilidades técnicas (Python, SQL, etc.) e comportamentais (Comunicação, etc.).")
    educacao: List[Educacao]
    experiencia_profissional: List[Experiencia]
    linkedin: Optional[str] = Field(None, description="URL para o perfil do LinkedIn, se encontrado.")


# --- Modelos para o Caso de Uso 2: Análise de Compatibilidade ---

class AnaliseCompatibilidade(BaseModel):
    """Define a estrutura para a análise de compatibilidade entre o candidato e a vaga."""
    score_geral: int = Field(description="Nota de 0 a 10 para a compatibilidade geral do candidato com a vaga.")
    pontos_fortes: List[str] = Field(description="Lista dos principais pontos que tornam o candidato um bom fit para a vaga.")
    pontos_a_melhorar: List[str] = Field(description="Lista de pontos onde o candidato não atende ou carece de experiência para a vaga.")
    resumo_analise: str = Field(description="Um parágrafo explicando o porquê da nota e da análise, justificando os pontos fortes e a melhorar.")


# --- Modelo para o Desafio Extra: Perguntas Inteligentes ---

class PerguntasEntrevista(BaseModel):
    """Define a estrutura para as perguntas de esclarecimento geradas pela IA."""
    informacoes_faltantes: List[str] = Field(description="Lista de perguntas para fazer ao candidato para esclarecer pontos ausentes ou duvidosos no currículo em relação à vaga.")


# --- Modelo para a Resposta Completa da API ---

class AnaliseCompleta(BaseModel):
    """
    Este é o modelo de resposta final da API, agregando todas as informações geradas.
    """
    perfil_extraido: PerfilCandidato
    analise_compatibilidade: AnaliseCompatibilidade
    perguntas_sugeridas: Optional[PerguntasEntrevista] = Field(None, description="Perguntas sugeridas para a entrevista, caso informações relevantes estejam faltando.")