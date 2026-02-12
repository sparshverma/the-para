from __future__ import annotations

from typing import List

from .models import InterviewMode


class ModelOrchestrator:
    """Lightweight mode router for fast vs reasoning behavior."""

    def __init__(self, mode: InterviewMode = InterviewMode.FAST):
        self.mode = mode

    def set_mode(self, mode: InterviewMode) -> None:
        self.mode = mode

    def generate_bullets(self, question: str, context: List[str]) -> List[str]:
        context_line = context[0] if context else "No matching resume/JD context found."

        if self.mode == InterviewMode.FAST:
            return [
                f"Start with a direct 1-sentence answer to: '{question[:90]}'",
                "Add one concrete result with metric (impact, scale, or speed).",
                f"Ground with your background: {context_line[:120]}",
            ]

        return [
            "State your assumptions and the goal before details.",
            f"Break response into 2-3 steps tailored to: '{question[:80]}'.",
            "Call out trade-offs and why your choice is practical.",
            f"Connect to your prior experience: {context_line[:120]}",
            "Close with measurable outcome and a follow-up question.",
        ]
