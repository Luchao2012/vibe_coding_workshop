# Brainstorming

## Possible Data Sources

**Primary source (for MVP):**
- ACC's existing website — crawl pages containing:
  - Membership information
  - Fee structures
  - Benefits and programs
  - Contact information
  - About pages

**Future sources (out of scope for MVP):**
- PDF documents (annual reports, brochures)
- Existing FAQ databases
- Staff-created knowledge base articles

## Example User Questions

**Membership:**
- "How much does membership cost?"
- "What are the benefits of joining?"
- "How do I become a member?"
- "Is there a family membership option?"

**Programs:**
- "What events does ACC organize?"
- "Are there youth programs?"
- "What services do you provide?"

**General:**
- "What is ACC?"
- "Where are you located?"
- "What are your hours?"

## What is MVP (Minimum Viable Product)?

**MVP scope:**
- Crawl ACC website (5-10 key pages)
- Store content in a local vector database (Chroma)
- Build RAG chatbot using LangChain + OpenAI
- Simple Streamlit UI where users can ask questions
- Get relevant answers based on website content

**Success = one functional end-to-end demo**

## Future Scope (not for initial workshop)

- Multi-language support (e.g., Chinese, Korean)
- Integration with ACC's actual website
- Conversation history/memory
- Escalation to human staff for complex questions
- Analytics dashboard (track common questions)
- PDF document ingestion

## Out of Scope

- Handling transactions (payments, registrations)
- Personal account information
- Booking systems
- Real-time database queries
- Production deployment
- Mobile app

## Risks & Constraints

**Risks:**
- Website structure may change → crawler breaks
- LLM may hallucinate information not in the data
- Rate limits on crawling
- API costs (OpenAI calls)

**Constraints:**
- Workshop timeframe: must be completable in 2-3 hours
- Audience: kids (grade 6-12), so code must be simple
- Budget: minimal API costs
- No access to ACC's internal databases
