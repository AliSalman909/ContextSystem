from pydantic import BaseModel, Field
from typing import Literal, List, Optional


DocType = Literal["meeting_minutes", "requirements", "email", "questionnaire"]


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class CustomerOut(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class DocumentOut(BaseModel):
    id: str
    customer_id: str
    doc_type: str
    filename: str
    storage_path: str

    class Config:
        from_attributes = True


class QuestionnaireQuestion(BaseModel):
    q: str
    why: str
    priority: Literal["high", "medium", "low"] = "medium"


class QuestionnaireSection(BaseModel):
    title: str
    questions: List[QuestionnaireQuestion]


class QuestionnaireOut(BaseModel):
    customer_id: str
    sections: List[QuestionnaireSection]
    notes: Optional[str] = None
