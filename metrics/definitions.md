# RFP Benchmark Metrics

This benchmark evaluates generated RFP responses against approved historical answers.

## 1) Grounding / citation correctness
- **Definition**: Fraction of generated citations that match approved source citations for each question.
- **Scoring**: `correct_citations / max(1, generated_citations)` per item; macro-averaged.
- **Pass target**: `>= 0.90`.

## 2) Answer completeness
- **Definition**: Coverage of required factual points expected in the approved answer.
- **Scoring**: `required_points_covered / total_required_points` per item using case-insensitive phrase matching; macro-averaged.
- **Pass target**: `>= 0.85`.

## 3) Policy compliance
- **Definition**: Rate of answers that violate none of the mapped policy checks.
- **Scoring**: Binary pass/fail per item, averaged over all items.
- **Checks included**:
  - `no_unapproved_claims`
  - `no_customer_names`
  - `no_absolute_guarantees`
  - `no_forward_looking_promises`
- **Pass target**: `>= 0.98`.

## 4) Reviewer edit distance
- **Definition**: How much reviewer rewriting was required between first draft and approved final answer.
- **Scoring**: Normalized Levenshtein distance `distance(draft, final) / max(len(final),1)`; lower is better.
- **Pass target**: `<= 0.20`.

## 5) Time-to-first-draft and time-to-final
- **Definition**:
  - `time_to_first_draft_seconds = draft_completed_at - draft_started_at`
  - `time_to_final_seconds = final_completed_at - draft_started_at`
- **Scoring**: Median across benchmark set.
- **Pass targets**:
  - first draft median `<= 180` seconds
  - final median `<= 600` seconds
