# Operations Research Optimization Solver

Terminal-based client with a FastAPI backend for:
- Transportation Problem: North-West Corner, Least Cost, VAM, optimal LP, compare all, best initial heuristic.
- Assignment Problem: minimum-cost assignment using SciPy's linear assignment implementation (Hungarian algorithm).

## Setup (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run API (Terminal 1)

From the project root:

```powershell
python -m uvicorn backend.api:app --reload
```

Open http://127.0.0.1:8000/docs to test the API.

## Run terminal client (Terminal 2)

From the project root:

```powershell
python -m backend.client
```

The client sends requests to FastAPI at http://127.0.0.1:8000.

## Notes
- Transportation input must be balanced: total supply equals total demand.
- Initial methods are feasible heuristics and are not guaranteed optimal.
- `optimal` and `compare` use linear programming for the true minimum.
- Assignment supports rectangular matrices; every member of the smaller side is assigned one-to-one.
