from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class TechnicalHint:
    detected: bool
    hints: List[str]


CODE_SIGNAL = re.compile(r"\b(def|class|for|while|if|return|public|private|function|=>)\b")


def detect_and_hint(region_text: str) -> TechnicalHint:
    if not CODE_SIGNAL.search(region_text):
        return TechnicalHint(detected=False, hints=[])

    hints = [
        "Restate input/output and constraints before coding.",
        "Start with brute force, then optimize bottlenecks.",
        "Track edge cases (empty input, duplicates, bounds).",
        "State complexity target explicitly (e.g., O(n), O(n log n)).",
    ]
    return TechnicalHint(detected=True, hints=hints)
