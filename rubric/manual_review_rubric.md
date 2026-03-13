# Manual Review Rubric for RFP Responses

Use this rubric when automated scoring is inconclusive or when auditing sampled responses.

## Reviewer instructions
1. Read the benchmark question and approved answer.
2. Evaluate the generated answer independently.
3. Assign scores using the tables below.
4. Record required edits and rationale.

## Dimension A: Grounding and citation correctness (0-4)
- **4**: All claims are grounded in approved sources; citations are specific and correct.
- **3**: Minor citation formatting issues; no unsupported material claims.
- **2**: Some claims weakly supported or generic citations.
- **1**: Multiple unsupported claims; citation mismatches.
- **0**: Citations missing or fabricated.

## Dimension B: Completeness (0-4)
- **4**: Covers all required points with accurate detail.
- **3**: Misses one minor required point.
- **2**: Misses multiple required points or compresses critical detail.
- **1**: Partial response with substantial omissions.
- **0**: Fails to answer question.

## Dimension C: Policy compliance (0-4)
- **4**: Fully compliant; no risky claims.
- **3**: Low-risk wording concerns, no policy breach.
- **2**: One probable policy issue requiring edit.
- **1**: Multiple policy concerns.
- **0**: Clear disallowed content.

## Dimension D: Edit effort (0-4)
- **4**: Reviewer performs cosmetic edits only.
- **3**: Light wording edits.
- **2**: Moderate restructuring.
- **1**: Heavy rewrite required.
- **0**: Full rewrite from scratch.

## Dimension E: Operational latency (0-4)
- **4**: Draft and final both within target SLA.
- **3**: One latency target slightly exceeded.
- **2**: Both targets exceeded but usable.
- **1**: Significantly delayed iteration.
- **0**: Unusable turnaround.

## Decision bands
- **Ship candidate**: Total score `>= 17` and no dimension below `3`.
- **Needs tuning**: Total score `12-16` or any dimension at `2`.
- **Block release**: Total score `<= 11` or any dimension `0-1`.
