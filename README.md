# Operations Research Optimization Solver

A Python-based Operations Research Solver built using **FastAPI, NumPy, and SciPy** to solve transportation and assignment optimization problems. The application provides REST API endpoints and interactive Swagger documentation for testing optimization algorithms.

## 🚀 Live Demo

**Live API Documentation (Swagger UI):**  
https://optimization-x038.onrender.com/docs

**API Base URL:**  
https://optimization-x038.onrender.com

**GitHub Repository:**  
https://github.com/piyushbhati210/Optimization

> **Note:** The application is hosted on Render's free plan. It may sleep after inactivity, so the first request can take some time to respond.

## ✨ Features

### 1. Transportation Problem
- Solves transportation problems with multiple sources and destinations.
- Supports initial solution methods:
  - North-West Corner Method
  - Least Cost Method
  - Vogel's Approximation Method (VAM)
- Supports optimal transportation cost calculation using Linear Programming.
- Validates supply and demand totals.
- Returns allocation matrices, total cost, row totals, and column totals.
- Provides supply and demand verification.

### 2. Assignment Problem
- Solves assignment problems using the Hungarian algorithm through SciPy.
- Finds the minimum-cost assignment.
- Returns the selected assignments and total assignment cost.

### 3. API and Testing
- FastAPI-based REST API.
- Interactive Swagger UI documentation.
- JSON request and response formats.
- Input validation and error responses.
- Publicly accessible deployment through Render.

## 🛠️ Technology Stack

- **Language:** Python
- **API Framework:** FastAPI
- **Server:** Uvicorn
- **Numerical Computing:** NumPy
- **Optimization:** SciPy
- **API Documentation:** Swagger UI / OpenAPI
- **Version Control:** Git and GitHub
- **Deployment:** Render

## 📂 Project Structure

```text
Optimization/
├── backend/
│   ├── __init__.py
│   ├── api.py
│   └── client.py
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3
- Git
- A terminal such as PowerShell or Command Prompt

### Step 1: Clone the repository

```bash
git clone https://github.com/piyushbhati210/Optimization.git
cd Optimization
```

### Step 2: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 3: Start the API server

```bash
python -m uvicorn backend.api:app --reload
```

### Step 4: Open the API documentation

Visit:

http://127.0.0.1:8000/docs

The interactive documentation lets you submit requests and inspect the results.

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API home/status |
| POST | `/transportation` | Solve transportation problems |
| POST | `/assignment` | Solve assignment problems |

For the exact request formats and available methods, refer to the [live API documentation](https://optimization-x038.onrender.com/docs).

## 🧮 Example 1: Transportation Problem

### Request

Send a `POST` request to `/transportation`:

```json
{
  "costs": [
    [5, 9, 2, 3],
    [5, 7, 8, 4],
    [6, 4, 5, 7],
    [5, 8, 3, 2]
  ],
  "supply": [20, 30, 25, 25],
  "demand": [30, 20, 25, 25],
  "method": "optimal"
}
```

### Example response

```json
{
  "problem": "transportation",
  "method": "Linear Programming",
  "total_cost": 345,
  "supply_verified": true,
  "demand_verified": true,
  "optimality_guaranteed": true
}
```

The actual response also includes the allocation matrix and row and column totals.

## 🧮 Example 2: Assignment Problem

### Request

Send a `POST` request to `/assignment`:

```json
{
  "costs": [
    [5, 9, 2, 3],
    [5, 7, 8, 4],
    [6, 4, 5, 7],
    [5, 8, 3, 2]
  ]
}
```

Use the response returned by the API to inspect the selected assignments and minimum total cost.

## ▶️ How to Test the Live API

1. Open the [Live Swagger UI](https://optimization-x038.onrender.com/docs).
2. Expand `POST /transportation` or `POST /assignment`.
3. Click **Try it out**.
4. Enter the JSON request.
5. Click **Execute**.
6. Review the HTTP status and JSON response.

No local installation is required to test the hosted API.

## 🎯 Project Objective

The objective of this project is to demonstrate how Operations Research optimization techniques can be implemented in Python and exposed through a REST API. It provides an interactive way to submit optimization problems, obtain solutions, and verify transportation constraints.

## 👨‍💻 Author

**Piyush Bhati**

- GitHub: https://github.com/piyushbhati210
- Project Repository: https://github.com/piyushbhati210/Optimization
- Live Demo: https://optimization-x038.onrender.com/docs

---

*Developed as a practical project in Operations Research, mathematical optimization, and API development.*
