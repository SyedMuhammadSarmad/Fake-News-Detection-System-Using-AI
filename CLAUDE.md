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
| Language | Python 3.12 |
| Web Framework | Django 5 |
| Auth | Django built-in auth + custom `AbstractUser` |
| Admin Panel | Django Admin (auto-generated, customized) |
| Database | SQLite (Django default, zero config) |
| Forms + UI | Django Crispy Forms + Bootstrap 5 (CDN) |
| ML Libraries | Scikit-learn, Pandas, NLTK, Joblib |
| ML Model | TF-IDF (50k features, bigrams) + Logistic Regression → `.joblib` |
| Dataset | Kaggle "Fake and Real News Dataset" (clmentbisaillon) — `True.csv` + `Fake.csv` |
| Visualization | Matplotlib/Seaborn → base64-encoded PNG embedded in templates |
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
│   Bootstrap 5 templates (Jinja2)   │
└──────────────┬──────────────────────┘
               │ HTTP
┌──────────────▼──────────────────────┐
│         Application Layer           │
│  Django 5 (accounts + news apps)   │
│  Auth, News Analysis, Admin views  │
│  Django Admin (customized)         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Data / ML Layer             │
│  SQLite (ORM via Django models)    │
│  ml/ package: preprocessor,        │
│  trainer, predictor (pure Python)  │
│  Saved model: ml_models/*.joblib   │
│  Dataset CSVs: datasets/           │
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
| Export Results | Download results as CSV (Export button on history page) |
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

## Project File Structure (Actual)

```
fake-news-detection/
├── core/                        # Django project config
│   ├── settings.py              # DB, INSTALLED_APPS, AUTH_USER_MODEL, paths
│   ├── urls.py                  # Root URL conf (admin + accounts + news)
│   └── wsgi.py
├── accounts/                    # Django app: custom User model, auth views
│   ├── models.py                # CustomUser (AbstractUser + verified field)
│   ├── views.py                 # register(), profile()
│   ├── forms.py                 # RegistrationForm (email unique), ProfileForm
│   ├── urls.py                  # /accounts/register/, /accounts/profile/
│   └── admin.py                 # CustomUserAdmin: verify_users bulk action
├── news/                        # Django app: analysis, history, export
│   ├── models.py                # NewsArticle, AnalysisResult, Dataset, ModelMetrics
│   ├── views.py                 # dashboard(), analyze(), history(), export_csv()
│   ├── forms.py                 # NewsSubmissionForm, DatasetUploadForm
│   ├── urls.py                  # /news/dashboard|analyze|history|export/
│   └── admin.py                 # DatasetAdmin, ModelMetricsAdmin + retrain endpoint
│                                #   _generate_metrics_chart() — TODO(human) #3
├── ml/                          # Pure Python ML package (no Django imports)
│   ├── preprocessor.py          # clean_text() — TODO(human) #1
│   ├── trainer.py               # train_model(dataset_dir, model_dir) -> dict
│   └── predictor.py             # predict(text, model_dir) -> dict — TODO(human) #2
├── templates/
│   ├── base.html                # Bootstrap 5 navbar, flash messages, footer
│   ├── admin/news/modelmetrics/ # change_list.html — Retrain button + chart img
│   ├── accounts/                # login.html, register.html, profile.html
│   └── news/                    # dashboard.html, analyze.html, history.html
├── static/css/                  # Custom CSS (if needed)
├── datasets/                    # True.csv + Fake.csv from Kaggle go here
├── ml_models/                   # model.joblib + vectorizer.joblib (generated on retrain)
├── db.sqlite3                   # SQLite database (auto-created on migrate)
├── manage.py
├── requirements.txt
└── CLAUDE.md                    # This file
```

### Key settings (core/settings.py)
```python
AUTH_USER_MODEL  = 'accounts.CustomUser'   # set BEFORE first migration
ML_MODEL_DIR     = BASE_DIR / 'ml_models'
MEDIA_ROOT       = BASE_DIR / 'datasets'
LOGIN_REDIRECT_URL   = '/news/dashboard/'
LOGOUT_REDIRECT_URL  = '/accounts/login/'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
```

### Run the server
```bash
# One-time setup
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser   # or use default: admin / admin123

# Development server
python3 manage.py runserver
# → http://127.0.0.1:8000/
```

### Admin credentials (auto-created)
- Username: `admin` | Password: `admin123`
- Login at `http://127.0.0.1:8000/admin/`

---

## Implementation Status

| Phase | Status | Notes |
|---|---|---|
| Phase 1 — Project setup | ✅ Done | Django 5, settings, urls, manage.py |
| Phase 2 — DB models + migrations | ✅ Done | CustomUser, NewsArticle, AnalysisResult, Dataset, ModelMetrics |
| Phase 3 — Auth (register/profile/login) | ✅ Done | register → verified=False → admin approves |
| Phase 4 — ML pipeline | ✅ Done (partial) | trainer.py complete; `clean_text()` and `predict()` are **TODO(human)** |
| Phase 5 — User views + templates | ✅ Done | dashboard, analyze, history, export CSV, all Bootstrap templates |
| Phase 6 — Admin panel | ✅ Done (partial) | Retrain button wired; `_generate_metrics_chart()` is **TODO(human)** |

### Student TODO(human) tasks remaining
1. **`ml/preprocessor.py` → `clean_text()`** — 7-step NLP pipeline (lowercase → URLs → non-alpha → tokenize → stopwords → lemmatize → rejoin)
2. **`ml/predictor.py` → `predict()`** — load joblib model, vectorize, predict label + proba, return verdict + confidence
3. **`news/admin.py` → `_generate_metrics_chart()`** — matplotlib line chart → BytesIO → base64 string for inline `<img>`

### Dataset required before training
Place these two files in the `datasets/` folder:
- `datasets/True.csv`
- `datasets/Fake.csv`

Download from Kaggle: **clmentbisaillon/fake-and-real-news-dataset**

---

## Key Constraints

- Must use **Python** (non-Python solutions may be rejected)
- UI must be properly designed (no bare unstyled HTML)
- All database tables must have properly defined relationships
- Admin must be able to retrain the model from the UI (`/admin/news/modelmetrics/retrain/`)
- System metrics (accuracy, precision, recall, F1) must be visible to admin
