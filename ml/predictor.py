"""
Inference module — loads a saved model and returns a prediction.
Pure Python — no Django imports.
"""
import os

import joblib

from ml.preprocessor import clean_text


def predict(text: str, model_dir: str) -> dict:
    """
    TODO(human) — implement the prediction pipeline below.

    Steps:
      1. Build paths:
            model_path      = os.path.join(model_dir, 'model.joblib')
            vectorizer_path = os.path.join(model_dir, 'vectorizer.joblib')
      2. Check both files exist; if not raise FileNotFoundError with a helpful message
            (hint: 'Model not found. Please ask the admin to train the model first.')
      3. Load model and vectorizer using joblib.load()
      4. Clean the input:  cleaned = clean_text(text)
      5. Vectorize:        X = vectorizer.transform([cleaned])
      6. Predict label:    label = model.predict(X)[0]   → 0 (Fake) or 1 (Real)
      7. Get probabilities: proba = model.predict_proba(X)[0]
            → array like [p_fake, p_real]
      8. Compute verdict and confidence:
            verdict    = 'Real' if label == 1 else 'Fake'
            confidence = round(float(max(proba)) * 100, 2)
      9. Return {'verdict': verdict, 'confidence': confidence}

    Parameters:
        text      (str): Raw news text submitted by the user
        model_dir (str): Directory where model.joblib and vectorizer.joblib are stored

    Returns:
        dict: {'verdict': 'Real'|'Fake', 'confidence': float 0-100}
    """
    pass
