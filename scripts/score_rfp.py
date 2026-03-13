#!/usr/bin/env python3
"""Score generated RFP answers against a historical benchmark set."""

from __future__ import annotations

import argparse
import json
import statistics
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


DISALLOWED_PATTERNS = {
    "no_unapproved_claims": ["guarantee", "guaranteed", "always", "never fails"],
    "no_customer_names": ["acme corp", "globex", "initech", "wayne enterprises"],
    "no_absolute_guarantees": ["100%", "zero risk", "fully immune"],
    "no_forward_looking_promises": ["will achieve", "will be certified", "coming soon"],
}


@dataclass
class ItemScore:
    citation_correctness: float
    completeness: float
    policy_compliant: float
    edit_distance: float
    ttf_draft_sec: float
    ttf_final_sec: float


def parse_iso8601(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr = [i]
        for j, cb in enumerate(b, start=1):
            ins = curr[j - 1] + 1
            delete = prev[j] + 1
            subst = prev[j - 1] + (ca != cb)
            curr.append(min(ins, delete, subst))
        prev = curr
    return prev[-1]


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def score_item(benchmark: dict, pred: dict) -> ItemScore:
    generated_citations = pred.get("citations", [])
    approved_citations = set(benchmark.get("citations", []))
    correct = sum(1 for citation in generated_citations if citation in approved_citations)
    citation_correctness = correct / max(1, len(generated_citations))

    answer = pred.get("answer", "")
    lower_answer = answer.lower()
    required_points = benchmark.get("required_points", [])
    covered = sum(1 for point in required_points if point.lower() in lower_answer)
    completeness = covered / max(1, len(required_points))

    compliant = 1.0
    for requirement in benchmark.get("policy_requirements", []):
        patterns = DISALLOWED_PATTERNS.get(requirement, [])
        if any(pattern in lower_answer for pattern in patterns):
            compliant = 0.0
            break

    draft = pred.get("answer", "")
    final = pred.get("reviewer_final_answer", pred.get("answer", ""))
    dist = levenshtein(draft, final)
    edit_distance = dist / max(1, len(final))

    started = parse_iso8601(pred["draft_started_at"])
    draft_done = parse_iso8601(pred["draft_completed_at"])
    final_done = parse_iso8601(pred["final_completed_at"])

    ttf_draft = (draft_done - started).total_seconds()
    ttf_final = (final_done - started).total_seconds()

    return ItemScore(citation_correctness, completeness, compliant, edit_distance, ttf_draft, ttf_final)


def aggregate(scores: list[ItemScore]) -> dict:
    return {
        "grounding_citation_correctness": statistics.mean(s.citation_correctness for s in scores),
        "answer_completeness": statistics.mean(s.completeness for s in scores),
        "policy_compliance": statistics.mean(s.policy_compliant for s in scores),
        "reviewer_edit_distance": statistics.mean(s.edit_distance for s in scores),
        "time_to_first_draft_seconds_median": statistics.median(s.ttf_draft_sec for s in scores),
        "time_to_final_seconds_median": statistics.median(s.ttf_final_sec for s in scores),
        "samples": len(scores),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", required=True, type=Path)
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    benchmark_rows = {row["id"]: row for row in load_jsonl(args.benchmark)}
    prediction_rows = {row["id"]: row for row in load_jsonl(args.predictions)}

    missing = set(benchmark_rows) - set(prediction_rows)
    if missing:
        raise SystemExit(f"Missing predictions for IDs: {sorted(missing)}")

    scores = [score_item(benchmark_rows[item_id], prediction_rows[item_id]) for item_id in sorted(benchmark_rows)]
    summary = aggregate(scores)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
