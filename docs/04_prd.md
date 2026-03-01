# Product Requirements Document (PRD)

## Feature List

### Core Features (MVP)

1. **Web Crawler**
   - Crawl specified ACC website pages
   - Extract text content (paragraphs, headings, lists)
   - Save as markdown files for easy inspection

2. **Vector Database**
   - Store crawled content in Chroma (local)
   - Enable semantic search over content
   - Chunk documents appropriately (~500 tokens)

3. **RAG Chatbot**
   - Accept user questions via text input
   - Retrieve relevant context from vector DB
   - Generate answers using OpenAI LLM
   - Cite sources when possible

4. **Streamlit UI**
   - Simple chat interface
   - Text input box for questions
   - Display bot responses clearly
   - Show "thinking" indicator while processing

### Nice-to-Have (Future)

- Conversation history within session
- "I don't know" responses for out-of-scope questions
- Admin panel to re-crawl content

## User Stories

### Story 1: Prospective Member
**As a** prospective member  
**I want to** ask "How much does membership cost?"  
**So that** I can quickly understand pricing without emailing staff

**Acceptance Criteria:**
- Bot responds in < 5 seconds
- Answer includes membership fee details from website
- Answer is factually accurate

---

### Story 2: Community Member
**As a** community member  
**I want to** ask "What programs does ACC offer?"  
**So that** I can learn about available services

**Acceptance Criteria:**
- Bot retrieves relevant program information
- Lists multiple programs if available
- Response is clear and organized

---

### Story 3: Current Member
**As a** current member  
**I want to** ask "Where is ACC located?"  
**So that** I can find the physical address quickly

**Acceptance Criteria:**
- Bot provides accurate address
- Response includes any relevant location details (parking, transit, etc.)

## Functional Requirements

### FR-1: Web Crawling
- System shall crawl specified URL list
- System shall extract text content from HTML
- System shall save content as markdown files
- System shall respect robots.txt (if present)

### FR-2: Content Storage
- System shall chunk documents into ~500 token segments
- System shall create embeddings using OpenAI
- System shall store embeddings in Chroma database
- System shall enable semantic similarity search

### FR-3: Question Answering
- System shall accept text questions from users
- System shall retrieve top 3-5 most relevant chunks
- System shall pass context + question to LLM
- System shall return generated answer to user

### FR-4: User Interface
- System shall provide chat interface via Streamlit
- UI shall display user questions and bot responses
- UI shall handle loading states gracefully
- UI shall be usable on laptop screens

## Non-Functional Requirements

### NFR-1: Performance
- Response time < 5 seconds for typical questions
- Crawler should process pages at reasonable rate (respect rate limits)

### NFR-2: Accuracy
- Answers must be grounded in crawled content
- No hallucinated facts
- If answer not found, bot should indicate uncertainty

### NFR-3: Usability
- Code must be readable by grade 6-12 students
- UI must be intuitive (no training required)
- Error messages must be clear

### NFR-4: Maintainability
- Code should be modular (separate crawler, retriever, chatbot)
- Clear comments explaining "why"
- Requirements.txt for dependencies

## Acceptance Criteria (Overall)

**Definition of Done for MVP:**
- [ ] Crawler successfully retrieves content from ≥5 ACC pages
- [ ] Content is stored in vector database
- [ ] User can ask questions via Streamlit UI
- [ ] Bot provides relevant answers to 10 test questions
- [ ] README explains how to run the system
- [ ] Code is well-commented and explainable

## Edge Cases

1. **Question not in data:**
   - Bot should respond: "I don't have information about that. Please contact ACC directly."

2. **Vague question:**
   - Example: "Tell me about ACC"
   - Bot should provide general overview from About page

3. **Crawler fails on a page:**
   - Log error, continue with other pages

4. **Multiple similar pages:**
   - Retriever may return redundant chunks
   - LLM should synthesize information

5. **Very long response:**
   - Limit LLM output to reasonable length (~300 words)
