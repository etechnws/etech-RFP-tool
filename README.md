# eTech RFP Workbench (Reconstructed Source Baseline)

This repository now includes a runnable baseline for the RFP Workbench so code can be iterated in-repo instead of relying on an external running instance.

## Repository layout

- `backend/` – FastAPI service (`main.py` entrypoint)
- `frontend/` – Vite + React UI source
- `docker-compose.yml` – optional local orchestration
- `.env.example` – environment template
- `docs/qa-gap-review.md` – QA gap mapping vs. target RFP behavior

## Quick start

### 1) Configure environment

```bash
cp .env.example .env
```

### 2) Run backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3) Run frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

The frontend expects backend URL from `VITE_API_BASE_URL` (defaults to `http://localhost:8000`).

## Docker compose (optional)

```bash
docker compose up --build
```

