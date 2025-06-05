from __future__ import annotations
from typing import List
from google.adk.agents.base_agent import BaseAgent
from google.adk.events.event import Event
from google.adk.agents.invocation_context import InvocationContext
from google.genai.types import Content, Part
import faiss
import numpy as np

class RagAgent(BaseAgent):
    """Simple retrieval augmented generation using a FAISS index and Vertex AI."""

    documents: List[str] = []
    dimension: int = 384  # embedding dimension placeholder
    index: faiss.IndexFlatIP | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.documents:
            self._build_index()

    def _embed(self, texts: List[str]) -> np.ndarray:
        # Dummy embedding using hash for deterministic vectors
        vecs = [np.array([hash(t) % 1000 for _ in range(self.dimension)], dtype='float32') for t in texts]
        return np.vstack(vecs)

    def _build_index(self) -> None:
        vectors = self._embed(self.documents)
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(vectors)

    async def _run_async_impl(self, ctx: InvocationContext):
        query = ctx.session_state.get('query') or ''
        if not self.index:
            yield Event(invocation_id=ctx.invocation_id, author=self.name,
                        content=Content(role='assistant', parts=[Part(text='No index available')]))
            return
        q_vec = self._embed([query])
        scores, ids = self.index.search(q_vec, 1)
        doc = self.documents[ids[0][0]] if ids.size and ids[0][0] != -1 else ''
        # This would normally call Vertex AI with the retrieved context.
        answer = f"Based on: {doc}\nAnswer to '{query}'"
        yield Event(invocation_id=ctx.invocation_id, author=self.name,
                    content=Content(role='assistant', parts=[Part(text=answer)]))

__all__ = ["RagAgent"]
