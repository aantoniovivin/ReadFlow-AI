from typing import Literal, Optional

from pydantic import BaseModel, Field


class GlossaryTerm(BaseModel):
    term: str
    definition: str
    context: str = ""
    category: Literal["scientist", "person", "scientific_term", "location"] = "scientific_term"


class MechanicalBlock(BaseModel):
    subheading: str
    body: str


class ComprehensionCheck(BaseModel):
    question: str
    answer: str


class Subtopic(BaseModel):
    title: str
    body: str


class BriefingSection(BaseModel):
    title: str
    page_range: str = ""
    subtitle: str = ""
    takeaways: list[str] = Field(default_factory=list)
    body: list[str] = Field(default_factory=list)
    foundational_overview: str = ""
    key_takeaways: list[str] = Field(default_factory=list)
    mechanical_deep_dive: list[MechanicalBlock] = Field(default_factory=list)
    clinical_or_realworld_significance: str = ""
    quick_comprehension_checks: list[ComprehensionCheck] = Field(default_factory=list)
    process_hierarchy: list[str] = Field(default_factory=list)
    process_details: list[str] = Field(default_factory=list)
    comparison_analysis: list[dict] = Field(default_factory=list)
    important_rules: list[str] = Field(default_factory=list)
    subtopics: list[Subtopic] = Field(default_factory=list)
    source_pages_referenced: list[int] = Field(default_factory=list)


class Briefing(BaseModel):
    executive_summary: str
    sections: list[BriefingSection]
    terms: list[GlossaryTerm] = Field(default_factory=list)


class TermBox(BaseModel):
    term: str
    definition: str
    context: str = ""
    page: int
    x: float
    y: float
    width: float
    height: float


class ChatRequest(BaseModel):
    question: str


class DisambiguationOption(BaseModel):
    entity: str
    entity_name: str
    entity_type: str
    disambiguation: str


class ResolvedEntity(BaseModel):
    name: str
    type: str
    description: str
    confidence: float = 1.0


class EntityExplanation(BaseModel):
    definition: str
    context: str = ""
    technical_explanation: str = ""
    example: str = ""


class ExternalSource(BaseModel):
    title: str = ""
    url: str = ""
    description: str = ""


class ExternalImage(BaseModel):
    url: str = ""
    proxy_url: str = ""
    title: str = ""
    source_url: str = ""
    provider: Literal["wikipedia", "wikimedia", "openverse", "svg_fallback", "none"] = "none"


class TermExplainRequest(BaseModel):
    term: str = Field(min_length=1, max_length=120)
    page: Optional[int] = Field(default=None, ge=1)
    section_index: Optional[int] = Field(default=None, ge=0)
    sentence: str = Field(default="", max_length=1200)
    resolved_entity: Optional[str] = Field(default=None, max_length=150)
    entity_type: Optional[str] = Field(default=None, max_length=100)


class ChatResponse(BaseModel):
    answer: str

