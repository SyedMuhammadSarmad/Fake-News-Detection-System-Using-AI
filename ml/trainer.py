"""
Model training script.
Usage (standalone):
    python3 -c "
    from ml.trainer import train_model
    metrics = train_model('datasets/', 'ml_models/')
    print(metrics)
    "
Pure Python — no Django imports.
"""
import os
import random

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from ml.preprocessor import clean_text


def train_model(dataset_dir: str, model_dir: str) -> dict:
    """
    Load True.csv + Fake.csv, train a TF-IDF + LogReg model,
    persist it to model_dir, and return performance metrics.

    Returns:
        dict with keys: accuracy, precision, recall, f1_score
    """
    # ── 1. Load datasets ──
    true_path = os.path.join(dataset_dir, 'True.csv')
    fake_path = os.path.join(dataset_dir, 'Fake.csv')

    if not os.path.exists(true_path) or not os.path.exists(fake_path):
        raise FileNotFoundError(
            f'Missing dataset files. Expected:\n  {true_path}\n  {fake_path}\n'
            'Download from Kaggle: clmentbisaillon/fake-and-real-news-dataset'
        )

    true_df = pd.read_csv(true_path)
    fake_df = pd.read_csv(fake_path)

    true_df['label'] = 1   # Real
    fake_df['label'] = 0   # Fake

    # ── 2. Combine title + text, clean ──
    df = pd.concat([true_df, fake_df], ignore_index=True)

    # Handle datasets that may only have 'text' column
    if 'title' in df.columns and 'text' in df.columns:
        df['content'] = df['title'].fillna('') + ' ' + df['text'].fillna('')
    elif 'text' in df.columns:
        df['content'] = df['text'].fillna('')
    else:
        raise ValueError('Dataset must have at least a "text" column.')

    df['content'] = df['content'].apply(clean_text)

    # Drop rows where clean_text returned None/empty
    df = df[df['content'].notna() & (df['content'].str.strip() != '')]

    # ── 3. Train / test split ──
    X_train, X_test, y_train, y_test = train_test_split(
        df['content'], df['label'],
        test_size=0.2, random_state=42, stratify=df['label']
    )

    # ── 4. TF-IDF vectorization ──
    vectorizer = TfidfVectorizer(max_features=50_000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec  = vectorizer.transform(X_test)

    # ── 5. Train logistic regression ──
    model = LogisticRegression(max_iter=1000, C=1.0, solver='lbfgs')
    model.fit(X_train_vec, y_train)

    # ── 6. Evaluate ──
    y_pred = model.predict(X_test_vec)
    metrics = {
        'accuracy':  round(accuracy_score(y_test, y_pred),  4),
        'precision': round(precision_score(y_test, y_pred), 4),
        'recall':    round(recall_score(y_test, y_pred),    4),
        'f1_score':  round(f1_score(y_test, y_pred),        4),
    }

    # ── 7. Persist model + vectorizer ──
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model,      os.path.join(model_dir, 'model.joblib'))
    joblib.dump(vectorizer, os.path.join(model_dir, 'vectorizer.joblib'))

    print(f'[trainer] Model saved to {model_dir}')
    print(f'[trainer] Metrics: {metrics}')
    return metrics
