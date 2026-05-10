# Setup Guide — Fake News Detection System

## Prerequisites
- Python 3.12 (https://www.python.org/downloads/)
- Git (https://git-scm.com/)
- A Kaggle account (free) to download the dataset

---

## Step 1 — Clone the Repository

```bash
git clone <your-github-repo-url>
cd "Fake News Detection System Using AI"
```

---

## Step 2 — Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Django, scikit-learn, NLTK, reportlab, openpyxl, matplotlib, and all other required packages.

---

## Step 4 — Set Up the Database

```bash
python manage.py migrate
```

---

## Step 5 — Create the Admin Account

```bash
python manage.py createsuperuser
```

When prompted, enter:
- **Username:** admin
- **Email:** (press Enter to skip)
- **Password:** admin123

---

## Step 6 — Download the Dataset

1. Go to: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
2. Download and extract the zip
3. Place both CSV files in the `datasets/` folder:

```
datasets/
├── True.csv
└── Fake.csv
```

> The `datasets/` folder already exists in the repo. Just drop the files in.

---

## Step 7 — Run the Server

```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## Step 8 — First-Time Setup Flow

### A. Train the AI model (Admin)
1. Go to http://127.0.0.1:8000/admin
2. Login: **admin / admin123**
3. Click **Model Metrics** in the sidebar
4. Click the **Retrain Model** button
5. Wait 1–2 minutes — accuracy/F1 scores will appear along with a performance chart

### B. Register a test user
1. Go to http://127.0.0.1:8000/accounts/register/
2. Fill in the form and submit
3. You will see an "awaiting admin approval" message

### C. Verify the user (Admin)
1. In the admin panel → **Users**
2. Tick the new user → select **"Verify selected users"** from the Action dropdown → click **Go**

### D. Analyze a news article (User)
1. Log in as the test user at http://127.0.0.1:8000/accounts/login/
2. Go to **Analyze Article**
3. Either paste any news text (minimum 20 characters) OR click one of the **sample article** buttons to auto-fill
4. Click **Run Analysis**
5. Result shows **Real** or **Fake** with a confidence percentage

### E. View history and export
1. Go to **History** to see all past analyses
2. Use the export buttons to download your results:
   - **CSV** — plain spreadsheet
   - **Excel** — formatted .xlsx file
   - **PDF** — formatted PDF report

### F. View charts (User Dashboard)
- The dashboard shows two charts once you have at least one analysis:
  - **Real vs Fake Doughnut** — your overall verdict distribution
  - **Confidence Trend** — confidence scores over your last 15 analyses

---

## Credentials Summary

| Role  | Username | Password |
|-------|----------|----------|
| Admin | admin    | admin123 |
| User  | (you create during registration) | (your choice) |

---

## Common Issues

**`No module named 'X'`** — Run `pip install -r requirements.txt` again with the virtual environment active.

**`model.joblib not found`** — The model hasn't been trained yet. Follow Step 8A.

**Login works but dashboard says "pending approval"** — Admin needs to verify the user account (Step 8C).

**`python3` not recognized on Windows** — Use `python` instead of `python3`.
