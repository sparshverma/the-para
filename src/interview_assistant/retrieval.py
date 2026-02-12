from __future__ import annotations

import math
import re
from collections import Counter
from typing import List

from .models import DocumentChunk

TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


def _cosine(a: Counter, b: Counter) -> float:
    common = set(a) & set(b)
    num = sum(a[t] * b[t] for t in common)
    da = math.sqrt(sum(v * v for v in a.values()))
    db = math.sqrt(sum(v * v for v in b.values()))
    if da == 0 or db == 0:
        return 0.0
    return num / (da * db)


class SimpleVectorIndex:
    def __init__(self, chunks: List[DocumentChunk]):
        self.chunks = chunks
        self.embeddings = [Counter(_tokenize(c.text)) for c in chunks]

    def search(self, query: str, k: int = 3) -> List[DocumentChunk]:
        q = Counter(_tokenize(query))
        scored = [(_cosine(q, emb), i) for i, emb in enumerate(self.embeddings)]
        scored.sort(reverse=True)
        return [self.chunks[i] for score, i in scored[:k] if score > 0]
