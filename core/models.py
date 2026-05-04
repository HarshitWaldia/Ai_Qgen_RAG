from pydantic import BaseModel, Field
from typing import List, Optional

# --- API Request Models ---
class SectionConfig(BaseModel):
    name: str = "Section A"
    q_type: str = Field(description="MCQ, Short Answer, Long Answer, Case-Based")
    count: int
    marks_per_question: int
    difficulty: str = Field(description="Easy, Medium, Hard")

class GenerateRequest(BaseModel):
    document_id: str
    language: str = "English"
    sections: List[SectionConfig]
    specific_topic: Optional[str] = None

# --- LLM Structured Output Models ---
class Option(BaseModel):
    label: str = Field(description="A, B, C, or D")
    text: str

class GeneratedQuestion(BaseModel):
    q_number: int
    text: str
    question_type: str
    options: List[Option] = Field(default_factory=list, description="Only for MCQs, otherwise provide an empty list []")
    marks: int
    difficulty: str
    blooms_taxonomy: str = Field(description="E.g., Remembering, Understanding, Applying, Analyzing")
    answer: str = Field(description="Exact answer derived strictly from context")
    explanation: str = Field(description="Detailed explanation with context reference")

class GeneratedSection(BaseModel):
    name: str
    questions: List[GeneratedQuestion]

class QuestionPaperBlueprint(BaseModel):
    title: str
    language: str
    sections: List[GeneratedSection]