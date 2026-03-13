#!/usr/bin/env python3
"""Fail CI when metric regressions exceed configured gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HIGHER_IS_BETTER = {
    "grounding_citation_correctness",
    "answer_completeness",
    "policy_compliance",
}
LOWER_IS_BETTER = {
    "reviewer_edit_distance",
    "time_to_first_draft_seconds_median",
    "time_to_final_seconds_median",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scores", required=True, type=Path)
    parser.add_argument("--gates", required=True, type=Path)
    args = parser.parse_args()

    scores = load_json(args.scores)
    gates = load_json(args.gates)

    failures: list[str] = []
    for metric, threshold in gates["thresholds"].items():
        if metric not in scores:
            failures.append(f"missing metric '{metric}' in score output")
            continue

        value = scores[metric]
        if metric in HIGHER_IS_BETTER and value < threshold:
            failures.append(f"{metric} regressed: {value:.4f} < {threshold:.4f}")
        elif metric in LOWER_IS_BETTER and value > threshold:
            failures.append(f"{metric} regressed: {value:.4f} > {threshold:.4f}")

    if failures:
        print("Regression gate failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("All regression gates passed.")


if __name__ == "__main__":
    main()
