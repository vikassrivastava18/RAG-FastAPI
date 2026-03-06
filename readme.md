# RAG (Retrieval-Augmented Generation) — FastAPI + PostgreSQL

Brief RAG application combining a FastAPI backend, PostgreSQL persistence, and LLM orchestration.

## Quick Start

1. Create a virtual environment and activate it:
```powershell
python -m venv .venv
.venv\Scripts\activate  # PowerShell
# or
.venv\Scripts\activate.bat   # cmd
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Configure environment variables (example .env):
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your_jwt_secret
....
```

4. Run (development):
```powershell
uvicorn main:app --reload
```

## Project layout

```
├── .env
├── main.py
├── requirements.txt
├── readme.md
├── api/
│   ├── __init__.py
│   ├── books.py
│   ├── llm.py
│   └── auth.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── scrap.py
│   └── utils.py
├── db/
│   ├── __init__.py
│   ├── models.py
│   ├── schemas.py
│   └── query.py
├── llm/
│   ├── __init__.py
│   ├── generate.py
│   └── vector.py
├── frontend/
│   ├── templates/
│   │   ├── template.html
│   │   └── login.html
│   └── assets/
│       └── js/
│           └── main.js
└── folders/
    └── logos/
```

## Folder purpose

- api/
  - FastAPI route modules and HTTP entry points.
  - Example files:
    - api/books.py — endpoints for book content, PPT/worksheet generation.
    - api/llm.py — endpoints exposing LLM-powered features (summaries, quizzes).
    - api/auth.py — authentication routes (login, token refresh).

- core/
  - Application-wide utilities and configuration.
  - config.py — settings loader, DB session factory, JWT and LLM client initialization.
  - scrap.py — scraping/parsing logic to extract book structure and content.
  - utils.py — small helpers (file handling, text normalization, PDF utils).

- db/
  - Database layer: models, Pydantic schemas, and query helpers.
  - models.py — SQLAlchemy models (User, Book, Chapter, Content, etc.).
  - schemas.py — request/response Pydantic schemas.
  - query.py — reusable DB access functions and bulk insert utilities.

- llm/
  - LLM orchestration and vector search.
  - generate.py — prompt templates, orchestration, response parsing, generation helpers.
  - vector.py — vector store integration (embedding, persistence, nearest-neighbor retrieval).

- frontend/
  - Static templates and frontend assets served by FastAPI (if any).
  - templates/ — HTML templates.
  - assets/ — JS/CSS used by UI pages that call backend endpoints.

- folders/
  - Static files and other app assets (images, logos, sample data).

## Key runtime pieces

- Authentication
  - Implemented via JWT; configured in core/config.py and routes in api/auth.py.

- Scraping & Ingestion
  - core/scrap.py extracts book structure (chapters, topics) and raw text for indexing.

- Persistence
  - PostgreSQL is used for structured data. Connection string is set via DATABASE_URL env var.

- Vector search & LLM
  - llm/vector.py handles embeddings and vector store.
  - llm/generate.py composes prompts, calls the LLM, and formats outputs.





