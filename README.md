# Interview Assistant (Compliant Prototype)

This repository contains a **safe** implementation prototype for a real-time interview coaching assistant intended for:
- mock interviews,
- self-practice,
- explicitly authorized support scenarios.

It intentionally excludes stealth, anti-detection, and proctoring-bypass features.

## Implemented components

- Session privacy manager with automatic purge behavior.
- Resume/JD ingestion for TXT/PDF/DOCX (PDF/DOCX support optional via local libraries).
- Lightweight retrieval layer (token cosine similarity).
- Prompt-building and response formatting into natural bullet points.
- Model orchestration toggle (`fast` / `reasoning`).
- Coding-sidebar analyzer for practice-mode code/problem text detection.
- Post-session analytics and report generation (JSON + text summary).

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m interview_assistant.demo
```

## Testing

```bash
pip install pytest
pytest
```
