# Alexandria

**Description:**  
Python project for automatic tracking of ML experiments: collects parameters, metrics, artifacts, dataset info, code, and environment details, and sends them to a backend.

---
## Project Structure
```graphql
alexandria/
│
├── tracker/            # Python library for auto-tracking
├── backend/            # FastAPI backend with SQLite
├── frontend/           # Web interface for DAG visualization
├── cli/                # CLI for interacting with runs
├── docs/               # Documentation (on Russian)
├── docker-compose.yml
├── pyproject.toml
└── README.md
```
---
## Current status 
**Python tracker implemented:**
- `@track` decorator for training functions.

- Automatic dataset detection (`pandas.DataFrame`, CSV).

- Metric and artifact logging.

- Code, environment, and Git commit tracking.

- Sending runs to the backend via REST API.

- Backend is ready to receive run records.