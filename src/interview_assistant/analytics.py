from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class SessionAnalytics:
    confidence_score: float
    key_phrases: List[str]
    roadmap: List[str]


def build_analytics(transcript: List[str]) -> SessionAnalytics:
    joined = " ".join(transcript).lower()
    phrase_bank = ["impact", "trade-off", "scalable", "ownership", "latency", "reliability"]
    found = [p for p in phrase_bank if p in joined]
    score = min(1.0, 0.45 + len(found) * 0.08)
    roadmap = [
        "Use more quantified outcomes (%, $, latency, throughput).",
        "Add one explicit trade-off statement in technical answers.",
        "Close answers with concise result + reflection.",
    ]
    return SessionAnalytics(confidence_score=score, key_phrases=found, roadmap=roadmap)


def write_reports(out_dir: str, analytics: SessionAnalytics) -> None:
    p = Path(out_dir)
    p.mkdir(parents=True, exist_ok=True)

    (p / "report.json").write_text(
        json.dumps(
            {
                "confidence_score": analytics.confidence_score,
                "key_phrases": analytics.key_phrases,
                "improvement_roadmap": analytics.roadmap,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    lines = [
        "Interview Analytics Summary",
        "==========================",
        f"Confidence Score (heuristic): {analytics.confidence_score:.2f}",
        "",
        "Key Phrases:",
        *[f"- {k}" for k in analytics.key_phrases],
        "",
        "Improvement Roadmap:",
        *[f"- {r}" for r in analytics.roadmap],
    ]
    (p / "report.txt").write_text("\n".join(lines), encoding="utf-8")
