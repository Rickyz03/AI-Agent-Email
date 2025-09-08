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

AI-Agent-Email/
│── backend/
│   ├── main.py          # API FastAPI
│   ├── models.py        # Modelli Pydantic + ORM
│   ├── db.py            # Connessione al DB
│   ├── vectorstore.py   # Gestione embeddings con Chroma
│   └── requirements.txt
│
│── README.md
│── .gitignore

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

---

## ✅ Prossimi step

* [ ] Ingestione email via IMAP.
* [ ] Definizione schema DB (threads, emails, kb\_docs, ecc.).
* [ ] Integrazione Vector DB (Chroma).
* [ ] Generazione bozze via LLM.
