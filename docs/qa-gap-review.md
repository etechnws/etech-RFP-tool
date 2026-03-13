# QA Gap Review (Post-Source-Restoration Baseline)

## Runtime target inspected

- Target URL: `http://etech_rfp_workbench:8000/`
- All probed routes returned `400 Bad Request` from `envoy`, so feature-level behavior of the target deployment could not be directly validated from this environment.

## Confirmed repository/branch state

- Current repository branch: `work`
- Prior to this update, repo contained only image assets and no runnable application source.
- Conclusion: this branch did **not** contain the running app source; baseline backend/frontend source has now been created in-repo to enable continued development.

## Gap map vs target RFP behavior

### Present now

1. API server entrypoint with health route (`backend/main.py`)
2. Frontend UI source scaffold (`frontend/src`)
3. Dependency manifests (`backend/requirements.txt`, `frontend/package.json`)
4. Env template and startup docs (`.env.example`, `README.md`)

### Missing / not yet synced

1. End-to-end RFP ingest workflow (upload + parsing)
2. Real analysis/scoring engine behavior behind `/api/rfp/analyze`
3. Persistence layer/schema and migration scripts
4. AuthN/AuthZ model and user/session controls
5. Integration connectors (LLM/provider APIs, external data sources)
6. Production deployment manifests from target environment
7. Test suite mirroring expected acceptance criteria

## Recommended next sync pass

1. Obtain source-of-truth repo URL + branch for `etech_rfp_workbench` deployment.
2. Diff restored baseline against source-of-truth code.
3. Port backend business logic and frontend workflows.
4. Re-run behavioral QA against agreed RFP acceptance checklist.
