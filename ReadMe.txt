# Context-Aware Requirement Clarification System

**(RAG-based Prototype for Tech–Client Conversations)**

---

## 1. Project Overview

This project implements a **context-aware backend system** designed for a technology company that interacts with clients through meetings, emails, and requirement documents.

The goal of the system is to **prevent loss of context and critical decisions** by:

* ingesting all customer-related documents,
* storing them in both structured and semantic memory,
* and generating an **engineering-style clarification questionnaire** based on all past context.

The focus of this milestone is **pipeline completeness**, not perfect AI output.

---

## 2. Problem Statement

In real-world projects:

* client requirements are spread across multiple documents,
* information contradicts over time,
* critical details are forgotten between meetings,
* and engineering teams repeatedly ask the same questions.

This system ensures that:

* all customer context is retained,
* past information is retrievable when needed,
* and missing or ambiguous requirements are surfaced automatically.

---

## 3. What Has Been Built (Scope So Far)

### ✅ Completed

* Customer creation
* Multi-document upload per customer
* Text extraction from uploaded files
* Chunking of extracted text
* Embedding generation
* Semantic storage in Pinecone (vector DB)
* Structured storage in PostgreSQL
* Context-aware questionnaire generation using AI
* Persistence of generated questionnaires and questions
* Full verification via pgAdmin and Swagger UI

### Not in Scope (Yet)

* Real user-facing frontend
* Live chat / email trigger engine
* Memory graph / knowledge graph
* Decision tracking across time
* Customer answering workflow UI

---

## 4. High-Level Architecture

### Core Components

1. **FastAPI Backend**
   Handles APIs, orchestration, and AI calls.

2. **PostgreSQL (Dockerized)**
   Stores structured data and system truth.

3. **Pinecone Vector Database**
   Stores semantic embeddings for retrieval.

4. **OpenAI Models**

   * Embeddings model for vectorization
   * Chat model for questionnaire generation

5. **Swagger UI (Temporary Frontend)**
   Used for testing and demo purposes.

---

## 5. Technology Stack

| Layer            | Technology                             |
| ---------------- | -------------------------------------- |
| Backend API      | FastAPI + Uvicorn                      |
| Structured DB    | PostgreSQL                             |
| DB Admin         | pgAdmin                                |
| Vector DB        | Pinecone                               |
| Embeddings       | OpenAI `text-embedding-3-small`        |
| LLM              | OpenAI Chat Model (e.g. `gpt-4o-mini`) |
| Containerization | Docker                                 |
| Storage          | Local filesystem                       |

---

## 6. PostgreSQL Schema (Structured Memory)

PostgreSQL acts as the **system of record**.

### Tables and Purpose

#### 1. `customers`

Stores customer/client information.
Everything in the system is scoped by `customer_id`.

#### 2. `documents`

Stores metadata for uploaded documents:

* document type (meeting minutes, requirements, emails)
* filename
* storage path
* upload timestamp

#### 3. `document_texts`

Stores extracted plain text from documents so AI can process them.

#### 4. `chunks`

Stores chunked segments of text and links them to Pinecone vectors.
Acts as the bridge between Postgres and the vector DB.

#### 5. `project_analysis`

Stores AI-generated breakdowns of customer requirements and detected constraints.

#### 6. `questionnaires`

Stores the generated questionnaire as a persistent artifact.
Tracks status (`draft`, `sent`, `completed`).

#### 7. `questions`

Stores individual clarification questions:

* question text
* priority
* topic category
* optional link to source chunk (traceability)

---

## 7. Pinecone Vector Database (Semantic Memory)

Pinecone stores **semantic representations** of document chunks.

### What Is Stored Per Vector

* Embedding vector (1536 dimensions)
* Metadata:

  * `customer_id`
  * `document_id`
  * `doc_type`
  * `chunk_index`
  * `uploaded_at`
  * `text` (chunk content)

### Why Pinecone Is Used

* Enables semantic retrieval (meaning-based search)
* Allows combining context across multiple documents
* Prevents reliance on keyword matching

---

## 8. End-to-End Pipeline Flow

### Step 1: Customer Creation

A new customer is created via API and stored in Postgres.

---

### Step 2: Document Upload

User uploads one or more documents:

* Meeting minutes
* Requirements
* Emails

Files are saved to local storage and metadata is saved in Postgres.

---

### Step 3: Text Extraction

Text is extracted from uploaded files and stored in `document_texts`.

---

### Step 4: Chunking

Extracted text is split into overlapping chunks to enable precise retrieval.

---

### Step 5: Embedding Generation

Each chunk is converted into an embedding using OpenAI’s embeddings model.

---

### Step 6: Vector Storage

Embeddings are stored in Pinecone with customer-scoped metadata.

---

### Step 7: Questionnaire Generation

When triggered:

* Pinecone retrieves relevant chunks across **all uploaded documents**
* Context is passed to the LLM with an **Engineer persona**
* The AI generates a structured questionnaire highlighting:

  * missing requirements
  * unclear constraints
  * integration questions
  * engineering concerns

---

### Step 8: Persistence

Generated questionnaire and questions are stored in Postgres.

---

## 9. Engineer Persona & AI Design

The AI operates with a **Senior Software Engineer persona**:

* focuses on implementation details
* avoids business fluff
* asks clarification questions that unblock development
* outputs structured JSON for reliability

This is **RAG-based prompting**, not fine-tuning or model training.

---

## 10. Frontend Status

No custom frontend has been built yet.

Swagger UI (`/docs`) is used as a **temporary testing frontend** to:

* create customers
* upload documents
* trigger questionnaire generation

A real frontend (React/Next.js) can be added later without backend changes.

---

## 11. Why This Design Is Correct

* Separates **structured truth** (Postgres) from **semantic memory** (Pinecone)
* Scales to multiple documents per customer
* Prevents context loss across time
* Matches real-world RAG system design
* Extensible to memory graphs and decision tracking

---

## 12. Future Extensions (Not Implemented Yet)

* Memory graph / knowledge graph
* Decision extraction and traceability
* Conflict detection across documents
* Customer response workflows
* Live chat / email triggers
* Frontend dashboard
* Role-based access

## How To Run (Windows)

### 1) Start Docker services (Postgres + pgAdmin)
```powershell
cd infra
docker compose up -d

cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload


3) Test via Swagger UI

Open:

http://127.0.0.1:8000/docs

4) pgAdmin (optional verification)

Open:

http://localhost:5050

Login:

admin@local.com
admin