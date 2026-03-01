# ACC Admin Helper Chatbot (Workshop Demo)

This is a simple, end-to-end demo chatbot for ACC. It answers common questions about membership, benefits, and general information by crawling ACC’s website and using a Retrieval-Augmented Generation (RAG) pipeline.

## What’s Included (MVP)

- Website crawler (httpx + BeautifulSoup)
- Local vector database (Chroma)
- RAG chatbot (LangChain + OpenAI)
- Simple UI (Streamlit)

## Folder Structure

```
vibe_coding_workshop/
├── app.py
├── requirements.txt
├── .env.example
├── data/
│   ├── raw/
│   └── vectorstore/
├── docs/
└── src/
```

## Setup (Python 3.11+)

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your API key:

```bash
cp .env.example .env
```

Open `.env` and add your OpenAI key.

## Next Steps (We will build)

1. Build the crawler to fetch ACC pages
2. Ingest content into Chroma
3. Add RAG chatbot logic
4. Create Streamlit UI

## Notes

- This is a workshop demo, not production-ready
- No personal data is collected
- Only public website data is used