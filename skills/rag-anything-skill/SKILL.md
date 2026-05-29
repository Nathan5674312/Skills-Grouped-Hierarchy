---
name: rag-anything
description: Multimodal RAG ingestion and retrieval over mixed documents (text, images, scanned PDFs, tables, equations). Use when the user wants to build a knowledge base from rich documents, query across images + text together, ingest scanned PDFs, or set up retrieval-augmented generation that is not text-only. Wraps the open-source RAG-Anything framework (HKUDS), built on LightRAG.
---

# RAG-Anything

Multimodal RAG. Ingests text, images, scanned PDFs, tables, equations into one knowledge graph, queries across all of them. This is a Python framework, not a drop-in prompt skill: it runs as code.

## Setup
```bash
pip install raganything
```
Needs an LLM API key and (for scanned docs) MinerU for extraction. See repo docs.

## Minimal use
```python
from raganything import RAGAnything
rag = RAGAnything(working_dir="./kb")
await rag.aprocess_document("scanned_report.pdf")   # ingests text+images+tables
result = await rag.aquery("compare the chart on p.3 with the conclusion")
```

## When to reach for it
- Documents where evidence spans modalities (diagram + caption + table).
- Scanned PDFs that text-only RAG fails on.
- Academic papers, financial reports, technical manuals.

## Repo
https://github.com/HKUDS/RAG-Anything  — full docs in its README and docs/ folder (batch processing, offline setup, failure modes).
