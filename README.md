# 📚 EduTrust AI

## Source-Grounded Academic Assistant

EduTrust AI is a domain-specific academic assistant designed to provide
source-grounded answers from trusted academic documents.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant
information from academic documents before generating an answer.

---

# 🎯 Problem Statement

Generic AI systems may generate answers that are inaccurate, unsupported,
or unrelated to the student's trusted academic materials.

Students need an academic assistant that can:

- Search trusted academic documents
- Retrieve relevant information
- Generate answers using retrieved evidence
- Show supporting sources
- Detect possible source conflicts
- Check source freshness
- Identify possible misconceptions
- Handle insufficient information safely

---

# 💡 Proposed Solution

EduTrust AI follows a source-grounded question answering pipeline.

Student Question
        ↓
Academic Knowledge Base
        ↓
PDF Text Extraction
        ↓
Text Cleaning
        ↓
Chunking
        ↓
Semantic Embedding
        ↓
Vector Database
        ↓
Relevant Information Retrieval
        ↓
Evidence Confidence
        ↓
Gemini / Groq
        ↓
Grounded Answer
        ↓
Sources + Validation
        ↓
Streamlit UI

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      Student         │
                    │      Question        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI API      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Document Retrieval   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Sentence Transformer │
                    │    Embeddings        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      ChromaDB        │
                    │    Vector Database   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Relevant Academic    │
                    │      Context         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Gemini / Groq      │
                    │   Answer Generation  │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │ Answer + Sources + Confidence  │
              │ Conflict + Freshness +         │
              │ Misconception Check            │
              └───────────────┬────────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │     Streamlit UI      │
                    └──────────────────────┘