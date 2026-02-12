from __future__ import annotations

from interview_assistant.analytics import build_analytics, write_reports
from interview_assistant.engine import InterviewAssistantEngine
from interview_assistant.models import DocumentChunk, InterviewMode
from interview_assistant.retrieval import SimpleVectorIndex
from interview_assistant.technical_sidebar import detect_and_hint


def main() -> None:
    chunks = [
        DocumentChunk(
            source="resume.txt",
            text="Built a low-latency analytics service that reduced p95 latency by 37% and improved reliability.",
        ),
        DocumentChunk(
            source="job_description.txt",
            text="Seeking backend engineer with Python, distributed systems, and strong ownership mindset.",
        ),
    ]
    index = SimpleVectorIndex(chunks)

    engine = InterviewAssistantEngine()
    engine.start_session("demo", mode=InterviewMode.FAST)

    q1 = "Tell me about a project where you improved system performance."
    result = engine.handle_turn("demo", q1, index)

    print("Transcript:", result.transcript_line)
    print("Bullets:")
    for b in result.bullets:
        print(" -", b)

    tech = detect_and_hint("def two_sum(nums, target):\n    pass")
    if tech.detected:
        print("\nTechnical Sidebar:")
        for h in tech.hints:
            print(" -", h)

    analytics = build_analytics([q1, "I discussed trade-off decisions and reliability impact."])
    write_reports("artifacts", analytics)

    engine.end_session("demo")


if __name__ == "__main__":
    main()
