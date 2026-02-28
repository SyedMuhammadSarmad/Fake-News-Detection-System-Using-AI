"""
Text preprocessing pipeline for fake-news classification.
Pure Python — no Django imports.
"""
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords', quiet=True)
nltk.download('wordnet',   quiet=True)
nltk.download('punkt',     quiet=True)
nltk.download('punkt_tab', quiet=True)

_stop_words  = set(stopwords.words('english'))
_lemmatizer  = WordNetLemmatizer()


def clean_text(text: str) -> str:
    """
    TODO(human) — implement the 7-step NLP cleaning pipeline below.

    Steps (in order):
      1. Lowercase the entire string
      2. Remove URLs  (hint: re.sub(r'http\\S+', '', text))
      3. Keep only alphabetic chars  (re.sub(r'[^a-z\s]', '', text))
      4. Tokenize into a list of words  (text.split())
      5. Remove stop-words  (use _stop_words set defined above)
      6. Lemmatize each remaining token  (use _lemmatizer.lemmatize(token))
      7. Rejoin tokens with a single space and return the string

    The function should return a clean, space-joined string.
    """

    #Lowercase the entire string
    text = text.lower()

    #remove url
    text = re.sub(r'http\S+','',text)

    #Keep only alphabetic chars
    text = re.sub(r'[^a-z\s]','',text)

    #tokenize
    token = text.split()

    #remove stop words
    filtered = [w for w in token if w not in _stop_words ]

    #Lemmatize each remaining token
    lemmatized = [_lemmatizer.lemmatize(w) for w in filtered]

    #Rejoin tokens with a single space and return the string
    return ' '.join(lemmatized)
