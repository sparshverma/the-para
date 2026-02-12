# Safe Interview Assistant Architecture (Compliant Alternative)

I can’t help build software designed to be undetectable in interviews, bypass proctoring, or evade platform security checks.

This document provides a **compliant alternative**: a real-time interview practice and coaching assistant that is transparent, consent-based, and suitable for mock interviews, self-practice, and explicitly authorized assessments.

## 1) Product Scope (Permitted)

Build a cross-platform desktop app (Windows 10+, macOS 11+) that:
- Captures user-authorized audio streams for coaching.
- Provides real-time transcription and response suggestions.
- Uses user-provided resume/JD documents for grounded guidance.
- Surfaces coding hints in practice mode for supported coding platforms.
- Produces post-session analytics.

## 2) Explicit Non-Goals (Security & Ethics Guardrails)

- No stealth overlays hidden from capture APIs.
- No process renaming/obfuscation intended to evade monitors.
- No bypass of proctoring or active-window detection.
- No covert use during real evaluations without explicit permission.

## 3) High-Level Architecture

### Desktop Client
- **Framework**: Tauri (Rust core + lightweight web UI) or Electron if needed.
- **Rendering**: Always-visible, user-toggleable HUD with clear app watermark.
- **Capture Permissions**:
  - Microphone via OS permission prompts.
  - Optional system audio via approved loopback APIs/drivers only after user consent.

### Streaming Pipeline
1. Audio chunking (20–40 ms frames).
2. Voice activity detection (VAD).
3. Streaming STT (Whisper-large-v3-turbo, Parakeet, or cloud STT).
4. Language identification + dynamic prompt locale.
5. LLM response generation (bullet-format guidance).
6. UI render with latency telemetry.

### RAG Layer
- File ingestion: PDF/DOCX parser.
- Chunking + embeddings + vector index (e.g., FAISS/LanceDB).
- Retrieval policy prioritizing resume facts + role requirements.
- Prompt templates enforcing factual grounding and concise speaking points.

### Coding Practice Module
- OCR on user-selected region only.
- Detects code blocks/problem statements in practice mode.
- Returns:
  - Clarifying steps.
  - Candidate-friendly hints.
  - Complexity notes (time/space).

## 4) Performance Targets (Compliant)

- STT partial latency target: < 500 ms where hardware/network allow.
- End-to-end first guidance target: ≤ 1.2 s on “speed mode” with streaming decode.
- Graceful degradation strategy:
  - Lower context window.
  - Smaller model fallback.
  - Progressive bullet rendering.

## 5) Privacy & Data Handling

- Session-scoped memory by default.
- Transcripts/embeddings deleted at session end unless user opts in to save.
- Encryption in transit (TLS) and at rest when persistence is enabled.
- Local-only mode option for sensitive interviews.

## 6) Model Orchestration

Expose user-selectable modes:
- **Fast Mode**: lower-latency model for instant prompts.
- **Reasoning Mode**: stronger model for complex questions.

Router policy:
- Behavioral question -> fast mode default.
- System design / algorithmic multi-step -> reasoning mode.
- User override always available.

## 7) UX Deliverables

### Live HUD
- Left: real-time transcript.
- Right: 3–5 grounded bullet points (natural phrasing).
- Footer: “Practice Mode” indicator + latency meter.

### Technical Sidebar
- Appears only in coding practice mode.
- Shows approach, edge cases, and O() complexity hints.

### Post-Session Report (PDF)
- Question themes.
- Suggested improvements.
- Confidence trend (clearly labeled as heuristic).
- Key phrase usage summary.

### Personalization Indicator
- Dashboard badge: “Resume context loaded” + source doc names.

## 8) Suggested Implementation Plan

1. Build desktop shell + permission flows.
2. Add streaming STT with partial hypotheses.
3. Implement RAG ingestion for resume/JD.
4. Add LLM bullet-point responder with guardrails.
5. Add OCR practice sidebar.
6. Add report generator.
7. Add observability (latency, error rate, token usage).
8. Security review and policy compliance checks.

## 9) Validation Checklist

- User consent prompts appear before any capture.
- App visible in task switcher and screen capture.
- No anti-detection code paths.
- PII retention policy enforced and tested.
- Latency SLO dashboard instrumented.

