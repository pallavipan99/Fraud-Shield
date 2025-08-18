# FraudShield: A Fraud Detection System

FraudShield is a complete **end‑to‑end fraud detection system** that you can run locally. It includes:
- **Backend (Python/Flask + SQLAlchemy)** for a REST API, model inference, and SQLite persistence.
- **ML training pipeline** using **scikit‑learn**, **SMOTE** (imbalanced‑learn), and optional **XGBoost**, with artifacts saved via `joblib`.
- **Frontend (React + Vite)** dashboard that visualizes KPIs, a time series of flags, and recent transactions; plus pages to ingest and batch‑score transactions.
- **Infra scaffold** for an optional **AWS Lambda** scorer that pulls model artifacts from S3.

---

## Repository Structure (detected from the zip)

```
FraudShield/
├─ backend/
│  ├─ app.py
│  ├─ train.py
│  ├─ utils.py
│  ├─ requirements.txt
│  └─ data/
│     └─ .gitkeep
├─ frontend/
│  ├─ package.json
│  ├─ vite.config.js
│  ├─ index.html
│  └─ src/
│     ├─ main.jsx
│     ├─ styles.css
│     ├─ App.jsx
│     ├─ api.js
│     └─ pages/
│        ├─ Dashboard.jsx
│        ├─ Ingest.jsx
│        └─ Batch.jsx
└─ infra/
   └─ lambda/
      ├─ handler.py
      └─ requirements.txt
```

> Notes
> - The backend expects to persist to **SQLite** by default (`sqlite:///fraudshield.db`). You can override with `DB_URL`.
> - The frontend uses `VITE_API_BASE_URL` if defined; otherwise it defaults to `http://localhost:5001/api`.
> - If the Kaggle dataset is not present, the trainer **generates a synthetic imbalanced dataset** so you can run everything without external data.

---

## Tech Stack

**Backend**
- Python, Flask, Flask‑CORS
- SQLAlchemy (SQLite by default; configurable via `DB_URL`)
- scikit‑learn, imbalanced‑learn (SMOTE), joblib, XGBoost

**Frontend**
- React (Vite)
- Axios (API client)
- Recharts (visualizations)
- React Router (routing)

**Infra (optional)**
- AWS Lambda handler scaffold (loads artifacts from S3)

---

## Backend — Setup, Train, Serve

### 1) Create a virtual environment and install dependencies
```bash
cd backend
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

pip install -r requirements.txt
```

### 2) (Optional) Provide Kaggle dataset
If you have the Kaggle credit card fraud dataset, place it at:
```
backend/data/creditcard.csv
```
Expected columns: `V1..V28, Amount, Class` (Class ∈ {0,1}).

If the file is **not** present, the trainer will **generate a synthetic imbalanced dataset** with 30 features plus an `amount` feature.

### 3) Train the model
```bash
python train.py
```
This will:
- Split data; scale with `StandardScaler`.
- Apply **SMOTE** to the **training** split only.
- Train candidates (RandomForest, MLP, and XGBoost if installed).
- Select best by AUROC and persist to `backend/models/`:
  - `model.joblib`
  - `scaler.joblib`
  - `meta.json` (model name, version, AUROC, threshold, feature list)

### 4) Start the API
```bash
python app.py
```
The API runs at: `http://localhost:5001/api`

**Configurable env vars:**
- `DB_URL` (default `sqlite:///fraudshield.db`)
- `PORT` (default `5001`)

---

## Frontend — Run the Dashboard

Open a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Vite will print a local URL (e.g., `http://localhost:5173` or `http://localhost:5174`).  
The frontend points to the backend via:
```
VITE_API_BASE_URL=http://localhost:5001/api
```
Set a custom value by creating `frontend/.env` if needed.

---

## API Endpoints (from `backend/app.py`)

**Base URL**: `http://localhost:5001/api`

| Method | Endpoint                   | Description |
|------:|----------------------------|-------------|
| GET   | `/health`                  | Health check and model status (version, whether artifacts are loaded) |
| POST  | `/predict`                 | Score a **single** transaction (no persistence) |
| POST  | `/transactions`            | Score and **persist** a single transaction to SQLite |
| GET   | `/transactions`            | List recent transactions; supports `?flagged=true&limit=50` |
| POST  | `/batch-score`             | Score an **array** of transactions in one call |
| GET   | `/metrics`                 | Returns totals, flagged rate, and a simple time series (`?last_minutes=1440`) |

### Example: health
```bash
curl http://localhost:5001/api/health
```

### Example: single predict (synthetic features)
```bash
curl -X POST http://localhost:5001/api/predict   -H "Content-Type: application/json"   -d '{"f1": 0.5, "f2": -1.2, "amount": 120.50}'
```

### Example: single predict (Kaggle features)
```bash
curl -X POST http://localhost:5001/api/predict   -H "Content-Type: application/json"   -d '{"V1": 0.5, "V2": -1.2, "Amount": 120.50}'
```

### Example: persist a transaction
```bash
curl -X POST http://localhost:5001/api/transactions   -H "Content-Type: application/json"   -d '{"f1": 0.2, "f2": -1.1, "amount": 89.30}'
```

### Example: list last 5
```bash
curl "http://localhost:5001/api/transactions?limit=5"
```

### Example: list last 5 flagged
```bash
curl "http://localhost:5001/api/transactions?flagged=true&limit=5"
```

### Example: batch score
```bash
curl -X POST http://localhost:5001/api/batch-score   -H "Content-Type: application/json"   -d '[{"f1":0.1,"f2":0.3,"amount":25.0},{"V1":-0.2,"V2":1.05,"Amount":300.0}]'
```

---

## Frontend Pages (from `frontend/src/pages`)

- `Dashboard.jsx` — shows KPIs (total, flagged, flagged_rate), a small time-series chart (Recharts `LineChart`) of recent flags, and the recent transactions table. Auto-refreshes every few seconds.
- `Ingest.jsx` — form to send a single transaction with 30 synthetic features (`f1..f30`) and `amount` to `/api/transactions`. Includes a **Randomize** helper.
- `Batch.jsx` — textarea to paste an array of transaction JSON objects for `/api/batch-score`, with response preview.

`frontend/src/api.js` centralizes the base URL using Axios. `styles.css` provides a minimal card/table layout.

---

## AWS Lambda Scaffold (optional)

`infra/lambda/handler.py` demonstrates a simple scorer that:
- Downloads `model.joblib` and `scaler.joblib` from S3 using env vars `MODEL_BUCKET`, `MODEL_KEY`, `SCALER_KEY`.
- Caches the artifacts in `/tmp` and scores a JSON payload.

This is a **starting point** for serverless deployment; you’ll still need to package dependencies appropriately (Lambda layer or manylinux‑compatible wheels).

---

## Notes and Tips

- **XGBoost optional**: If `pip install xgboost` fails on your platform, training still works with RandomForest and MLP.
- **Feature names accepted**: The backend can consume either **Kaggle** feature names (`V1..V28`, `Amount`) or **synthetic** names (`f1..f30`, `amount`). `utils.py` maps alternates to the expected feature list (`meta.json`).
- **Database URL**: Change to Postgres/MySQL by setting `DB_URL` (e.g., `postgresql+psycopg://user:pass@host/dbname`). SQLAlchemy will create the schema on first run.
- **Ports**: Backend defaults to `5001`; Vite dev server typically uses `5173`/`5174`. If you change the backend port, set `VITE_API_BASE_URL` accordingly.
---

## License

MIT License. Review the license before reuse in production or regulated environments.
