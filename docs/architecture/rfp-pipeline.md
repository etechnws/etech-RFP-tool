# RFP Response Pipeline Architecture

## Purpose and Scope
This document defines a production-ready architecture for generating high-quality RFP response drafts from approved enterprise content, with explicit source citations and a human approval gate.

Goals:
- Improve response speed while preserving quality and compliance.
- Ensure every generated claim is traceable to approved sources.
- Enable progressive delivery from deterministic foundations to AI-assisted drafting and workflow automation.

---

## End-to-End Pipeline Overview

1. **Document ingestion + OCR**
   - Ingest source documents (PDF, DOCX, PPTX, HTML, plaintext, scanned images).
   - Extract text and structure (headings, tables, page numbers).
   - Run OCR for image/scanned content and normalize text.
   - Store canonical document objects and chunked passages.

2. **Structured question extraction**
   - Parse RFP package and identify sections, questions, sub-questions, constraints, and due dates.
   - Normalize questions into a machine-readable schema with stable IDs.
   - Flag ambiguous or malformed questions for manual triage.

3. **Retrieval over approved content (vector + keyword)**
   - Hybrid retrieval over only approved/whitelisted corpora.
   - Combine lexical search (BM25/keyword) and semantic ANN vector search.
   - Re-rank and deduplicate results, then package evidence sets per question.

4. **Draft generation with source citations**
   - Generate draft answers grounded in retrieved evidence.
   - Require inline citation references and per-answer citation metadata.
   - Reject or down-rank unsupported statements.

5. **Human review/approval workflow**
   - Assign drafts to reviewers/SMEs.
   - Track edits, approvals, rejections, and rationale.
   - Export approved final responses with audit trail.

---

## Service Boundaries and Interfaces

Each module is an independently deployable service with explicit input/output contracts.
JSON Schema-like definitions below are normative at the API boundary.

### 1) Ingestion + OCR Service

**Responsibility**
- Convert raw files into canonical text + structured chunks with provenance.

**Inputs**
```json
{
  "ingestion_job_id": "string",
  "documents": [
    {
      "document_id": "string",
      "filename": "string",
      "mime_type": "application/pdf|...",
      "storage_uri": "string",
      "approved": true,
      "metadata": {
        "owner": "string",
        "effective_date": "YYYY-MM-DD",
        "tags": ["string"]
      }
    }
  ]
}
```

**Outputs**
```json
{
  "ingestion_job_id": "string",
  "status": "completed|partial|failed",
  "documents": [
    {
      "document_id": "string",
      "text_blocks": [
        {
          "block_id": "string",
          "text": "string",
          "page": 1,
          "section_path": ["Executive Summary", "Security"],
          "char_start": 0,
          "char_end": 512,
          "ocr_confidence": 0.97
        }
      ],
      "chunks": [
        {
          "chunk_id": "string",
          "text": "string",
          "token_count": 220,
          "source_block_ids": ["string"],
          "citation": {
            "document_id": "string",
            "page": 1,
            "section_path": ["string"]
          }
        }
      ],
      "errors": []
    }
  ]
}
```

### 2) Structured Question Extraction Service

**Responsibility**
- Transform RFP text/files into normalized question objects and requirements.

**Inputs**
```json
{
  "rfp_id": "string",
  "documents": [{ "document_id": "string", "storage_uri": "string" }],
  "extraction_mode": "deterministic|assisted"
}
```

**Outputs**
```json
{
  "rfp_id": "string",
  "questions": [
    {
      "question_id": "Q-1.2.3",
      "section": "Technical Requirements",
      "prompt": "Describe your incident response process.",
      "sub_prompts": ["Escalation timelines", "Communication channels"],
      "constraints": {
        "max_words": 300,
        "must_include": ["24/7"],
        "format": "narrative|table|yes_no"
      },
      "due_date": "YYYY-MM-DD",
      "priority": "high|medium|low",
      "ambiguity_flags": []
    }
  ],
  "unparsed_segments": ["string"]
}
```

### 3) Retrieval Service (Hybrid Vector + Keyword)

**Responsibility**
- Retrieve and rank approved evidence chunks for each question.

**Inputs**
```json
{
  "rfp_id": "string",
  "question_id": "string",
  "query": "string",
  "filters": {
    "approved_only": true,
    "tags": ["security", "product"],
    "effective_after": "YYYY-MM-DD"
  },
  "top_k": 20
}
```

**Outputs**
```json
{
  "question_id": "string",
  "retrieval_id": "string",
  "results": [
    {
      "chunk_id": "string",
      "document_id": "string",
      "score_vector": 0.82,
      "score_keyword": 12.4,
      "score_fused": 0.91,
      "snippet": "string",
      "citation": {
        "document_id": "string",
        "page": 14,
        "section_path": ["Security", "Incident Response"]
      }
    }
  ],
  "coverage": {
    "result_count": 20,
    "distinct_documents": 5,
    "low_evidence": false
  }
}
```

### 4) Draft Generation Service

**Responsibility**
- Produce grounded answer drafts using only provided evidence and return citation links.

**Inputs**
```json
{
  "rfp_id": "string",
  "question": {
    "question_id": "string",
    "prompt": "string",
    "constraints": {}
  },
  "evidence": [
    {
      "chunk_id": "string",
      "snippet": "string",
      "citation": { "document_id": "string", "page": 1 }
    }
  ],
  "generation_mode": "template|llm",
  "citation_required": true
}
```

**Outputs**
```json
{
  "question_id": "string",
  "draft_id": "string",
  "answer_markdown": "We provide 24/7 monitoring [C1]...",
  "citations": [
    {
      "citation_id": "C1",
      "chunk_id": "string",
      "document_id": "string",
      "page": 1,
      "quote": "string"
    }
  ],
  "quality_signals": {
    "citation_coverage": 0.95,
    "unsupported_claims": 0,
    "constraint_violations": []
  }
}
```

### 5) Human Review & Approval Service

**Responsibility**
- Orchestrate assignments, editing, approval lifecycle, and auditability.

**Inputs**
```json
{
  "rfp_id": "string",
  "drafts": [{ "question_id": "string", "draft_id": "string" }],
  "workflow": {
    "reviewers": ["user_123"],
    "required_approvals": 1,
    "sla_hours": 48
  }
}
```

**Outputs**
```json
{
  "rfp_id": "string",
  "review_status": "in_review|approved|changes_requested|rejected",
  "items": [
    {
      "question_id": "string",
      "draft_id": "string",
      "decision": "approved|changes_requested|rejected",
      "reviewer_edits": [
        {
          "editor_id": "string",
          "timestamp": "ISO-8601",
          "edit_type": "insert|delete|replace",
          "delta_chars": 42,
          "reason": "Tone refinement"
        }
      ],
      "comments": ["string"]
    }
  ],
  "audit_log_uri": "string"
}
```

---

## Telemetry and Observability Requirements

Telemetry is mandatory and emitted per stage, per question, and per RFP.

### Core KPIs

1. **Latency**
   - Ingestion latency (p50/p95/p99)
   - Extraction latency per question
   - Retrieval latency per query
   - Draft generation latency per question
   - End-to-end time from upload to approval

2. **Retrieval hit-rate and quality**
   - Hit-rate@k (e.g., at least one relevant chunk in top-k)
   - nDCG/MRR on labeled evaluation sets
   - Low-evidence rate (questions with insufficient grounding)

3. **Citation coverage**
   - Percentage of sentences/claims with at least one citation
   - Unsupported-claim rate detected by validators
   - Citation precision (human spot-check sampling)

4. **Reviewer edits and acceptance**
   - Edit distance between draft and approved answer
   - Reviewer edit rate by section/question type
   - First-pass approval rate
   - Time in review + SLA breach rate

### Event Contract (example)

```json
{
  "event_name": "draft_generated",
  "timestamp": "ISO-8601",
  "rfp_id": "string",
  "question_id": "string",
  "service": "draft-generation",
  "latency_ms": 1840,
  "metrics": {
    "citation_coverage": 0.92,
    "unsupported_claims": 1,
    "retrieval_hit": true
  },
  "trace_id": "string"
}
```

### Operational Requirements
- Correlate logs/metrics/traces using `trace_id` and `rfp_id`.
- Persist immutable audit records for approved submissions.
- Alert on regression thresholds (e.g., citation coverage < 90%, p95 latency > target).

---

## Incremental Implementation Plan

### Phase 1 — Deterministic extraction + retrieval

**Scope**
- Rule-based parsing for question extraction.
- OCR + text normalization pipeline.
- Hybrid retrieval with deterministic ranking/fusion.
- No generative drafting yet (template assembly only).

**Deliverables**
- Stable schemas and APIs for ingestion, extraction, retrieval.
- Gold evaluation set for retrieval and extraction QA.
- Baseline dashboard for latency + hit-rate.

**Exit Criteria**
- ≥ target extraction accuracy on validation set.
- ≥ target hit-rate@k for priority question categories.
- End-to-end deterministic answer assembly available for pilot users.

### Phase 2 — AI drafting with citations

**Scope**
- LLM drafting constrained to retrieved evidence.
- Citation binding/validation and unsupported-claim checks.
- Draft quality scoring and fallback to deterministic templates.

**Deliverables**
- Draft Generation Service in `llm` mode.
- Citation validator and policy guardrails.
- Reviewer UI support for citation inspection.

**Exit Criteria**
- Citation coverage above threshold (e.g., ≥ 90%).
- Unsupported-claim rate below threshold.
- Measurable reduction in reviewer editing effort vs. Phase 1.

### Phase 3 — Workflow automation and collaboration

**Scope**
- Full assignment routing, approvals, reminders, escalations.
- Collaboration features (comments, version diffs, role-based access).
- Integration with CRM/proposal systems for package export.

**Deliverables**
- End-to-end orchestration across services.
- SLA monitoring and automated notifications.
- Complete audit trail with compliance exports.

**Exit Criteria**
- End-to-end cycle time reduction meets business target.
- First-pass approval rate reaches agreed target.
- Compliance/audit requirements pass stakeholder review.

---

## Non-Functional Requirements

- **Security:** approved-content allowlist, RBAC, encryption at rest/in transit.
- **Reliability:** idempotent processing, retry policies, dead-letter queues.
- **Scalability:** asynchronous job queues and horizontal scaling by module.
- **Governance:** versioned prompts/schemas, reproducible runs, audit-friendly lineage.
