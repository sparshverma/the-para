from __future__ import annotations

from .models import GuidanceResult, InterviewMode, SessionState
from .orchestrator import ModelOrchestrator
from .privacy import PrivacySessionStore
from .retrieval import SimpleVectorIndex


class InterviewAssistantEngine:
    def __init__(self, session_store: PrivacySessionStore | None = None):
        self.sessions = session_store or PrivacySessionStore()

    def start_session(self, session_id: str, mode: InterviewMode = InterviewMode.FAST) -> SessionState:
        session = SessionState(session_id=session_id, mode=mode)
        self.sessions.create(session)
        return session

    def set_mode(self, session_id: str, mode: InterviewMode) -> None:
        session = self.sessions.get(session_id)
        session.mode = mode

    def handle_turn(self, session_id: str, interviewer_text: str, index: SimpleVectorIndex) -> GuidanceResult:
        session = self.sessions.get(session_id)
        session.transcript.append(interviewer_text)

        context = index.search(interviewer_text, k=3)
        session.retrieved_context = context

        orchestrator = ModelOrchestrator(mode=session.mode)
        bullets = orchestrator.generate_bullets(
            question=interviewer_text,
            context=[c.text for c in context],
        )

        return GuidanceResult(
            transcript_line=interviewer_text,
            bullets=bullets,
            mode=session.mode,
            context_sources=[c.source for c in context],
        )

    def end_session(self, session_id: str) -> None:
        self.sessions.end_session(session_id)
