from typing import Literal

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scipy.optimize import linear_sum_assignment, linprog

app = FastAPI(
    title="Operations Research Optimization API",
    description="Transportation and Assignment Problem Solver",
    version="1.0.0",
)


class TransportationRequest(BaseModel):
    costs: list[list[float]]
    supply: list[float]
    demand: list[float]
    method: Literal[
        "north_west", "least_cost", "vam",
        "optimal", "compare", "best_initial"
    ] = "optimal"


class AssignmentRequest(BaseModel):
    costs: list[list[float]]


def validate_transport(p):
    try:
        c = np.asarray(p.costs, dtype=float)
        s = np.asarray(p.supply, dtype=float)
        d = np.asarray(p.demand, dtype=float)
    except (TypeError, ValueError):
        raise HTTPException(400, "All inputs must be numeric.")

    if c.ndim != 2 or c.size == 0:
        raise HTTPException(400, "Costs must be a non-empty matrix.")
    m, n = c.shape
    if m > 100 or n > 100:
        raise HTTPException(400, "Maximum matrix size is 100 x 100.")
    if s.ndim != 1 or d.ndim != 1 or len(s) != m or len(d) != n:
        raise HTTPException(400, "Supply/demand dimensions do not match costs.")
    if not (np.isfinite(c).all() and np.isfinite(s).all() and np.isfinite(d).all()):
        raise HTTPException(400, "Inputs must be finite.")
    if (c < 0).any() or (s < 0).any() or (d < 0).any():
        raise HTTPException(400, "Costs, supply and demand must be non-negative.")
    if not np.isclose(s.sum(), d.sum()):
        raise HTTPException(
            400,
            f"Unbalanced problem: supply={s.sum()}, demand={d.sum()}. "
            "Add a dummy source or destination first."
        )
    return c, s, d


def initial_solution(c, supply, demand, method):
    m, n = c.shape
    s, d = supply.copy(), demand.copy()
    x = np.zeros((m, n))
    eps = 1e-8

    while s.sum() > eps:
        rows = [i for i in range(m) if s[i] > eps]
        cols = [j for j in range(n) if d[j] > eps]
        if not rows or not cols:
            break

        if method == "north_west":
            i, j = rows[0], cols[0]
        elif method == "least_cost":
            i, j = min(
                ((i, j) for i in rows for j in cols),
                key=lambda z: (c[z], z[0], z[1])
            )
        else:
            candidates = []
            for i0 in rows:
                ordered = sorted((c[i0, j], j) for j in cols)
                penalty = ordered[1][0] - ordered[0][0] if len(ordered) > 1 else 0
                candidates.append(
                    (penalty, -ordered[0][0], -i0, -ordered[0][1],
                     i0, ordered[0][1])
                )
            for j0 in cols:
                ordered = sorted((c[i, j0], i) for i in rows)
                penalty = ordered[1][0] - ordered[0][0] if len(ordered) > 1 else 0
                candidates.append(
                    (penalty, -ordered[0][0], -ordered[0][1], -j0,
                     ordered[0][1], j0)
                )
            *_, i, j = max(candidates)

        qty = min(s[i], d[j])
        x[i, j] += qty
        s[i] -= qty
        d[j] -= qty
    return x


def optimal_transport(c, supply, demand):
    m, n = c.shape
    a_supply = np.zeros((m, m * n))
    a_demand = np.zeros((n, m * n))
    for i in range(m):
        a_supply[i, i*n:(i+1)*n] = 1
    for j in range(n):
        a_demand[j, j::n] = 1

    result = linprog(
        c.flatten(),
        A_eq=np.vstack([a_supply, a_demand]),
        b_eq=np.r_[supply, demand],
        bounds=(0, None),
        method="highs",
    )
    if not result.success:
        raise HTTPException(422, f"Optimization failed: {result.message}")
    x = result.x.reshape(m, n)
    x[np.abs(x) < 1e-8] = 0
    return x


def transport_result(c, x, supply, demand, optimal=False):
    return {
        "allocation": x.tolist(),
        "total_cost": float(np.sum(c * x)),
        "row_totals": x.sum(axis=1).tolist(),
        "column_totals": x.sum(axis=0).tolist(),
        "supply_verified": bool(np.allclose(x.sum(axis=1), supply)),
        "demand_verified": bool(np.allclose(x.sum(axis=0), demand)),
        "optimality_guaranteed": optimal,
    }


@app.get("/")
def home():
    return {
        "message": "Operations Research API is running",
        "docs": "/docs",
        "endpoints": ["/transportation", "/assignment"],
    }


@app.post("/transportation")
def transportation(p: TransportationRequest):
    c, s, d = validate_transport(p)
    names = {
        "north_west": "North-West Corner",
        "least_cost": "Least Cost",
        "vam": "Vogel's Approximation Method",
    }

    if p.method in names:
        x = initial_solution(c, s, d, p.method)
        return {
            "problem": "transportation",
            "method": names[p.method],
            **transport_result(c, x, s, d),
        }

    if p.method == "optimal":
        x = optimal_transport(c, s, d)
        return {
            "problem": "transportation",
            "method": "Linear Programming",
            **transport_result(c, x, s, d, optimal=True),
        }

    results = {}
    for key, name in names.items():
        x = initial_solution(c, s, d, key)
        results[key] = {
            "method": name,
            **transport_result(c, x, s, d),
        }

    if p.method == "compare":
        x = optimal_transport(c, s, d)
        results["optimal"] = {
            "method": "Linear Programming",
            **transport_result(c, x, s, d, optimal=True),
        }
        return {"problem": "transportation", "results": results}

    best_key = min(results, key=lambda k: results[k]["total_cost"])
    return {
        "problem": "transportation",
        "method": "Best Initial Solution",
        "selected_method": best_key,
        **results[best_key],
        "all_initial_results": results,
    }


@app.post("/assignment")
def assignment(p: AssignmentRequest):
    try:
        c = np.asarray(p.costs, dtype=float)
    except (TypeError, ValueError):
        raise HTTPException(400, "Costs must be numeric.")

    if c.ndim != 2 or c.size == 0:
        raise HTTPException(400, "Enter a non-empty cost matrix.")
    if max(c.shape) > 100:
        raise HTTPException(400, "Maximum matrix dimension is 100.")
    if not np.isfinite(c).all():
        raise HTTPException(400, "Costs must be finite numbers.")

    rows, cols = linear_sum_assignment(c)
    allocation = np.zeros(c.shape, dtype=int)
    allocation[rows, cols] = 1
    assignments = [
        {"row": int(i + 1), "column": int(j + 1), "cost": float(c[i, j])}
        for i, j in zip(rows, cols)
    ]
    return {
        "problem": "assignment",
        "method": "Hungarian Algorithm",
        "allocation": allocation.tolist(),
        "assignments": assignments,
        "total_cost": float(c[rows, cols].sum()),
        "rows_assigned": len(rows),
        "columns_assigned": len(cols),
        "optimality_guaranteed": True,
    }
