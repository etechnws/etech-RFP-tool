# RFP Benchmark Suite

This directory contains a historical benchmark set and tooling inputs for RFP answer quality regression testing.

## Contents
- `historical_rfp/benchmark_set.jsonl`: Canonical benchmark questions and approved answers.
- `samples/predictions_example.jsonl`: Example model output file schema.

## Run scoring
```bash
python3 scripts/score_rfp.py \
  --benchmark benchmarks/historical_rfp/benchmark_set.jsonl \
  --predictions benchmarks/samples/predictions_example.jsonl \
  --output benchmarks/samples/latest_scores.json
```

## Run regression gates
```bash
python3 scripts/check_regression.py \
  --scores benchmarks/samples/latest_scores.json \
  --gates config/release_gates.json
```
