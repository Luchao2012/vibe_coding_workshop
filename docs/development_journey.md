# Development Journey: ACC Admin Helper Chatbot

## Overview
This document summarizes the complete development journey of building a simple RAG (Retrieval-Augmented Generation) chatbot for the Asian Chamber of Commerce (ACC) to handle repetitive customer inquiries about membership, programs, and benefits.

**Target Audience**: Kids (grades 6-12) in a coding workshop  
**Goal**: Build a simple, explainable end-to-end demo

---

## Technology Stack

### Backend
- **Python 3.10+**: Core programming language
- **FastAPI**: (planned but not implemented - kept simple with Streamlit)
- **LangChain**: (considered but not used - manual RAG implementation for clarity)
- **httpx + BeautifulSoup4**: Web scraping
- **python-dotenv**: Environment variable management
- **OpenAI API**: LLM provider (gpt-4o model)

### Frontend
- **Streamlit**: Simple single-page UI (chosen for workshop simplicity)

### Data Storage
- **Local markdown files**: No vector database needed (only ~9k tokens of data)
- **Simple keyword search**: More explainable than embeddings for workshop

---

## Development Phases

### Phase 1: Planning & Documentation
Following the Software Development Lifecycle (SDLC) guidance in `software_development_lifecycle.md`:

1. **Problem Statement** ([01_problem_statement.md](01_problem_statement.md))
   - ACC receives repetitive inquiries about membership fees, benefits, joining procedures
   - Customer service team overwhelmed
   - Need automated solution

2. **Brainstorming** ([02_brainstorming.md](02_brainstorming.md))
   - Explored solutions: FAQ page, chatbot, email automation, knowledge base
   - Selected RAG chatbot as best balance of automation and natural interaction

3. **Business Requirements** ([03_business_requirements.md](03_business_requirements.md))
   - Answer common questions accurately
   - Reduce customer service workload
   - Provide 24/7 availability
   - Simple demo for workshop

4. **Product Requirements** ([04_product_requirements.md](04_product_requirements.md))
   - Web crawler for ACC website
   - RAG system with keyword search
   - Streamlit UI with chat interface
   - Source document transparency

5. **Solution Design** ([05_solution_design.md](05_solution_design.md))
   - Architecture: Crawler → Markdown Files → Corpus Loader → RAG Chatbot → Streamlit UI
   - Simple, explainable components

### Phase 2: Implementation

#### 2.1 Project Structure
```
vibe_coding_workshop/
├── .env                          # API keys (gitignored)
├── .env.example                  # Template for API keys
├── requirements.txt              # Python dependencies
├── app.py                        # Streamlit UI
├── src/
│   ├── config.py                # Crawler configuration
│   ├── crawler.py               # Web scraper
│   ├── corpus.py                # Document loader & search
│   └── chatbot.py               # RAG implementation
├── data/
│   └── raw/                     # Crawled markdown files
└── docs/                        # Planning documents
```

#### 2.2 Web Crawler ([src/crawler.py](../src/crawler.py))
- Extracts text from HTML: h1-h4, p, li, div, span elements
- Recursive link following (max 50 pages)
- Saves as markdown files
- Rate limiting (1 second delay between requests)

**Key Learning**: Web pages often put important content in `<div>` and `<span>` tags, not just semantic HTML tags. Initial version missed pricing data because it only captured h1-h3, p, and li elements.

#### 2.3 Corpus Loader ([src/corpus.py](../src/corpus.py))
- Loads all .md files from `data/raw/`
- Simple keyword search with relevance scoring
- Snippet extraction with context window

**Critical Configuration**:
```python
max_length=2000  # Increased from 500 to capture full pricing tables
```

#### 2.4 RAG Chatbot ([src/chatbot.py](../src/chatbot.py))
Simple RAG pipeline:
1. Search corpus for relevant documents (top_k=3)
2. Build context from search results
3. Send context + question to OpenAI
4. Return generated answer

**System Prompt**: Instructs GPT to answer only from provided context, be concise and friendly, include contact info when appropriate.

#### 2.5 Streamlit UI ([app.py](../app.py))
- Text input for questions
- Answer display
- Expandable "Source Documents" section for transparency
- Example questions in sidebar
- Cached corpus loading with TTL=60 seconds

### Phase 3: Debugging & Fixes

#### Issue 1: Package Installation
**Problem**: pip install stuck on building grpcio wheel  
**Solution**: Simplified requirements.txt, installed only necessary packages (httpx, beautifulsoup4, python-dotenv, openai, streamlit)

#### Issue 2: OpenAI API Quota
**Problem**: 429 error - billing not set up  
**Solution**: User added payment method to OpenAI account

#### Issue 3: Crawler Missing Content
**Problem**: Crawler only captured navigation menus, not actual content  
**Root Cause**: HTML structure used div/span tags for content  
**Solution**: Enhanced `extract_text()` to include div and span elements

#### Issue 4: Missing Pricing Data
**Problem**: membership-info.md initially created with incomplete data  
**Solution**: Manually created complete file with all 6 membership tiers and pricing

#### Issue 5: Streamlit Cache
**Problem**: Updated data files not loading even after restart  
**Root Cause**: `@st.cache_resource` without TTL cached corpus indefinitely  
**Solution**: Added `ttl=60` parameter to force refresh every 60 seconds

#### Issue 6: Chatbot Can't Answer Pricing Questions (THE BIG ONE)
**Problem**: Despite having correct data, chatbot said "context does not include specific details about membership levels and fees"

**Investigation**:
- ✓ Data exists in membership-info.md with all pricing
- ✓ Corpus loads the file correctly (4 files total)
- ✓ Search finds the membership-info.md document
- ✗ **Snippet extraction only captured 500 characters**

**Root Cause**: 
The `_extract_snippet()` function extracted 500 characters starting from the first occurrence of query words. For "membership levels fees", it found "membership" in the title "# Membership Info" and extracted 500 chars from there. The snippet ended at the introduction paragraph, BEFORE the actual pricing tiers section that started at "## Membership Levels".

**Solution**:
```python
# Changed in src/corpus.py line 60
snippet = self._extract_snippet(
    doc["content"], query_words, max_length=2000  # Was 500
)
```

**Why It Works**:
- membership-info.md is ~2800 characters total
- 2000-char snippet captures intro + all 6 membership tiers with pricing
- Still well within OpenAI's context window limits
- Simple one-line fix, easy to explain

---

## Key Lessons Learned

### 1. RAG Quality = Retrieval Quality × LLM Quality
Even with the best LLM (GPT-4o), if retrieval doesn't capture the right context, the system fails. The LLM was behaving correctly by saying "I don't have that information" when the snippet genuinely didn't include pricing.

### 2. Test the Full Pipeline
We tested individual components (corpus loading ✓, search ✓) but didn't verify the *content* of search results until systematic debugging revealed the snippet was truncated.

### 3. Snippet Length for Structured Data
For documents with structured information (pricing tables, feature lists), conservative snippet lengths may miss critical data that appears after headers/introductions. Either:
- Increase snippet size (our approach)
- Extract multiple snippets from different sections
- Use smarter snippet extraction (find ALL keyword matches, not just first)

### 4. Web Scraping Requires HTML Structure Awareness
Real-world websites don't always use semantic HTML. Important content may be in `<div>`, `<span>`, or other generic elements. Initial scraper only got navigation menus because it expected semantic tags.

### 5. Caching Can Hide Issues
Streamlit's aggressive caching made debugging harder. Always consider cache behavior when data isn't updating as expected.

### 6. Simple is Better for Teaching
- No vector database (Chroma) - just keyword search
- No LangChain framework - manual RAG implementation
- Streamlit instead of React/Next.js
- Local files instead of cloud storage

This makes every component easy to understand and explain to middle/high school students.

---

## Final System Architecture

```
User Question
     ↓
[Streamlit UI] (app.py)
     ↓
[RAG Chatbot] (chatbot.py)
     ↓
[Corpus Search] (corpus.py) → Returns 2000-char snippets
     ↓
[OpenAI GPT-4o] ← Context + Question
     ↓
Answer → [Streamlit UI] → User
```

**Data Flow**:
1. Web Crawler scrapes ACC website → Markdown files
2. Corpus Loader loads all .md files into memory
3. User asks question in Streamlit UI
4. Chatbot searches corpus (keyword search, top 3 results)
5. Each result includes 2000-char snippet with context
6. Context sent to OpenAI with question
7. OpenAI generates answer based on context
8. Answer displayed to user with source documents

---

## Testing & Verification

### Manual Testing
✅ "what are the membership levels and fees in ACC"  
✅ "how much does bronze membership cost"  
✅ "what is the platinum membership fee"  
✅ "what programs does ACC offer"  
✅ "how do I join ACC"

### Automated Testing
Created test suite (`test_comprehensive.py`) with 8 test cases covering:
- Membership pricing questions
- Program inquiries
- Location information
- Contact details

**Result**: All tests pass with correct pricing information in answers

---

## Production Considerations (Future)

For actual deployment beyond workshop demo:

1. **Vector Database**: Use Chroma/Pinecone for semantic search at scale
2. **Better Crawler**: Use Playwright for JavaScript-heavy sites
3. **Conversation Memory**: Track chat history for follow-up questions
4. **Multi-language**: Support Chinese, Korean, Spanish
5. **Analytics**: Track common questions, user satisfaction
6. **FastAPI Backend**: Separate API from frontend
7. **React Frontend**: More professional UI
8. **Authentication**: Secure admin panel for updating content
9. **Rate Limiting**: Prevent API abuse
10. **Monitoring**: Log errors, track costs

---

## Repository Structure

### Source Code
- [src/config.py](../src/config.py) - URLs and crawler settings
- [src/crawler.py](../src/crawler.py) - Web scraping logic
- [src/corpus.py](../src/corpus.py) - Document loading and search
- [src/chatbot.py](../src/chatbot.py) - RAG implementation
- [app.py](../app.py) - Streamlit UI

### Documentation
- [docs/01_problem_statement.md](01_problem_statement.md)
- [docs/02_brainstorming.md](02_brainstorming.md)
- [docs/03_business_requirements.md](03_business_requirements.md)
- [docs/04_product_requirements.md](04_product_requirements.md)
- [docs/05_solution_design.md](05_solution_design.md)
- [docs/fix_summary.md](fix_summary.md) - Detailed debugging analysis
- [docs/development_journey.md](development_journey.md) - This file

### Data
- [data/raw/*.md](../data/raw/) - Crawled ACC website content

---

## How to Run

1. **Setup Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Crawl Data** (optional - data already included):
   ```bash
   python -m src.crawler
   ```

4. **Run Chatbot**:
   ```bash
   streamlit run app.py
   ```

5. **Open Browser**: http://localhost:8501

---

## Workshop Teaching Points

When explaining this project to students:

1. **Start with the problem**: ACC gets same questions over and over
2. **Show the data**: Open membership-info.md, see the pricing tiers
3. **Explain RAG**: Search for relevant info, send to AI, get answer
4. **Demo the crawler**: Show how it turns website into text files
5. **Live demo**: Ask questions, show answers AND sources
6. **Discuss the bug**: Explain how snippet length affected results
7. **Code walkthrough**: Each file is simple and readable

**Key Message**: AI is powerful, but it needs good data retrieval to work well!

---

## Success Metrics

✅ Successfully answers membership fee questions  
✅ Provides accurate program information  
✅ Includes source attribution for transparency  
✅ Simple enough for middle schoolers to understand  
✅ Complete end-to-end demo (crawler → RAG → UI)  
✅ Well-documented for teaching purposes  

---

## Contributors

Built as a coding workshop demo following the ACC problem statement and Software Development Lifecycle guidance.

**Date**: March 2026  
**Purpose**: Educational demo for grades 6-12 coding workshop
