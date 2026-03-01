"""Streamlit UI for the ACC Admin Helper Chatbot."""

from __future__ import annotations

import streamlit as st

from src.chatbot import get_rag_response
from src.corpus import Corpus


def main() -> None:
    """Main Streamlit app."""
    st.set_page_config(page_title="ACC Admin Helper", layout="wide")

    st.title("🏢 ACC Admin Helper Chatbot")
    st.markdown(
        "Ask questions about the Asian Chamber of Commerce — membership, programs, and more!"
    )

    # Initialize corpus (cached with TTL to reload periodically)
    @st.cache_resource(ttl=60)  # Reload every 60 seconds
    def load_corpus() -> Corpus:
        with st.spinner("Loading ACC knowledge base..."):
            return Corpus("data/raw")

    corpus = load_corpus()

    # Display status
    st.success(f"✓ Loaded {len(corpus.documents)} pages from ACC website")

    # Chat interface
    st.subheader("Ask a Question")

    user_question = st.text_input(
        "Your question:",
        placeholder="e.g., How much does membership cost? What programs do you offer?",
    )

    if user_question:
        with st.spinner("Searching and generating answer..."):
            answer = get_rag_response(user_question, corpus)

        st.subheader("Answer")
        st.write(answer)

        # Show search results (for transparency)
        with st.expander("📄 Source Documents"):
            results = corpus.search(user_question, top_k=3)
            if results:
                for i, result in enumerate(results, 1):
                    st.markdown(f"**{i}. {result['source']}**")
                    st.text(result["content"][:300] + "...")
            else:
                st.info("No relevant documents found.")

    # Example questions
    st.sidebar.subheader("Example Questions")
    examples = [
        "How much does membership cost?",
        "What programs does ACC offer?",
        "What are the benefits of being a member?",
        "How do I join ACC?",
        "What is the Asian Chamber of Commerce?",
        "Where is ACC located?",
    ]

    for example in examples:
        if st.sidebar.button(example, key=example):
            st.rerun()

    # Help section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About this chatbot")
    st.sidebar.info(
        "This is a demo chatbot that answers questions based on ACC's website content. "
        "For complex inquiries, please contact ACC directly: info@asianchamber-hou.org"
    )


if __name__ == "__main__":
    main()
