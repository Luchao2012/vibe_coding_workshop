"""Load and manage the ACC knowledge corpus.

This module reads all markdown files and provides search functionality.
Keep it simple for workshop clarity.
"""

from __future__ import annotations

from pathlib import Path


class Corpus:
    """Simple in-memory corpus of ACC knowledge."""

    def __init__(self, raw_data_dir: str = "data/raw"):
        """Load all markdown files from the directory."""
        self.raw_data_dir = Path(raw_data_dir)
        self.documents: list[dict[str, str]] = []
        self._load_documents()

    def _load_documents(self) -> None:
        """Load all .md files from raw_data_dir."""
        if not self.raw_data_dir.exists():
            print(f"Warning: {self.raw_data_dir} does not exist")
            return

        for file_path in sorted(self.raw_data_dir.glob("*.md")):
            try:
                content = file_path.read_text(encoding="utf-8")
                # Extract friendly name from filename
                name = file_path.stem.replace("asianchamber-hou.org_", "").replace("-", " ")
                self.documents.append(
                    {
                        "name": name,
                        "filename": file_path.name,
                        "content": content,
                    }
                )
                print(f"✓ Loaded: {file_path.name}")
            except Exception as exc:
                print(f"✗ Failed to load {file_path.name}: {exc}")

    def search(self, query: str, top_k: int = 3) -> list[str]:
        """Simple keyword search.

        Returns the top_k most relevant document chunks.
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())

        results = []
        for doc in self.documents:
            content_lower = doc["content"].lower()

            # Count matching words
            matches = sum(1 for word in query_words if word in content_lower)

            if matches > 0:
                # Extract a relevant snippet (increase to 2000 to capture full pricing tables)
                snippet = self._extract_snippet(
                    doc["content"], query_words, max_length=2000
                )
                results.append(
                    {
                        "source": doc["name"],
                        "content": snippet,
                        "score": matches,
                    }
                )

        # Sort by score (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    @staticmethod
    def _extract_snippet(
        text: str, query_words: set[str], max_length: int = 500
    ) -> str:
        """Extract a relevant snippet from text."""
        text_lower = text.lower()

        # Find first occurrence of any query word
        best_pos = len(text)
        for word in query_words:
            pos = text_lower.find(word)
            if pos != -1 and pos < best_pos:
                best_pos = pos

        # Extract window around first match
        if best_pos == len(text):
            # No match found, return beginning
            return text[:max_length]

        start = max(0, best_pos - 100)
        end = min(len(text), start + max_length)
        snippet = text[start:end]

        # Clean up
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."

        return snippet.strip()

    def get_all_content(self) -> str:
        """Get all content as a single string (for fallback)."""
        return "\n\n".join([f"## {doc['name']}\n\n{doc['content']}" 
                            for doc in self.documents])
