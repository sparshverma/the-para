from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class InterviewMode(str, Enum):
    FAST = "fast"
    REASONING = "reasoning"


@dataclass
class DocumentChunk:
    source: str
    text: str


@dataclass
class SessionState:
    session_id: str
    mode: InterviewMode = InterviewMode.FAST
    transcript: List[str] = field(default_factory=list)
    retrieved_context: List[DocumentChunk] = field(default_factory=list)


@dataclass
class GuidanceResult:
    transcript_line: str
    bullets: List[str]
    mode: InterviewMode
    context_sources: List[str]
