"""
Caso de Uso 1 - Extração Estruturada do Currículo
Vamos implementar a primeira funcionalidade principal: ler o PDF e transformá-lo em um JSON estruturado.

"""

from pydantic import BaseModel, Field
from typing import List, Optional

class Educacao(BaseModel):
    instituicao: str = Field(description="Nome da instituição de ensino.")
    curso: str = Field(description="Nome do curso ou formação.")
    ano_conclusao: Optional[int] = Field(description="Ano de conclusão do curso.")

class Experiencia(BaseModel):
    empresa: str
    cargo: str
    inicio: str
    fim: Optional[str]
    responsabilidades: str = Field(description="Descrição das atividades e responsabilidades.")

class PerfilCandidato(BaseModel):
    nome: str = Field(description="Nome completo do candidato.")
    email: Optional[str] = Field(description="Endereço de e-mail do candidato.")
    telefone: Optional[str]
    resumo: str = Field(description="Um resumo de 2-3 frases sobre o perfil profissional do candidato.")
    habilidades: List[str] = Field(description="Lista de habilidades técnicas e comportamentais.")
    educacao: List[Educacao]
    experiencia_profissional: List[Experiencia]
    linkedin: Optional[str] = Field(description="URL para o perfil do LinkedIn.")


"""
Caso de Uso 2 - Análise de Compatibilidade
Com o perfil estruturado em mãos, vamos compará-lo com a vaga.
"""

class AnaliseCompatibilidade(BaseModel):
    score_geral: int = Field(description="Nota de 0 a 10 para a compatibilidade geral do candidato com a vaga.")
    pontos_fortes: List[str] = Field(description="Lista dos principais pontos que tornam o candidato um bom fit.")
    pontos_a_melhorar: List[str] = Field(description="Lista de pontos onde o candidato não atende ou carece de experiência para a vaga.")
    resumo_analise: str = Field(description="Um parágrafo explicando o porquê da nota e da análise.")


"""
Extra - Perguntas Inteligentes
Vamos adicionar a lógica para identificar informações faltantes e sugerir perguntas.
"""

class PerguntasEntrevista(BaseModel):
    informacoes_faltantes: List[str] = Field(description="Lista de perguntas para fazer ao candidato para esclarecer pontos ausentes ou duvidosos no currículo em relação à vaga.")