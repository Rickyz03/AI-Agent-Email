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

   Copy `.env` in the _backend/_ folder and set your credentials:

   ```env
   # Database
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=email-agent-user
   DB_PASSWORD=email-agent-psw
   DB_NAME=email-agent-db

   # OpenAI
   OPENAI_API_KEY=your-openai-key
   OPENAI_MODEL_NAME=gpt-4o-mini

   # Chroma
   CHROMA_HOST=localhost
   CHROMA_PORT=8000
   CHROMA_COLLECTION=emails

   # IMAP
   IMAP_HOST=imap.libero.it
   IMAP_PORT=993
   IMAP_USERNAME=your-email@libero.it
   IMAP_PASSWORD=your-password

   # Security
   SECRET_KEY=your-secret-key

   # Signing name
   SIGNING_NAME=Name Surname
   ```

   * **SECRET\_KEY**: used to encrypt/decrypt sensitive data.
     Generate one locally with:

     ```bash
     python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
     ```

   Then, copy `.env.local` in the _frontend/_ folder:

   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8001

   # Email ingestion defaults
   NEXT_PUBLIC_EMAIL_PROVIDER=gmail
   NEXT_PUBLIC_EMAIL_UNREAD=false
   NEXT_PUBLIC_EMAIL_N=50
   ```

6. **Prepare Gmail API credentials**

   To allow Gmail ingestion, you need two local files:  
   - `credentials.json` → OAuth 2.0 credentials downloaded from Google Cloud Console.  
   - `token.json` → generated after the first authentication.  

   ### How to obtain `credentials.json`  
   1. Go to [Google Cloud Console](https://console.cloud.google.com/).  
   2. Create a new project (or select an existing one).  
   3. Navigate to **API & Services > Library** and enable the **Gmail API**.  
   4. Go to **API & Services > Credentials**.  
   5. Click **Create Credentials > OAuth Client ID**.  
      * Application type: **Desktop App** (for local testing).  
   6. Download the JSON file and rename it to `credentials.json`.  
   7. Place this file inside the `backend/ingestion` folder.  

   ### How to generate `token.json`  
   1. Activate the virtual environment:  

      ```bash
      venv\Scripts\activate   # Windows
      source venv/bin/activate   # Linux/Mac
      ```  

   2. Navigate into the ingestion folder and run the init script:  

      ```bash
      cd ingestion
      python init_gmail.py
      ```  

   3. A browser window will open asking you to log in with your Gmail account.  
      - If the app is unverified, click **Advanced > Continue anyway**.  
      - Make sure your Gmail address is added as a **Test User** in the OAuth consent screen on Google Cloud Console.  

   4. After successful login, a `token.json` file will be created in the same folder.  

   ⚠️ **Note**: Both `credentials.json` and `token.json` are ignored in `.gitignore` and must be created manually by each developer.

7. **Start the FastAPI backend server**

   ```bash
   uvicorn main:app --reload --port 8001
   ```

   * The backend runs at: [http://localhost:8001](http://localhost:8001)
   * Interactive API docs: [http://localhost:8001/docs](http://localhost:8001/docs)

8. **Endpoints**

   * Use `/ingest` to fetch emails from Gmail or IMAP into the DB.
   * Use `/draft` to generate automatic reply drafts.
   * Use `/kb/index` to add documents to the knowledge base.
   * Use `/preferences` to set tone/signature.
   * Use `/feedback` to log user actions.

9. **Start the Next.js frontend**

   * Open a new terminal (keep the backend running on port `8001`).

   * Move into the `frontend/` folder:

      ```bash
      cd ../frontend
      ```

   * Install dependencies:

      ```bash
      npm install
      ```

   * Start the development server:

      ```bash
      npm run dev
      ```

      * The frontend runs at: [http://localhost:3000](http://localhost:3000)

---

10. **Next steps after full stack startup**

* Browse the **Inbox** dashboard at [http://localhost:3000](http://localhost:3000).
* Generate drafts with the **AI Draft Panel** or manually via **Manual Draft**.
* Manage your **preferences** (tone, signature, style) in the **Settings** page.
* Upload documents to the **Knowledge Base** via the **KB** page.
* Provide feedback with the **Accept / Edit / Reject** buttons → feedback is logged in the backend.

---

## 📂 Project Structure

```
AI-Agent-Email/
│── backend/
│   ├── main.py                  # FastAPI entrypoint with routing and pipeline orchestration
│   │  
│   ├── db.py                    # Postgres DB connection + SessionLocal
│   ├── models.py                # SQLAlchemy models (Email, Thread, Preferences, Events, etc.)
│   ├── schemas.py               # Pydantic schemas for API request/response
│   │  
│   ├── ingestion/               # Handles email ingestion from various sources
│   ├── pipeline/                # Contains processing logic for email data
│   ├── rag/                     # Implements retrieval-augmented generation techniques
│   ├── feedback/                # Manages user feedback and updates
│   ├── utils/                   # Utility functions and helpers
│   ├── tests/                   # Contains test cases for the application
│   │
│   ├── Dockerfile               # Docker image for backend service
│   ├── .env                     # Environment variables configuration
│   ├── requirements.txt         # Python project dependencies
│   ├── .gitignore               # Backend files and folders to exclude from version control
│   ├── test_endpoints.ps1       # PowerShell script for testing API endpoints
│   └── test_endpoints.sh        # Bash script for testing API endpoints
│
│   frontend/
│   ├── app/
│   │   ├── layout.tsx           # Main layout (header, sidebar, theme)
│   │   ├── page.tsx             # Dashboard Inbox (default view)
│   │   ├── globals.css          # Global styles and Tailwind config
│   │   │
│   │   ├── threads/             # Single thread/email page
│   │   ├── manual/              # Manual Form for AI Draft Generator
│   │   ├── settings/            # User preferences
│   │   ├── kb/                  # Knowledge Base management
│   │   ├── api/                 # Client-side wrapper for backend calls
│   │   │
│   │   ├── components/          # Reusable UI components
│   │   │
│   │   ├── lib/                 # Generic utilities
│   │   └── types/               # Shared types
│   │
│   ├── Dockerfile               # Docker image for frontend service
│   ├── .env.local               # Environment variables for frontend configuration
│   ├── package.json             # Project metadata and dependencies for Node.js
│   └── .gitignore               # Frontend files and folders to exclude from version control
│
├── docker-compose.yml           # Docker Compose configuration for local development
├── README.md                    # Main project documentation
└── LICENSE                      # Software license
````

