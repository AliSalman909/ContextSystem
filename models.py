import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    documents: Mapped[list["Document"]] = relationship("Document", back_populates="customer")

    # NEW
    analyses: Mapped[list["ProjectAnalysis"]] = relationship("ProjectAnalysis", back_populates="customer")
    questionnaires: Mapped[list["Questionnaire"]] = relationship("Questionnaire", back_populates="customer")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("customers.id"), nullable=False)

    doc_type: Mapped[str] = mapped_column(String(50), nullable=False)  # meeting_minutes, requirements, email, questionnaire
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)

    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    customer: Mapped["Customer"] = relationship("Customer", back_populates="documents")
    text: Mapped["DocumentText"] = relationship("DocumentText", back_populates="document", uselist=False)
    chunks: Mapped[list["Chunk"]] = relationship("Chunk", back_populates="document")


class DocumentText(Base):
    __tablename__ = "document_texts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    document_id: Mapped[str] = mapped_column(String, ForeignKey("documents.id"), nullable=False, unique=True)
    extracted_text: Mapped[str] = mapped_column(Text, nullable=False)

    document: Mapped["Document"] = relationship("Document", back_populates="text")


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    document_id: Mapped[str] = mapped_column(String, ForeignKey("documents.id"), nullable=False)

    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)

    pinecone_vector_id: Mapped[str] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    document: Mapped["Document"] = relationship("Document", back_populates="chunks")

    # NEW (traceability from questions -> chunk)
    sourced_questions: Mapped[list["Question"]] = relationship("Question", back_populates="source_chunk")


# =========================
# NEW TABLES (Step additions)
# =========================

class ProjectAnalysis(Base):
    """
    Stores AI’s breakdown/analysis of requirements for a customer.
    Keep it simple for MVP; you can store constraints as text or JSON string.
    """
    __tablename__ = "project_analysis"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("customers.id"), nullable=False)

    summary: Mapped[str] = mapped_column(Text, nullable=False)
    detected_constraints: Mapped[str] = mapped_column(Text, nullable=True)  # JSON-like string for MVP
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    customer: Mapped["Customer"] = relationship("Customer", back_populates="analyses")


class Questionnaire(Base):
    __tablename__ = "questionnaires"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("customers.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(200), nullable=False, default="Requirements Clarification Questionnaire")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft")  # draft/sent/completed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    customer: Mapped["Customer"] = relationship("Customer", back_populates="questionnaires")
    questions: Mapped[list["Question"]] = relationship("Question", back_populates="questionnaire")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    questionnaire_id: Mapped[str] = mapped_column(String, ForeignKey("questionnaires.id"), nullable=False)

    text: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=True)

    # Optional but very useful (even if Pinecone doesn’t store these yet)
    priority: Mapped[str] = mapped_column(String(10), nullable=True)        # high/medium/low
    topic_category: Mapped[str] = mapped_column(String(50), nullable=True)  # Security/Database/Frontend/etc.

    # Traceability back to chunk
    source_chunk_id: Mapped[str] = mapped_column(String, ForeignKey("chunks.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    questionnaire: Mapped["Questionnaire"] = relationship("Questionnaire", back_populates="questions")
    source_chunk: Mapped["Chunk"] = relationship("Chunk", back_populates="sourced_questions")
