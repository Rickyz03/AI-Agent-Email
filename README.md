# AI Agent Email ✉️🤖

An intelligent agent that reads emails and proposes automatic replies.  
Goal: save time in email management by generating ready-to-send drafts with consistent tone, language, and context.

---

## 🚀 Features (MVP)
- Email ingestion from providers (IMAP/Gmail API).
- Preprocessing: message body cleaning, signature and quote removal.
- Intent/priority classification (info request, complaint, spam, etc.).
- Draft generation (3 variants: brief, standard, detailed) via LLM.
- Minimal web UI to view threads and drafts.
- Feedback loop to learn from corrections.

---

## 🛠️ Tech Stack
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+).
- **Relational Database**: PostgreSQL (email/threads storage).
- **Vector DB**: [Chroma](https://www.trychroma.com/) (for embeddings and retrieval).
- **LLM Orchestration**: LangChain / LangGraph.
- **Frontend (later)**: React/Next.js.

---

## 📂 Project Structure

```
AI-Agent-Email/
│── backend/
│   ├── main.py                # FastAPI entrypoint with routing and pipeline orchestration
│   │  
│   ├── db.py                  # Postgres DB connection + SessionLocal
│   ├── models.py              # SQLAlchemy models (Email, Thread, Preferences, Events, etc.)
│   ├── schemas.py             # Pydantic schemas for API request/response
│   │  
│   ├── ingestion/  
│   │   ├── __init__.py  
│   │   ├── imap_client.py     # IMAP connection, email polling
│   │   ├── gmail_api.py       # Gmail API integration (OAuth2)
│   │   └── parser.py          # Email parsing, attachments, HTML → text cleaning
│   │  
│   ├── pipeline/  
│   │   ├── __init__.py  
│   │   ├── preprocess.py      # Message body cleaning, signatures, quotes
│   │   ├── classifier.py      # Intent/priority classifier (ML/LLM)
│   │   ├── retriever.py       # Context building (thread + KB) with RAG
│   │   ├── generator.py       # Draft generation with LLM
│   │   └── guardrails.py      # Validations, PII filters, fallbacks
│   │  
│   ├── rag/  
│   │   ├── __init__.py  
│   │   ├── vector_store.py    # Embeddings management with Chroma/pgvector
│   │   ├── embeddings.py      # Embeddings creation (OpenAI, sentence-transformers, etc.)
│   │   └── knowledge_base.py  # KB documents management and chunking
│   │  
│   ├── feedback/  
│   │   ├── __init__.py  
│   │   ├── logger.py          # Feedback events logging (drafts accepted, edited, discarded)
│   │   └── updater.py         # Preferences, templates, dynamic few-shot updates
│   │  
│   ├── utils/  
│   │   ├── __init__.py  
│   │   ├── settings.py        # Configurations (dotenv/env vars)
│   │   ├── security.py        # Encryption, secrets management, privacy policies
│   │   └── templates.py       # Standard email templates and fallbacks
│   │  
│   ├── tests/  
│   │   ├── __init__.py  
│   │   ├── test_api.py        # FastAPI endpoint tests
│   │   ├── test_pipeline.py   # End-to-end pipeline tests
│   │   └── test_db.py         # Model and DB tests
│   │
│   ├── .env                   # Environment variables configuration
│   └── requirements.txt       # Python project dependencies
│
├── README.md                  # Main project documentation
├── .gitignore                 # Files and folders to exclude from version control
└── LICENSE                    # Software license
````

---

## ⚙️ Local Setup (Dev)

1. **Clone the repository**

   ```bash
   git clone https://github.com/Rickyz03/AI-Agent-Email.git
   cd AI-Agent-Email/backend
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start external services with Docker**

   * **PostgreSQL**

     ```bash
     docker pull postgres
     docker run -d --name postgres-db \
       -e POSTGRES_USER=email-agent-user \
       -e POSTGRES_PASSWORD=email-agent-psw \
       -e POSTGRES_DB=email-agent-db \
       -p 5432:5432 postgres
     ```

   * **ChromaDB**

     ```bash
     docker pull chromadb/chroma
     docker run -d --name chroma-db -p 8000:8000 chromadb/chroma
     ```

5. **Configure environment variables**

   Copy `.env` (example provided in repo) and set your credentials:

   ```env
   # Database
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=email-agent-user
   DB_PASSWORD=email-agent-psw
   DB_NAME=email-agent-db

   # External APIs
   OPENAI_API_KEY=your-openai-key

   # Chroma
   CHROMA_URL=http://localhost:8000

   # Security
   SECRET_KEY=your-secret-key
   ```

   * **SECRET\_KEY**: used to encrypt/decrypt sensitive data.
     Generate one locally with:

     ```bash
     python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
     ```

6. **Initialize the database**

   ```bash
   python -c "from db import Base, engine; Base.metadata.create_all(bind=engine)"
   ```

7. **Start the FastAPI backend server**

   ```bash
   uvicorn main:app --reload --port 8001
   ```

   * The backend runs at: [http://localhost:8001](http://localhost:8001)
   * Interactive API docs: [http://localhost:8001/docs](http://localhost:8001/docs)

8. **Next steps**

   * Use `/ingest` to fetch emails from Gmail or IMAP into the DB.
   * Use `/draft` to generate automatic reply drafts.
   * Use `/kb/index` to add documents to the knowledge base.
   * Use `/preferences` to set tone/signature.
   * Use `/feedback` to log user actions.

9. **Next steps after server start**

   * Use the **API** (e.g. `/draft` endpoint) to generate automatic replies for emails.
   * Integrate with the **frontend** (when available) to browse threads, see summaries, and apply actions (accept/edit/send).
   * Check logs in console for feedback and RAG retrieval details.
   * Add documents to the knowledge base (`rag/knowledge_base.py`) to improve draft quality.


