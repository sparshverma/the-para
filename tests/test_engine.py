from interview_assistant.engine import InterviewAssistantEngine
from interview_assistant.models import DocumentChunk, InterviewMode
from interview_assistant.retrieval import SimpleVectorIndex


def test_engine_returns_grounded_bullets():
    chunks = [
        DocumentChunk(source="resume.txt", text="Optimized service latency and improved reliability."),
        DocumentChunk(source="jd.txt", text="Need Python backend engineer with ownership."),
    ]
    index = SimpleVectorIndex(chunks)

    engine = InterviewAssistantEngine()
    engine.start_session("s1", mode=InterviewMode.FAST)
    result = engine.handle_turn("s1", "How did you reduce latency?", index)

    assert result.bullets
    assert "resume.txt" in result.context_sources


def test_mode_switch_to_reasoning_produces_longer_structure():
    chunks = [DocumentChunk(source="resume.txt", text="Designed distributed systems.")]
    index = SimpleVectorIndex(chunks)
    engine = InterviewAssistantEngine()
    engine.start_session("s2", mode=InterviewMode.FAST)
    engine.set_mode("s2", InterviewMode.REASONING)
    result = engine.handle_turn("s2", "Design a scalable queue.", index)

    assert result.mode == InterviewMode.REASONING
    assert len(result.bullets) >= 4
