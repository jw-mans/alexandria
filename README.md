# Alexandria

Alexandria is a lightweight experiment tracking system for machine learning projects.  
It allows you to log experiments, track metrics, code, datasets, artifacts, and environment, and compare different runs easily.

---

## Why Alexandria?

Many teams use tools like MLflow, Weights & Biases, or even Git to track ML experiments. Alexandria is designed to be:

- **Simple and lightweight**: Minimal setup, no heavy infrastructure required.
- **Python-native**: Fully integrates with Python projects and ML pipelines.
- **Flexible**: Works with CSVs, pandas DataFrames, and HuggingFace datasets.
- **CLI & API ready**: Track experiments via a decorator, and inspect them with a CLI or directly via the backend API.
- **Run comparison**: Easily see differences between experiment runs (parameters, metrics, datasets, code, and artifacts).

Unlike MLflow or Langfuse, Alexandria doesn’t require a database server or complicated UI setups. Unlike Git, it understands ML-specific entities like metrics and datasets.

---

## Features

### Ready:
- Logging experiments automatically with a `@track` decorator
- Tracking metrics in loops (e.g., epochs)
- Profiling datasets, code, artifacts, and environment
- REST API backend (FastAPI) to store and query experiments
- CLI to inspect runs, artifacts, datasets, and diffs
- Diff between two runs (metrics, parameters, datasets, code, artifacts, environment)

### Planned:
- Support for remote backends
- Authentication and multi-user support
- Custom dataset types and ML frameworks integration
- Enhanced visualization (graphs, charts)
- Alerts and notifications on metric changes

---

## Installation

```bash
git clone https://github.com/yourusername/alexandria.git
cd alexandria
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Usage
### Tracking experiments
```Python
from tracker.decorators import track, log_metric

@track(experiment_name="my_experiment")
def train():
    for step in range(10):
        loss = 0.1 * step
        acc = 0.9 - 0.01 * step
        log_metric("loss", loss, step)
        log_metric("accuracy", acc, step)
        # training logic here

train()
```
### CLI
```bash
# Show run details
alex show run RUN_ID

# List datasets
alex datasets list --limit 50

# List artifacts
alex artifacts list RUN_ID

# Compare two runs
alex diff runs RUN1_ID RUN2_ID
```
## Architecture

- **Backend**: FastAPI + SQLite, storing runs, metrics, parameters, artifacts, datasets, and environment

- **Tracker**: Python decorator @track, automatic profiling

- **CLI**: Typer-based CLI to inspect runs and datasets

- **Serialization**: Runs are converted into JSON-compatible format for storage and comparison

## Contributing
Contributions are welcome! Please submit issues or pull requests for bug fixes, new features, or improvements.
