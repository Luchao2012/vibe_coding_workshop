"""
WORKSHOP GUIDE: Running the ACC Admin Helper Chatbot

This guide walks you through running the chatbot end-to-end.
"""

# ============================================================================
# STEP 1: PREPARE (if you haven't already)
# ============================================================================

# Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install packages
pip install -r requirements.txt

# Set your OpenAI API key
cp .env.example .env
# Edit .env and paste your key: OPENAI_API_KEY=sk-...


# ============================================================================
# STEP 2: UNDERSTAND THE CODE (brief walkthrough)
# ============================================================================

# src/crawler.py
# - Fetches ACC website pages (already ran, see data/raw/)
# - Extracts text from HTML
# - Saves as markdown files

# src/corpus.py
# - Loads the 7 markdown files
# - Provides search() function for keyword matching
# - Returns relevant snippets when you ask a question

# src/chatbot.py
# - Takes a question + search results
# - Sends to OpenAI with system prompt
# - Returns generated answer (grounded in the data)

# app.py
# - Streamlit UI
# - Loads corpus
# - Shows chat interface
# - Displays source documents


# ============================================================================
# STEP 3: RUN THE APP
# ============================================================================

streamlit run app.py

# Expected: Opens http://localhost:8501 in browser
# You'll see:
#   - Title: "ACC Admin Helper Chatbot"
#   - Status: "✓ Loaded 7 pages from ACC website"
#   - Input box: "Ask a Question"
#   - Sidebar: Example questions


# ============================================================================
# STEP 4: TEST IT
# ============================================================================

# Try these in the chat box:

1. "How much does membership cost?"
   Expected: Answer about ACC membership fees

2. "What programs does ACC offer?"
   Expected: List of programs/events

3. "What are the benefits of joining?"
   Expected: Benefits description

4. "How do I become a member?"
   Expected: Membership process

5. "Where is ACC located?"
   Expected: Address in Houston

# See the "Source Documents" expander below the answer
# to see which pages the chatbot used


# ============================================================================
# HOW IT WORKS (under the hood)
# ============================================================================

Question: "How much does membership cost?"

1. SEARCH (corpus.py)
   - Finds keywords: "membership" "cost" "fee" "price"
   - Returns top 3 relevant document chunks
   - Example: "...individual membership is $50/year..."

2. RAG (chatbot.py)
   - Builds a prompt:
     System: "You are an ACC assistant. Answer using only provided context."
     Context: [those document chunks]
     User: "How much does membership cost?"

3. LLM (OpenAI)
   - Processes the prompt
   - Generates answer using ONLY the provided context
   - Never makes things up (hallucinations prevented!)

4. DISPLAY (app.py)
   - Shows answer in chat
   - Shows source documents for transparency


# ============================================================================
# KEY CONCEPTS FOR STUDENTS
# ============================================================================

## RAG = Retrieval-Augmented Generation

Without RAG:
  Q: "How much does ACC membership cost?"
  A: "I don't know anything about ACC"

With RAG:
  Q: "How much does ACC membership cost?"
  Search: Find "ACC membership cost $50/year"
  A: "ACC membership costs $50 per year"

RAG gives the LLM the facts it needs!

## Why no vector database?

- Only ~9,000 tokens of data (tiny!)
- Simple keyword search is enough
- Simpler code for students
- Faster setup (no pip wheel building issues)

## What we DID use

✓ Simple keyword search (Python strings)
✓ OpenAI for LLM
✓ Streamlit for UI
✓ httpx + BeautifulSoup for crawling


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

Issue: "ModuleNotFoundError: No module named 'openai'"
Solution: pip install openai

Issue: "Error: OPENAI_API_KEY not set"
Solution: Add your key to .env file

Issue: "No answers, or generic responses"
Solution: Your OpenAI API key might be invalid, or daily limit reached

Issue: "Streamlit won't start"
Solution: Make sure you're in the .venv:
  source .venv/bin/activate
  streamlit run app.py


# ============================================================================
# NEXT STEPS (if you want to enhance)
# ============================================================================

1. Add more ACC pages to crawl (update config.py)
2. Improve keyword search (add synonyms)
3. Add conversation history
4. Deploy on Heroku/AWS
5. Add multi-language support
6. Use a vector database (Chroma, Pinecone) for 100x scale

That's it! Enjoy exploring RAG chatbots! 🚀
