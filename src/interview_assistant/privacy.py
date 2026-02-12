from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict

from .models import SessionState


@dataclass
class PrivacySessionStore:
    """In-memory, session-scoped store with explicit purge semantics."""

    sessions: Dict[str, SessionState] = field(default_factory=dict)
    created_at: Dict[str, datetime] = field(default_factory=dict)

    def create(self, session: SessionState) -> None:
        self.sessions[session.session_id] = session
        self.created_at[session.session_id] = datetime.now(timezone.utc)

    def get(self, session_id: str) -> SessionState:
        return self.sessions[session_id]

    def end_session(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)
        self.created_at.pop(session_id, None)

    def purge_all(self) -> None:
        self.sessions.clear()
        self.created_at.clear()
