# AI Agent Email ✉️🤖

Un agente intelligente che legge le email e propone risposte automatiche.  
Obiettivo: risparmiare tempo nella gestione della posta elettronica, generando bozze pronte da inviare, con coerenza di tono, lingua e contesto.

---

## 🚀 Funzionalità (MVP)
- Ingestione email da provider (IMAP/Gmail API).
- Preprocess: pulizia corpo messaggio, rimozione firme e quote.
- Classificazione intent/priorità (richiesta info, reclamo, spam, ecc.).
- Generazione bozze (3 varianti: breve, standard, dettagliata) tramite LLM.
- UI web minimale per visualizzare thread e bozze.
- Feedback loop per apprendere dalle correzioni.

---

## 🛠️ Tech Stack
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+).
- **Database relazionale**: PostgreSQL (storage email/threads).
- **Vector DB**: [Chroma](https://www.trychroma.com/) (per embeddings e retrieval).
- **Orchestrazione LLM**: LangChain / LangGraph.
- **Frontend (in seguito)**: React/Next.js.

---

## 📂 Struttura progetto (iniziale)

```
AI-Agent-Email/
│── backend/
│   ├── main.py                # Entrypoint FastAPI con routing e orchestrazione pipeline
│   │  
│   ├── db.py                  # Connessione al DB Postgres + SessionLocal
│   ├── models.py              # Modelli SQLAlchemy (Email, Thread, Preferences, Events, ecc.)
│   ├── schemas.py             # Schemi Pydantic per request/response API
│   │  
│   ├── ingestion/  
│   │   ├── __init__.py  
│   │   ├── imap_client.py     # Connessione IMAP, polling email
│   │   ├── gmail_api.py       # Integrazione Gmail API (OAuth2)
│   │   └── parser.py          # Parsing email, allegati, pulizia HTML → testo
│   │  
│   ├── pipeline/  
│   │   ├── __init__.py  
│   │   ├── preprocess.py      # Pulizia corpo messaggio, firme, quote
│   │   ├── classifier.py      # Intent/priority classifier (ML/LLM)
│   │   ├── retriever.py       # Costruzione contesto (thread + KB) con RAG
│   │   ├── generator.py       # Generazione bozze con LLM
│   │   └── guardrails.py      # Validazioni, filtri PII, fallback
│   │  
│   ├── rag/  
│   │   ├── __init__.py  
│   │   ├── vector_store.py    # Gestione embeddings con Chroma/pgvector
│   │   ├── embeddings.py      # Creazione embeddings (OpenAI, sentence-transformers, ecc.)
│   │   └── knowledge_base.py  # Gestione documenti KB e chunking
│   │  
│   ├── feedback/  
│   │   ├── __init__.py  
│   │   ├── logger.py          # Log eventi feedback (bozze accettate, editate, scartate)
│   │   └── updater.py         # Aggiornamento preferenze, template, few-shot dinamici
│   │  
│   ├── utils/  
│   │   ├── __init__.py  
│   │   ├── settings.py        # Configurazioni (dotenv/env vars)
│   │   ├── security.py        # Crittografia, gestione segreti, policy privacy
│   │   └── templates.py       # Template standard di email e fallback
│   │  
│   ├── tests/  
│   │   ├── __init__.py  
│   │   ├── test_api.py        # Test endpoint FastAPI
│   │   ├── test_pipeline.py   # Test pipeline end-to-end
│   │   └── test_db.py         # Test modelli e DB
│   └── requirements.txt       # Dipendenze Python del progetto
│
├── README.md                  # Documentazione principale del progetto
├── .gitignore                 # File e cartelle da escludere dal version control
└── LICENSE                    # Licenza del software
````

---

## ⚙️ Setup locale (dev)
1. Clona il repo:
   ```bash
   git clone https://github.com/Rickyz03/AI-Agent-Email.git
   cd AI-Agent-Email/backend
   ```

2. Crea ed attiva un virtualenv:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Installa le dipendenze:

   ```bash
   pip install -r requirements.txt
   ```

4. Avvia il server:

   ```bash
   uvicorn main:app --reload
   ```

   API disponibili su: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📦 Dipendenze principali (requirements.txt)

* `fastapi`
* `uvicorn`
* `psycopg2-binary` (driver PostgreSQL)
* `sqlalchemy` (ORM)
* `chromadb`
* `langchain`
* `pydantic`
