
<img src="assets/tutor.png" alt="Socratic Dialogue Tutor" width="700"/>

## Key features
- RAG based document answering functionality using FAISS and LangChain.
- Socratic dialogue style tutor for learning concepts using LangGraph.
- Ask user concept related question, give hint if the answer is not satifactory.

## LangGraph Workflow Diagram
<img src="assets/dialogue_graph.png" alt="LangGraph workflow diagram" width="400"/>


## Configuration
Add .env file in the backend directory and add following along with your OpenAI API key
```
OPENAI_API_KEY="Your OpenAI key"
DATABASE_URL="postgresql://postgres:hello2020@localhost:5432/testdb"
GPT_MODEL="gpt-4o"
SECRET_KEY="germkgndvalkrt45rtt3680983480@!@#&#^kjwjkklal2942947295001234111"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Quick Start

Run the application with
```
docker-compose build
docker-compose up
```


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





