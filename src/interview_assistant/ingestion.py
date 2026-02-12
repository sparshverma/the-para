from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from .models import DocumentChunk


class DocumentIngestionError(RuntimeError):
    pass


def _read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError as exc:
        raise DocumentIngestionError("Install pypdf for PDF support.") from exc

    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _read_docx(path: Path) -> str:
    try:
        import docx  # type: ignore
    except ImportError as exc:
        raise DocumentIngestionError("Install python-docx for DOCX support.") from exc

    doc = docx.Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs)


def load_document(path: str) -> str:
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".txt":
        return _read_txt(p)
    if suffix == ".pdf":
        return _read_pdf(p)
    if suffix == ".docx":
        return _read_docx(p)
    raise DocumentIngestionError(f"Unsupported extension: {suffix}")


def chunk_text(text: str, source: str, chunk_size: int = 450) -> List[DocumentChunk]:
    words = text.split()
    chunks: List[DocumentChunk] = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk.strip():
            chunks.append(DocumentChunk(source=source, text=chunk))
    return chunks


def ingest_documents(paths: Iterable[str]) -> List[DocumentChunk]:
    all_chunks: List[DocumentChunk] = []
    for path in paths:
        text = load_document(path)
        all_chunks.extend(chunk_text(text=text, source=path))
    return all_chunks
