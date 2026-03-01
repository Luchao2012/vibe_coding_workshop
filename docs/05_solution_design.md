
# Solution Design

## System Architecture

```
┌─────────────┐
│   ACC       │
│  Website    │
└──────┬──────┘
       │
       │ 1. Crawl pages
       ▼
┌─────────────────┐
│   Web Crawler   │  (httpx + BeautifulSoup)
│  (crawler.py)   │
└────────┬────────┘
         │
         │ 2. Save as markdown
         ▼
┌─────────────────┐
│  data/raw/      │  (.md files)
└────────┬────────┘
         │
         │ 3. Load & chunk
         ▼
┌─────────────────┐
│  Vector Store   │  (Chroma + OpenAI embeddings)
│  (vectorstore/) │
└────────┬────────┘
         │
         │ 4. Semantic search
         ▼
┌─────────────────┐
│   Retriever     │  (LangChain)
│  (retriever.py) │
└────────┬────────┘
         │
         │ 5. Context + Question
         ▼
┌─────────────────┐
│   LLM (GPT)     │  (OpenAI API)
│  (chatbot.py)   │
└────────┬────────┘
         │
         │ 6. Answer
         ▼
┌─────────────────┐
│   Streamlit UI  │
│    (app.py)     │
└─────────────────┘
```

## Data Flow

### Phase 1: Data Ingestion (Offline)
1. **Input:** List of ACC website URLs
2. **Crawler:** Fetch HTML, extract text using BeautifulSoup
3. **Output:** Save each page as `.md` file in `data/raw/`

### Phase 2: Vector Database Setup (One-time)
4. **Input:** Markdown files from `data/raw/`
5. **Chunking:** Split into ~500 token chunks (LangChain)
6. **Embedding:** Convert chunks to vectors using OpenAI embeddings
7. **Storage:** Store in Chroma (local directory `data/vectorstore/`)

### Phase 3: Query Answering (Runtime)
8. **User asks question** via Streamlit
9. **Embed question** (same embedding model)
10. **Semantic search:** Find top-k similar chunks in Chroma
11. **Construct prompt:** Combine context + question
12. **LLM generates answer** using GPT-3.5/4
13. **Display answer** in Streamlit UI

## Folder Structure

```
vibe_coding_workshop/
├── README.md                    # Main instructions
├── .env.example                 # Template for API keys
├── .env                         # Actual keys (gitignored)
├── requirements.txt             # Python dependencies
├── docs/                        # Planning documents
│   ├── 01_problem_statement.md
│   ├── 02_brainstorming.md
│   ├── 03_brd.md
│   ├── 04_prd.md
│   └── 05_solution_design.md
├── data/
│   ├── raw/                     # Crawled markdown files
│   └── vectorstore/             # Chroma database
├── src/
│   ├── __init__.py
│   ├── crawler.py               # Web scraping logic
│   ├── ingest.py                # Load data into vectorstore
│   ├── retriever.py             # RAG retriever setup
│   ├── chatbot.py               # LLM chat logic
│   └── config.py                # Config (URLs, settings)
└── app.py                       # Streamlit entry point
```

## Tech Stack Decisions

| Component | Technology | Reason |
|-----------|-----------|--------|
| **Backend Language** | Python 3.11+ | Simple, widely taught, great for AI/ML |
| **Web Framework** | FastAPI (not used in MVP, Streamlit only) | Reserved for future API |
| **UI** | Streamlit | Simplest for workshop; single file, no HTML/JS |
| **Web Scraping** | httpx + BeautifulSoup4 | Lightweight, synchronous, easy to debug |
| **Vector DB** | Chroma | Local, no server needed, simple API |
| **Embeddings** | OpenAI `text-embedding-3-small` | High quality, cost-effective |
| **LLM** | OpenAI GPT-3.5-turbo | Fast, cheap, good for demos |
| **RAG Framework** | LangChain | Simplifies RAG pipeline, well-documented |

## Tradeoffs

### Why Chroma (not Pinecone/Weaviate)?
- **Pro:** Local storage, no API keys or server setup
- **Pro:** Perfect for workshops
- **Con:** Not production-scalable
- **Decision:** Simplicity wins for demo

### Why Streamlit (not FastAPI + HTML)?
- **Pro:** Single Python file, instant UI
- **Pro:** Less code for students to understand
- **Con:** Less flexibility for custom design
- **Decision:** Workshop focus = Streamlit

### Why OpenAI (not open-source LLM)?
- **Pro:** High-quality embeddings and generation
- **Pro:** No GPU needed
- **Con:** Costs money (but minimal for demo)
- **Decision:** Reliability and simplicity

## RAG Explanation (For Teaching)

**RAG = Retrieval-Augmented Generation**

### The Problem:
- LLMs like GPT don't know about ACC specifically
- If we just ask "What are ACC's membership fees?", it will guess or say "I don't know"

### The Solution (RAG):
1. **Retrieval:** When user asks a question, search our vector database for relevant ACC content
2. **Augmentation:** Add that content to the prompt as "context"
3. **Generation:** LLM generates answer based on provided context

### Example:

**Without RAG:**
- Question: "How much is membership?"
- LLM: "I don't have specific information about ACC membership fees."

**With RAG:**
- Question: "How much is membership?"
- System finds: "ACC individual membership is $50/year. Family membership is $120/year."
- LLM sees context and answers: "ACC offers individual membership for $50/year and family membership for $120/year."

**Key insight:** We're giving the LLM the information it needs, so it doesn't have to memorize or guess.

## Security Considerations

**For MVP (workshop):**
- API keys in `.env` file (never commit to git)
- `.gitignore` includes `.env`, `data/`, and `__pycache__/`
- No user authentication (public demo)
- No sensitive data collection

**Future (production):**
- Use secrets management (AWS Secrets Manager, etc.)
- Add rate limiting
- Input validation (prevent prompt injection)
- User authentication

## Scalability Limitations (Demo Scope)

**This is a DEMO, not production-ready:**
- **Chroma:** Runs locally, not distributed
- **No caching:** Every question re-queries DB
- **Single-user:** Streamlit isn't built for thousands of concurrent users
- **No monitoring:** No logs, metrics, or error tracking

**To scale for production, would need:**
- Managed vector DB (Pinecone, Weaviate Cloud)
- API backend (FastAPI) with proper async handling
- Frontend app (React)
- Caching layer (Redis)
- Monitoring (Prometheus, Grafana)
- CI/CD pipeline

**But for a workshop:** This design is perfect ✓

## Development Phases

### Phase 1: Setup & Crawling
- Set up project structure
- Install dependencies
- Write crawler
- Test on 5 ACC pages

### Phase 2: Vector Database
- Implement ingestion script
- Chunk documents
- Store in Chroma
- Test retrieval

### Phase 3: Chatbot Logic
- Set up LangChain RAG chain
- Test question answering in notebook/script
- Verify responses are grounded

### Phase 4: Streamlit UI
- Build simple chat interface
- Connect to chatbot backend
- Test end-to-end flow

### Phase 5: Documentation & Testing
- Write README with run instructions
- Test on fresh environment
- Add comments for teaching
