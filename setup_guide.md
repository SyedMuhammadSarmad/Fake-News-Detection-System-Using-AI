Setup & Test Guide

  Step 1 — Get the Dataset

  Download from Kaggle: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset

  Place both files here:
  datasets/
  ├── True.csv
  └── Fake.csv

  ---
  Step 2 — Start the Server

  cd "Fake News Detection System Using AI"
  python3 manage.py runserver

  Open http://127.0.0.1:8000

  ---
  Step 3 — Full End-to-End Flow

  A. Train the model (Admin)
  1. Go to http://127.0.0.1:8000/admin → login: admin / admin123
  2. Click Model Metrics in the sidebar
  3. Click the ⚙ Retrain Model button — this runs train_model() on your CSVs (takes ~1–2 min)
  4. On success you'll see accuracy/F1 scores appear in the table + the line chart

  B. Register a test user
  1. Go to http://127.0.0.1:8000/accounts/register/
  2. Fill in the form → submit → you'll see "awaiting admin approval"

  C. Verify the user (Admin)
  1. Back in admin → Users → tick the new user → Action: "Verify selected users" → Go

  D. Analyze an article
  1. Log in as the test user
  2. Go to Analyze → paste any news text (min 20 chars) → submit
  3. You should see the Real/Fake verdict + confidence progress bar

  E. Check history + export
  1. History page shows all past submissions with badges
  2. Export CSV button downloads your analysis history as a .csv file

  ---