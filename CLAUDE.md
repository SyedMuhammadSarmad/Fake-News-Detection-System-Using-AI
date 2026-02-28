# Fake News Detection System Using AI — CLAUDE.md

## Project Overview

**Course:** CS619 — Final Year Project (FYP)
**Group ID:** F25PROJECT5A938
**Supervisor:** Huma Mumtaz
**Authors:** bc220413756, bc220413177
**Design Document Version:** 1.0 (23 Jan 2026)

A Python-based web application that lets users submit news articles or headlines and receive an AI/ML-powered verdict: **Real** or **Fake**, along with a confidence score.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| ML Libraries | Scikit-learn, Pandas, NumPy, NLTK |
| Dataset | Kaggle Public Fake News Dataset |
| IDE | VS Code / Jupyter Notebook |
| Visualization | Matplotlib, Seaborn |
| Version Control | GitHub |

> Use the **latest and smartest Python-based tools/platforms**. Non-Python solutions risk rejection.

---

## Core Functional Requirements

### 1. User Registration & Profile Management
- Secure registration flow: user registers → admin verifies → user gets access
- Users can **view and update** their own profiles
- Strict privacy protection on all user data

### 2. News Submission & Analysis
- Users submit news articles or headlines
- AI/ML model analyzes submission and returns **"Real"** or **"Fake"** + confidence score
- Users can view full **history** of previously analyzed articles

### 3. Admin Panel
- Manage user accounts: **Add, Update, Delete**
- Upload and update training datasets (CSV only)
- **Retrain** the AI model when new data is added
- View system performance metrics: accuracy, precision, recall, F1-score
- Generate usage reports
- Delete analysis history
- Ensure data security and user privacy

---

## System Architecture (Three-Tier)

```
┌─────────────────────────────────────┐
│           Interface Layer           │
│  User Dashboard  |  Admin Dashboard │
│       Main Page  |  Login / Register│
└──────────────┬──────────────────────┘
               │ HTTP
┌──────────────▼──────────────────────┐
│         Application Layer           │
│  Flask / FastAPI backend            │
│  Auth, News Analysis, Admin APIs    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Data / ML Layer             │
│  Database (Users, News, History)    │
│  Scikit-learn ML Model              │
│  Dataset storage (CSV uploads)      │
└─────────────────────────────────────┘
```

---

## Database Design — Key Entities (ERD)

- **User** — id, name, email, password_hash, role (user/admin), verified, created_at
- **NewsArticle** — id, user_id (FK), text/headline, submitted_at
- **AnalysisResult** — id, article_id (FK), verdict (Real/Fake), confidence_score, analyzed_at
- **Dataset** — id, filename, uploaded_by (FK admin), uploaded_at
- **ModelMetrics** — id, accuracy, precision, recall, f1_score, trained_at

Maintain **foreign key relationships** between all tables.

---

## User Flows (Sequence Diagrams)

| Flow | Description |
|---|---|
| User Registration | Register → Admin verifies → Access granted |
| User Login | Email/password → Auth → Dashboard |
| Analyze News Article | Submit text → ML inference → Show result + confidence |
| View Analysis History | Fetch user's past submissions and results |
| Test with Sample Datasets | Run model against sample data |
| View Visualizations | Graphs: accuracy trends, Real/Fake distribution |
| Export Results | Download results as PDF or Excel |
| Admin – Add/Update/Delete User | Full CRUD on user accounts |
| Admin – Upload Dataset | CSV upload only; validate format |
| Admin – Retrain Model | Trigger retraining with latest dataset |
| Admin – View System Metrics | Accuracy, precision, recall, F1 |
| Admin – Generate Reports | Usage and performance reports |
| Admin – Delete History | Remove analysis history records |

---

## Interface Design

- **Main Page** — Landing/home page
- **User Dashboard** — Submit news, view history, view graphs, export
- **Admin Dashboard** — User management, dataset upload, model retraining, metrics

> All interfaces must be **properly designed** with complete **input validation** on every form.

---

## Test Cases Reference (UC → TC Mapping)

| Use Case | ID | Key Test Scenarios |
|---|---|---|
| Login | UC-01 | TC-01 valid login, TC-02 wrong password, TC-03 forgot password, TC-04 DB unavailable |
| Manage Users | UC-02 | TC-05 add user, TC-06 update, TC-07 delete, TC-08 duplicate email |
| Upload Dataset | UC-03 | TC-09 valid CSV, TC-10 invalid .exe, TC-11 corrupted CSV |
| Retrain Model | UC-04 | TC-12 retrain success, TC-13 cancel, TC-14 timeout on large dataset |
| View Metrics | UC-05 | TC-15 metrics displayed with correct values |
| Export Results | UC-13 | TC-32 PDF, TC-33 Excel, TC-34 cancel export |
| View History | UC-11 | TC-28 records shown, TC-29 empty history message |
| View Graphs | UC-12 | TC-30 charts displayed, TC-31 no analysis warning |
| Receive Result | UC-10 | TC-26 Fake/Real + confidence shown, TC-27 model not trained error |

---

## Development Standards

- **Input validation** required on every form (email format, file type, empty fields)
- **Privacy:** never expose other users' data; hash all passwords
- **Dataset uploads:** accept CSV only; reject .exe or corrupted files with clear error messages
- **Model retraining:** must store new model and update metrics after retraining
- **Confidence score** must always accompany every Real/Fake verdict
- **Visualizations:** use Matplotlib/Seaborn for accuracy trends and distribution charts

---

## Project File Structure (Recommended)

```
fake-news-detection/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── auth.py         # Login, registration
│   │   ├── user.py         # News submission, history
│   │   └── admin.py        # Admin CRUD, dataset, retrain
│   ├── models/
│   │   ├── db_models.py    # SQLAlchemy/ORM table definitions
│   │   └── ml_model.py     # ML training & inference
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JS, assets
├── datasets/               # Uploaded CSV files
├── ml/
│   ├── train.py            # Model training script
│   └── saved_model/        # Persisted model files
├── tests/                  # Unit/integration tests
├── requirements.txt
└── CLAUDE.md               # This file
```

---

## Key Constraints

- Must use **Python** (non-Python solutions may be rejected)
- UI must be properly designed (no bare unstyled HTML)
- All database tables must have properly defined relationships
- Admin must be able to retrain the model from the UI
- System metrics (accuracy, precision, recall, F1) must be visible to admin
