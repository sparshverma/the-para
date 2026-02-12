from interview_assistant.privacy import PrivacySessionStore
from interview_assistant.models import SessionState
from interview_assistant.technical_sidebar import detect_and_hint


def test_session_purge():
    store = PrivacySessionStore()
    store.create(SessionState(session_id="abc"))
    assert store.get("abc").session_id == "abc"
    store.end_session("abc")
    assert "abc" not in store.sessions


def test_technical_hint_detection():
    hit = detect_and_hint("for i in range(n): return i")
    miss = detect_and_hint("please introduce yourself")

    assert hit.detected is True
    assert len(hit.hints) > 0
    assert miss.detected is False
